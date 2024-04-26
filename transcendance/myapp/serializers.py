#Serializers help convert  Django models (or querysets) into JSON format,
# which can then be used by APIs to communicate with the frontend.
#extend ModelSerializer, which simplifies serialization of model instances:
#  Fields Specification: enumerating fields that should be serialized/deserialized. 
#   Meta Class Usage: Standard practice for DRF serializers.
from rest_framework import serializers
from .models import Player, Game
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Embed UserSerializer for nested user data

    class Meta:
        model = Player
        fields = ['id', 'user', 'profile_picture', 'created_at']


class GameSerializer(serializers.ModelSerializer):
    player1 = PlayerSerializer(read_only=True)
    player2 = PlayerSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'player1', 'player2', 'score1', 'score2', 'game_over']
