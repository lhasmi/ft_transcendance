from django.core.management.base import BaseCommand
from myapp.models import Player

#Resets the online status of all players to 0
class Command(BaseCommand):

    def handle(self, *args, **options):
        players = Player.objects.all()
        players.update(online_status=0)
        self.stdout.write(self.style.SUCCESS('Successfully reset online status for all players.'))
