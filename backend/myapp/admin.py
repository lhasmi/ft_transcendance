from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Player, Match, MyMatch

# Defines how player entries are displayed and managed in the Django admin interface.
class PlayerAdmin(admin.ModelAdmin):
    # List display for the fields to display in the list view.
    list_display = ('get_username', 'get_email', 'display_name', 'profile_picture', 'created_at', 'online_status', 'two_fa_activated')
    readonly_fields = ('profile_picture', 'created_at')
    search_fields = ('user__username', 'user__email', 'display_name')
    list_filter = ('online_status', 'two_fa_activated')  
   
    actions = ['reset_otp']

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user__username'  # Allows column order sorting
    get_username.short_description = 'Username'  # Renames column head

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

    def two_fa_activated(self, obj):
        return bool(obj.two_fa_activated)  # Check the wo_fa_activated field
    two_fa_activated.boolean = True
    two_fa_activated.short_description = 'two fa activated'

    # Operates directly from the Django admin interface, on multiple selected players
    def reset_otp(self, request, queryset):  # Calls generate_secret_key on each player to reset their OTP secret key.
        for player in queryset:
            player.generate_secret_key()
            two_fa_activated.boolean = True
            player.save()
        self.message_user(request, "OTP reset for selected players.")
    reset_otp.short_description = 'Reset OTP for selected players'

class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_players', 'winner', 'played_on',  'user_score', 'opponent_score')
    search_fields = ('players__user__username', 'winner__user__username')
    list_filter = ('played_on',)
    
    def display_players(self, obj): #provides a link to a custom admin view where OTP can be reset. 
        return ", ".join([player.user.username for player in obj.players.all()])
    display_players.short_description = 'Players'

class MyMatchAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'score1', 'score2', 'played_on')

admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MyMatch, MyMatchAdmin)

# handles resetting the OTP secret for a single player when accessed via a specific URL.
# the function returns to Django admin interface
# @staff_member_required 
# def reset_otp_secret(request, username):
#     user = get_object_or_404(User, username=username)
#     player = get_object_or_404(Player, user=user)
#     player.generate_secret_key()
#     player.save()
#     return HttpResponseRedirect(reverse('admin:myapp_player_changelist'))
# for that to work the line bellow has to be added to the urls.py 
# path('admin/reset_otp/<str:username>/', reset_otp_secret, name='reset_otp'), # only if we decide to uncomment the standalone function in admin.py
