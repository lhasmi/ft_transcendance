# ft_transcendance
# see the notion page for detailled logs

### testing the Apis with curl
# To test the Player list and creation endpoint:


# To get a list of players
curl -X GET http://localhost:8000/players/ -H 'Accept: application/json'

# To create a new player
curl -X POST http://localhost:8000/players/ \
     -H 'Content-Type: application/json' \
     -d '{"username": "newplayer", "email": "player@example.com"}'

# Replace localhost:8000 with your actual server’s URL if not testing locally.

#### creating a new user using the Django shell.

python manage.py shell

# in the shell prompt:

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
user = User.objects.create_user('newuser' 'test@example.com', 'password123')
token, created = Token.objects.get_or_create(user=user)
print(token.key)
