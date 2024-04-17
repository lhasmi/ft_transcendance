from django.db import models
# Foreign Key Relations: using related_name for backwards navigation in relations.

class Game(models.Model):
    player1 = models.ForeignKey('Player', related_name='games_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey('Player', related_name='games_as_player2', on_delete=models.CASCADE)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    game_over = models.BooleanField(default=False)

class Player(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

