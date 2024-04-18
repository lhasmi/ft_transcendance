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

### List of dependencies to be installed before running Frontend

brew install node
### List of dependencies to be installed before running backend

brew upgrade python

pip install virtualenv

python3.11 -m pip install --upgrade pip

# navigate inside the parent directory of the django project ( ft_transcendance), then create the virtual environment
# vtrans is the name I gave to the virtual environment
virtualenv vtrans
# now the vtrans is at the same level as transcendance and inside transcendance we have manage.py and the transcendance directory and the myapp directory
source vtrans/bin/activate

pip install django djangorestframework

pip install python-dotenv

brew install postgresql

pip install django-cors-headers
pip install psycopg2
brew services start postgresql@14
pg_ctl -D /Users/lhasmi/.brew/var/postgresql@14 status
psql -d postgres
# insie the database prompt :
CREATE ROLE lh_db WITH LOGIN PASSWORD '<copy password from .env>';
ALTER ROLE lh_db CREATEDB;
CREATE DATABASE "djangotrans_db";
\l
\q

python manage.py migrate

python manage.py createsuperuser
# call it admin pass admin email admin@example.com, confirm with y
python manage.py migrate
python manage.py runserver

