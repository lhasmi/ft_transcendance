# myapp/management/commands/backfill_otp_enabled.py
# to backfill the otp_enabled field for existing players
from django.core.management.base import BaseCommand
from myapp.models import Player

class Command(BaseCommand):
    help = 'Backfill otp_enabled field for existing users'

    def handle(self, *args, **kwargs):
        players = Player.objects.all()
        updated_count = 0
        for player in players:
            if player.secret_key and not player.otp_enabled:
                player.otp_enabled = True
                player.save()
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} players.'))
