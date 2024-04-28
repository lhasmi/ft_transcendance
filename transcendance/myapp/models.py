from django.db import models
from django.contrib.auth.models import User
# Foreign Key Relations: using related_name for backwards navigation in relations.

class Game(models.Model):
    player1 = models.ForeignKey('Player', related_name='games_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey('Player', related_name='games_as_player2', on_delete=models.CASCADE)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    game_over = models.BooleanField(default=False)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_picture = models.ImageField(upload_to='media/', default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    #any reference to username or email can directly use player.user.username and player.user.email.
    def __str__(self):
        return f"{self.user.username}'s Player Profile"
