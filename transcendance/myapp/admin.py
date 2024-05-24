from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Player, Match

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'display_name', 'profile_picture', 'created_at', 'online_status', 'manage_otp')
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

    def manage_otp(self, obj):
        return format_html('<a href="{}">Manage OTP</a>', 
                           reverse('manage_otp', args=[obj.user.username]))
    manage_otp.short_description = 'OTP Management'

class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_players', 'winner', 'played_on',  'user_score', 'opponent_score')
    search_fields = ('players__user__username', 'winner__user__username')
    list_filter = ('played_on',)
    
    def display_players(self, obj): #provides a link to a custom admin view where OTP can be reset. 
        return ", ".join([player.user.username for player in obj.players.all()])
    display_players.short_description = 'Players'


admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)

@staff_member_required
def reset_otp_secret(request, player_id):
    user = get_object_or_404(User, username=username)
    player = get_object_or_404(Player, user=user)
    player.generate_secret_key()
    player.save()
    return HttpResponseRedirect('/admin/app/player/')