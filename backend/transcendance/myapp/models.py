import base64
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    display_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='media/', default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    online_status = models.IntegerField(default=0) # Changed from BooleanField to IntegerField
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    secret_key = models.CharField(max_length=100, blank=True, null=True)  # to store TOTP secret key
    two_fa_method = models.CharField(max_length=10, choices=[('email', 'Email')], default='email')
    two_fa_requested = models.BooleanField(default=False) 
    two_fa_activated = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.user.username}'s Player Profile"
    def set_online(self):## For status online tracking
        self.online_status += 1  # Increment online status(OS) counter
        self.save()
    def set_offline(self):## For status offline tracking
        if self.online_status > 0:
            self.online_status -= 1  # Decrement OS counter
        self.save()
    def generate_secret_key(self):
        if not self.secret_key:
            self.secret_key = get_random_string(20)
            self.save()

    # otp_enabled = models.BooleanField(default=False) 
# self.otp_enabled = True  # Enable OTP when a secret key is generated
class Match(models.Model):
    players = models.ManyToManyField(Player, related_name="matches")
    winner = models.ForeignKey(Player, related_name="won_matches", on_delete=models.SET_NULL, null=True)
    played_on = models.DateTimeField(auto_now_add=True) # Automatically set the date when the match is created
    user_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)

class MyMatch(models.Model):
    player1 = models.CharField(null=True)
    player2 = models.CharField(null=True)
    winner = models.CharField(null=True)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    played_on = models.DateTimeField(auto_now_add=True)
# Foreign Key Relations: using related_name for backwards navigation in relations.


# In Player model, we link every player with a specific user instance, which allows to add custom 
# fields like profile_picture. This design inherits and extends the base User model capabilities
# by association rather than by modifying the existing User model. It is called a One-to-One relationship
# For status online/offline tracking
