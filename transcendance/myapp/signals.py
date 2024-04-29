from django.db import transaction
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Player
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_player_profile(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            with transaction.atomic():
                Player.objects.create(user=instance)
                logger.info(f"Player profile created for user {instance.username}")
        except Exception as e:
            logger.error(f"Failed to create player profile for user {instance.username}: {e}")
