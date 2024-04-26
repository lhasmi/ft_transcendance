from django.contrib import admin
from .models import Player, Game
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'profile_picture', 'created_at')
    readonly_fields = ('profile_picture',)

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field  = 'user__username'  # Allows column order sorting
    get_username.short_description = 'Username'  # Renames column head

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

admin.site.register(Player, PlayerAdmin)

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'score1', 'score2', 'game_over')
    list_filter = ('game_over',)
    search_fields = ('player1__user__username', 'player2__user__username')

admin.site.register(Game, GameAdmin)

