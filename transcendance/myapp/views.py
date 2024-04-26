from rest_framework import viewsets
from .models import Player, Game
from .serializers import PlayerSerializer, GameSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# using ModelViewSet, which provides a full set of read and write operations without needing to specify explicit methods for basic behavior:
#    QuerySet Configuration: Directly tying to the model’s all objects queryset, which is fine for development.
#    Serializer Class:  linked to their respective serializers.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().select_related('user') 
    serializer_class = PlayerSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"error": "Username, password, and email are required fields."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "A user with that username already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with that email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
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


class UserProfileUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')  # Optional: handle changing password securely

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        
        user.save()
        return Response({'message': 'User profile updated successfully'}, status=status.HTTP_200_OK)
