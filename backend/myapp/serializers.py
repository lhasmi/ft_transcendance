from rest_framework import serializers
from .models import Player, Match, MyMatch
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class PublicPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        # fields = ['id', 'display_name']
        fields = ['id', 'user']

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = serializers.SerializerMethodField()#to customize the serialization of friends

    class Meta:
        model = Player
        fields = [
            'id', 'user', 'profile_picture', 'created_at', 'display_name', 
            'online_status', 'friends', 'two_fa_requested', 'two_fa_activated'
        ]
        extra_kwargs = {
            'profile_picture': {'required': False},
            'two_fa_requested': {'read_only': True},
            'two_fa_activated': {'read_only': True}#read_only prevents from being 
            #altered through API endpoints 
        }
    
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
        fields = ['id', 'user', 'online_status']  # to allow users to see the status of their friends

class MatchSerializer(serializers.ModelSerializer):
    ## Show all players in the match
    players = serializers.ListField(
        child=serializers.CharField(),  # Accept usernames as strings
        write_only=True
    )
    winner = serializers.CharField(write_only=True) 
    players_detail = PublicPlayerSerializer(read_only=True, many=True, source='players')
    # winner_detail = PublicPlayerSerializer(read_only=True, source='winner')
    user_score = serializers.IntegerField()  
    opponent_score = serializers.IntegerField()

    class Meta:
        model = Match
        # fields = ['id', 'players',  'winner', 'played_on', 'user_score', 'opponent_score', 'players_detail', 'winner_detail', 'is_winner']
        fields = ['id', 'players',  'winner', 'played_on', 'user_score', 'opponent_score', 'players_detail', 'winner_detail']

    def validate_players(self, value):
        players = []
        # for username in value: # removed because we need to validate only the logged in user, the other user is a guest
        #     try:
        #         player = Player.objects.get(user__username=username)
        #         players.append(player)
        #     except Player.DoesNotExist:
        #         raise serializers.ValidationError(f"Player with username '{username}' does not exist.")
        try:
            player = Player.objects.get(user__username=value[0])
            players.append(player)
        except Player.DoesNotExist:
            raise serializers.ValidationError(f"Player with username '{value[0]}' does not exist.")
        return players

    def validate_winner(self, value):
        # try:
        #     winner = Player.objects.get(user__username=value)
        # except Player.DoesNotExist:
        #     raise serializers.ValidationError(f"Player with username '{value}' does not exist.")
        winner = value
        return winner

    def create(self, validated_data):
        players = validated_data.pop('players')
        winner = validated_data.pop('winner')
        match = Match.objects.create(winner=winner, **validated_data)
        match.players.set(players)
        return match

    def update(self, instance, validated_data):
        players = validated_data.pop('players', None)
        winner = validated_data.pop('winner', None)
        if players is not None:
            instance.players.set(players)
        if winner is not None:
            instance.winner = winner
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MyMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyMatch
        fields = ['player1', 'player2', 'winner', 'score1', 'score2', 'played_on']
#Serializers help convert  Django models (or querysets) into JSON format,
# which can then be used by APIs to communicate with the frontend.
#extend ModelSerializer, which simplifies serialization of model instances:
#  Fields Specification: enumerating fields that should be serialized/deserialized. 
#   Meta Class Usage: Standard practice for DRF serializers.