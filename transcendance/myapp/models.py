import base64
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    display_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='media/', default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    online_status = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    secret_key = models.CharField(max_length=100, blank=True, null=True)  # to store TOTP secret key
    two_fa_method = models.CharField(max_length=10, choices=[('email', 'Email'), ('sms', 'SMS')], default='email')
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # to store phone number for SMS 2FA
    #any reference to username or email can directly use player.user.username and player.user.email.
    def __str__(self):
        return f"{self.user.username}'s Player Profile"
    def set_online(self):## For status online tracking
        self.online_status = True
        self.save()
    def set_offline(self):## For status offline tracking
        self.online_status = False
        self.save()
    def generate_secret_key(self):
        if not self.secret_key:
            self.secret_key = get_random_string(20)
            self.save()

class Match(models.Model):
    players = models.ManyToManyField(Player, related_name="matches")
    winner = models.ForeignKey(Player, related_name="won_matches", on_delete=models.SET_NULL, null=True)
    played_on = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

# Foreign Key Relations: using related_name for backwards navigation in relations.


# In Player model, we link every player with a specific user instance, which allows to add custom 
# fields like profile_picture. This design inherits and extends the base User model capabilities
# by association rather than by modifying the existing User model. It is called a One-to-One relationship
# For status online/offline tracking
