from django.db import models
from django.contrib.auth.models import User
# Foreign Key Relations: using related_name for backwards navigation in relations.



class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    display_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='media/', default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    online_status = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True)
    #any reference to username or email can directly use player.user.username and player.user.email.
    def __str__(self):
        return f"{self.user.username}'s Player Profile"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(Player, related_name="friend_requests_sent", on_delete=models.CASCADE)
    to_user = models.ForeignKey(Player, related_name="friend_requests_received", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Match(models.Model):
    players = models.ManyToManyField(Player, related_name="matches")
    winner = models.ForeignKey(Player, related_name="won_matches", on_delete=models.SET_NULL, null=True)
    played_on = models.DateTimeField(auto_now_add=True)
    details = models.TextField()