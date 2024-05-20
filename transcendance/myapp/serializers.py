from rest_framework import serializers
from .models import Player, Match
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = serializers.SerializerMethodField()#to customize the serialization of friends
    class Meta:
        model = Player
        fields = ['id', 'user', 'profile_picture', 'created_at', 'display_name', 'online_status', 'friends']
        extra_kwargs = {'profile_picture': {'required': False}}
    
    def get_friends(self, obj):
        friends = obj.friends.all()
        return PlayerFriendSerializer(friends, many=True).data
    # Bellow lines, are just a safeguard, since the update is already handled in views (09.05.2024)
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:# Update User data if provided
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
        for attr, value in validated_data.items():# Update Player data
            setattr(instance, attr, value)
        instance.save()
        return instance

class PlayerFriendSerializer(serializers.ModelSerializer):#for simplified view of a player's friends.
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ['id', 'user', 'online_status']

class MatchSerializer(serializers.ModelSerializer):
    ## Show all players in the match
    players = PlayerSerializer(read_only=True, many=True)
    winner = PlayerSerializer(read_only=True)  # Show the winner's details
    is_winner = serializers.BooleanField(read_only=True)
    class Meta:
        model = Match
        fields = ['id', 'players',  'winner', 'played_on', 'details', 'is_winner']
    
#Serializers help convert  Django models (or querysets) into JSON format,
# which can then be used by APIs to communicate with the frontend.
#extend ModelSerializer, which simplifies serialization of model instances:
#  Fields Specification: enumerating fields that should be serialized/deserialized. 
#   Meta Class Usage: Standard practice for DRF serializers.