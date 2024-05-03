from django.contrib import admin
from .models import Player, Match, FriendRequest
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'display_name', 'profile_picture', 'created_at', 'online_status')
    readonly_fields = ('profile_picture', 'created_at')
    search_fields = ('user__username', 'user__email', 'display_name')
    list_filter = ('online_status',)

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field  = 'user__username'  # Allows column order sorting
    get_username.short_description = 'Username'  # Renames column head

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_players', 'winner', 'played_on', 'details')
    search_fields = ('players__user__username', 'winner__user__username')
    list_filter = ('played_on',)
    
    def display_players(self, obj):
        return ", ".join([player.user.username for player in obj.players.all()])
    display_players.short_description = 'Players'

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'timestamp')
    search_fields = ('from_user__user__username', 'to_user__user__username')
    list_filter = ('timestamp',)

    def from_user(self, obj):
        return obj.from_user.user.username

    def to_user(self, obj):
        return obj.to_user.user.username

admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
