from rest_framework import viewsets, status, permissions
from .models import Player, FriendRequest, Match
from .serializers import PlayerSerializer, MatchSerializer
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
# using ModelViewSet, provides a full set of read and write operations without needing to specify explicit methods for basic behavior:
#    QuerySet Configuration: Directly tying to the model’s all objects queryset, which is fine for development.
#    Serializer Class:  linked to their respective serializers.


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().select_related('user') 
    serializer_class = PlayerSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

def validate_email(email):
    if not email:
        raise DjangoValidationError("Email address is required.")
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, email):
        raise DjangoValidationError("Invalid email format.")

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        display_name = request.data.get('display_name')
        if not username or not password or not email:
            return Response({"error": "Username, password, and email are required fields."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)  # Validate email format
        except DjangoValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "A user with that username already exists."},
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with that email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        player = Player.objects.create(user=user, display_name=display_name)
        token = Token.objects.get(user=user).key
        return Response({"message": "User created successfully", "token": token},
                        status=status.HTTP_201_CREATED)



class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)


def validate_image(image):
    max_size = 2 * 1024 * 1024  # 2MB
    if image.size > max_size:
        raise DjangoValidationError("The maximum file size that can be uploaded is 2MB")
    if not image.name.endswith(('.png', '.jpg', '.jpeg')):
        raise DjangoValidationError("Only JPEG and PNG files are allowed.")
    


class UserProfileUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)  # to handle file upload

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

# API View for sending friend requests
# to do : preventing duplicate friend requests, handling non-existent user IDs 
#securing endpoints against unauthorized access.
class FriendRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, to_player_id):
        try:
            to_player = Player.objects.get(id=to_player_id)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.player == to_player:
            return Response({'error': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.player.friends.filter(id=to_player.id).exists() or FriendRequest.objects.filter(from_user=request.user.player, to_user=to_player).exists():
            return Response({'error': 'Already friends or friend request already sent.'}, status=status.HTTP_409_CONFLICT)
        
        FriendRequest.objects.create(from_user=request.user.player, to_user=to_player)
        return Response({'message': 'Friend request sent.'}, status=status.HTTP_200_OK)

# API View to accept a friend request
#  Ensure user input is sanitized and validated if friend requests. 
class AcceptFriendRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, request_id):
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user.player)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

        request.user.player.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user.player)
        friend_request.delete()
        return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)


class MatchHistoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        player = request.user.player
        matches = Match.objects.filter(players=player)
        data = MatchSerializer(matches, many=True).data
        return Response(data, status=status.HTTP_200_OK)
# above : adjusted to filter matches involving the logged-in user's Player profile.  

class UserStatsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        wins = Match.objects.filter(winner=user).count()
        total_games = user.matches.count()
        data = {'wins': wins, 'losses': total_games - wins}
        return Response(data, status=status.HTTP_200_OK)

class UpdateOnlineStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        player = request.user.player
        player.online_status = True
        player.save()
        return Response({'message': 'Online status updated.'})

class ListOnlineFriendsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        player = request.user.player
        friends = Player.objects.filter(user__friend_set__users=player.user, online_status=True)
        serializer = PlayerSerializer(friends, many=True)
        return Response(serializer.data)