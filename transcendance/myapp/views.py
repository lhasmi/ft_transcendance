from rest_framework import viewsets
from .models import Player, Game
from .serializers import PlayerSerializer, GameSerializer
# using ModelViewSet, which provides a full set of read and write operations without needing to specify explicit methods for basic behavior:

#    QuerySet Configuration: Directly tying to the model’s all objects queryset, which is fine for development.
#    Serializer Class:  linked to their respective serializers.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
