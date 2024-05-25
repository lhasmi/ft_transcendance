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
from .models import Player, Match, MyMatch
from .serializers import PlayerSerializer, MatchSerializer, MyMatchSerializer # IMPORT MyMatchSerializer
from django.db.models import Q


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

        if not username or not password or not email:
            return Response({"error": "Username, password and email are required fields."},
                            status=status.HTTP_400_BAD_REQUEST)
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
        jwt_token = RefreshToken.for_user(user)
        return Response({
            "message": "User created successfully", 
            "refresh": str(jwt_token), 
            "access": str(jwt_token.access_token)
        }, status=status.HTTP_201_CREATED)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user login and send OTP via email.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            jwt_token = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully", 
                "refresh": str(jwt_token), 
                "access": str(jwt_token.access_token)
            }, status=status.HTTP_201_CREATED)
        #     player = getattr(user, 'player', None)
        #     if player and player.secret_key: # Check if the player has a secret_key for OTP;
        #         totp = TOTP(player.secret_key, step=60, digits=6)  # secret_key is stored in the player model
        #         otp_token = totp.token()
        #         send_mail(
        #             'Your OTP',
        #             f'Your one-time password is {otp_token}. Please enter it to complete your login.',
        #             'from@example.com',
        #             [user.email],
        #             fail_silently=False,
        #         )
        #         return Response({'message': 'OTP sent to your email. Please verify to complete login.'}, status=status.HTTP_200_OK)
        #     else:
        #         return Response({'error': 'OTP setup not found for user'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_404_NOT_FOUND)

class VerifyOTPAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Verify the OTP for completing the login process.
        """
        username = request.data.get('username')
        otp = request.data.get('otp')

        if username is None or otp is None:
            return Response({'error': 'Please provide both username and OTP'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=username)
        player = getattr(user, 'player', None)

        if user is not None and player and player.secret_key:
            totp = TOTP(player.secret_key, step=60, digits=6)
            totp.time = time.time()
            if totp.verify(otp):
                login(request, user)
                jwt_token = RefreshToken.for_user(user)
                return Response({
                    'access': str(jwt_token.access_token),
                    'refresh': str(jwt_token)
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': f'Invalid OTP. Please try again or contact the admin at {settings.ADMIN_MAIL} if the issue persists.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'OTP setup not found for user'}, status=status.HTTP_404_NOT_FOUND)

class Enable2FAAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Enable 2FA for the user by generating and sending an OTP.
        """
        user = request.user
        player = user.player
        player.generate_secret_key()
        totp = TOTP(player.secret_key, step=60, digits=6)
        otp_token = totp.token()
        send_mail(
            'Your OTP',
            f'Your one-time password is {otp_token}. Please enter it to enable 2FA.',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return Response({"message": "OTP sent to your email. Please verify to enable 2FA."}, status=status.HTTP_200_OK)


