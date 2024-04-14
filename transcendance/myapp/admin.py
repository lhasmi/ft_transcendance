from django.contrib import admin

# Register models here.
from .models import Player, Game

admin.site.register(Player)
admin.site.register(Game)
