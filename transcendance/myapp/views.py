from rest_framework import viewsets
from .models import Player, Game
from .serializers import PlayerSerializer, GameSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# using ModelViewSet, which provides a full set of read and write operations without needing to specify explicit methods for basic behavior:
#    QuerySet Configuration: Directly tying to the model’s all objects queryset, which is fine for development.
#    Serializer Class:  linked to their respective serializers.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]  # Allows access to any user

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response(
                {"error": "Username, password, and email are required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "A user with that username already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # You don't need to create the token here, it will be created by the signal
        token = Token.objects.get(user=user).key
        
        return Response(
            {"message": "User created successfully", "token": token},
            status=status.HTTP_201_CREATED
        )
