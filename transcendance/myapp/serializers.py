from rest_framework import serializers
from .models import Player, Match
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Player
        fields = ['id', 'user', 'profile_picture', 'created_at', 'display_name', 'online_status']
        extra_kwargs = {'profile_picture': {'required': False}}
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MatchSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)
    class Meta:
        model = Match
        fields = ['id', 'players',  'winner', 'played_on', 'details']

#Serializers help convert  Django models (or querysets) into JSON format,
# which can then be used by APIs to communicate with the frontend.
#extend ModelSerializer, which simplifies serialization of model instances:
#  Fields Specification: enumerating fields that should be serialized/deserialized. 
#   Meta Class Usage: Standard practice for DRF serializers.