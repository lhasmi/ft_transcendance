import re
import base64
import time

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Case, When, Value, BooleanField
from django.shortcuts import get_object_or_404
from django_otp.oath import TOTP
from rest_framework import viewsets, status, permissions, filters
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# from twilio.rest import Client 
from .models import Player, Match
from .serializers import PlayerSerializer, MatchSerializer

# twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
# def send_sms(phone_number, message):
#     twilio_client.messages.create(
#         body=message,
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=phone_number
#     )

def validate_email(email):
    """
    Validates the provided email for correct format.
    """
    if not email:
        raise DjangoValidationError("Email address is required.")
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, email):
        raise DjangoValidationError("Invalid email format.")

def validate_image(image):
    """
    Validates the uploaded image for size and format.
    """
    max_size = 2 * 1024 * 1024  # 2MB
    if image.size > max_size:
        raise DjangoValidationError("The maximum file size that can be uploaded is 2MB")
    if not image.name.endswith(('.png', '.jpg', '.jpeg')):
        raise DjangoValidationError("Only JPEG and PNG files are allowed.")

class PlayerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing player profiles.
    """
    queryset = Player.objects.all().select_related('user')
    serializer_class = PlayerSerializer
    filter_backends = (filters.OrderingFilter,)

class MatchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and updating match history 
    """
    queryset = Match.objects.all()
    ordering_fields = ['played_on']
    ordering = ['-played_on']
    serializer_class = MatchSerializer

    def create(self, request, *args, **kwargs):#equivalent to post
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):#equivalent to put
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        display_name = request.data.get('display_name')
        two_fa_method = request.data.get('two_fa_method')  # Get the 2FA method (email or sms)
        # phone_number = request.data.get('phone_number')  # Get the phone number if SMS is selected

        if not username or not password or not email or not two_fa_method:
            return Response({"error": "Username, password, email, and 2FA method are required fields."},
                            status=status.HTTP_400_BAD_REQUEST)
        if two_fa_method not in ['email', 'sms']:
            return Response({"error": "Invalid 2FA method. Choose 'email' or 'sms'."},
                            status=status.HTTP_400_BAD_REQUEST)
        # if two_fa_method == 'sms' and not phone_number:
        #     return Response({"error": "Phone number is required for SMS 2FA."},
        #                     status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)
        except DjangoValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "A user with that username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with that email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        if display_name:
            user.player.display_name = display_name
            user.player.save()

        try:
            totp = TOTP(user.player.secret_key, step=60, digits=6) # Initialize TOTP object
            otp_token = totp.token()
            if two_fa_method == 'email':
                send_mail( # Send token via email or SMS
                    'Your OTP',
                    f'Your one-time password is {otp_token}. Please enter it to complete your registration.',
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
            elif two_fa_method == 'sms':
                return Response({"error": "SMS is not supported by our Website"}, status=status.HTTP_400_BAD_REQUEST)
                # send_sms(phone_number, f'Your OTP is {otp_token}')
        except DjangoValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        jwt_token = RefreshToken.for_user(user)
        return Response({
            "message": "User created successfully", 
            "refresh": str(jwt_token), 
            "access": str(jwt_token.access_token)
        }, status=status.HTTP_201_CREATED)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        otp = request.data.get('otp')
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            player = getattr(user, 'player', None)
            # Check if the player has a secret_key for OTP; assuming it's stored securely in player profile
            if player and player.secret_key:
                totp = TOTP(player.secret_key)  # secret_key is stored in the player model
                totp.time = time.time()
                if totp.verify(otp):
                    login(request, user)
                    jwt_token = RefreshToken.for_user(user)
                    return Response({
                        'access': str(jwt_token.access_token),
                        'refresh': str(jwt_token)
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid OTP. Please try again or contact the admin at {settings.ADMIN_MAIL} if the issue persists.'}, status=status.HTTP_401_UNAUTHORIZED) 
            else:
                return Response({'error': 'OTP setup not found for user'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_404_NOT_FOUND)

class UserProfileUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)  # file upload

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            player = user.player
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response({"error": "Player profile does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        try:
            player = user.player  # Accessing the Player model of this User
        except Player.DoesNotExist:
            return Response({"error": "Player profile does not exist"}, status=status.HTTP_404_NOT_FOUND)
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        profile_picture = request.FILES.get('profile_picture')  # Get uploaded image
        display_name = request.data.get('display_name')

        try:
            with transaction.atomic(): # changes to DB are rolled back if any part fails
                if username and username != user.username:
                    if User.objects.filter(username=username).exists():
                        return Response({"error": "This username is already taken."}, status=status.HTTP_400_BAD_REQUEST)
                    user.username = username
                if email and email != user.email:
                    try:
                        validate_email(email)  # Validate email format
                    except DjangoValidationError as ve:
                        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
                    if User.objects.exclude(id=user.id).filter(email=email).exists():  # Check if any other user has this email
                        return Response({"error": "This email is already in use by another user."}, status=status.HTTP_400_BAD_REQUEST)
                    user.email = email
                if password:
                    user.set_password(password)
                    user.save()
                    logout(request)  # Log out from all sessions after password change
                if profile_picture:
                    try:
                        validate_image(profile_picture)
                    except DjangoValidationError as ve:
                        raise DRFValidationError({'profile_picture': [str(ve)]})
                    player.profile_picture = profile_picture
                if display_name:
                    if Player.objects.filter(display_name=display_name).exclude(user=user).exists():
                        return Response({"error": "This display name is already taken."}, status=status.HTTP_400_BAD_REQUEST)
                    player.display_name = display_name
                user.save()
                player.save()
            return Response({'message': 'User profile updated successfully'}, status=status.HTTP_200_OK)
        except DjangoValidationError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Failed to update profile due to an unexpected error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FriendRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        friend_username = request.data.get('username')
        if not friend_username:
            return Response({'error': 'Username is required to add a friend'}, status=status.HTTP_400_BAD_REQUEST)

        friend_user = get_object_or_404(User, username=friend_username)
        friend_player = get_object_or_404(Player, user=friend_user)

        if request.user.player == friend_player:
            return Response({'error': 'You cannot add yourself as a friend'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.player.friends.filter(id=friend_player.id).exists():
            return Response({'error': 'Already friends'}, status=status.HTTP_409_CONFLICT)
        request.user.player.friends.add(friend_player)
        #friend_player.friends.add(request.user.player) #no need for this line since now symmetrical is true

        return Response({'message': 'Friend added successfully'}, status=status.HTTP_200_OK)

class ListFriendsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        player = request.user.player
        friends = player.friends.all()
        serializer = PlayerSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateOnlineStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        player = request.user.player
        status = request.data.get('status', 'online')
        if status == 'online':
            player.set.online()
        else:
            player.set.offline()
        #player.online_status = True
        #player.save()
        return Response({'message': f'Player is now {status}.'})

class UserStatsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        player = request.user.player
        wins = Match.objects.filter(winner=player).count()
        total_games = player.matches.count()
        data = {'wins': wins, 'losses': total_games - wins}
        return Response(data, status=status.HTTP_200_OK)

class MatchHistoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        player = request.user.player
        ordering = request.query_params.get('ordering', '-played_on')
        matches = Match.objects.filter(players=player).order_by(ordering).annotate(
            is_winner=Case(
                When(winner=player, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        data = MatchSerializer(matches, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    # above : adjusted to filter matches involving the logged-in user's Player profile.
 

# using ModelViewSet, provides a full set of read and write operations without needing to specify explicit methods for basic behavior:
#    QuerySet Configuration: Directly tying to the model’s all objects queryset, which is fine for development.
#    Serializer Class:  linked to their respective serializers.

# API View for sending friend requests
# to do : preventing duplicate friend requests, handling non-existent user IDs 
#securing endpoints against unauthorized access.