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

python3 manage.py shell

# in the shell prompt:

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
user = User.objects.create_user('newuser' 'test@example.com', 'password123')
token, created = Token.objects.get_or_create(user=user)
print(token.key)

### List of dependencies to be installed before running Frontend

brew install node

#### ########################################################### 
### List of dependencies to be installed before running backend
#### ########################################################### 

brew upgrade python
python3.11 -m pip install --upgrade pip

pip3 install virtualenv


# create the virtual environment
# vtrans is the name I gave to the virtual environment
virtualenv vtrans
# now the vtrans is at /Users/lailah
source vtrans/bin/activate

# This command will output a list of installed packages along with their versions. & Save the dependencies to a file:
pip3 freeze > requirements.txt  # to save the dependencies to a file
# you need to be inside the virt env first, for my case:
source /Users/lailah/vtrans/bin/activate 
pip3 freeze > /Users/lailah/transcendance/ft_transcendance_09052024/requirements.txt
# to install them all at once
pip3 install -r requirements.txt

# Bellow are the dependencies 
pip3 install djangorestframework
pip3 install python-dotenv
brew install postgresql
python3 -m pip install Pillow
pip3 install django-cors-headers
pip3 install psycopg2
brew services start postgresql@14
pg_ctl -D /Users/lhasmi/.brew/var/postgresql@14 status
psql -d postgres
# insie the database prompt :
CREATE ROLE lh_db WITH LOGIN PASSWORD '<copy password from .env>';
ALTER ROLE lh_db CREATEDB;
CREATE DATABASE "djangotrans_db";
\l
\q
python3 manage.py migrate

python3 manage.py createsuperuser
# call it admin pass admin email admin@example.com, confirm with y
python3 manage.py migrate
python3 manage.py runserver


### Before you start
myapp.Player.profile_picture: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python3 -m pip install Pillow".

#### ###############################
## !!!!!!! LOOK HERE BELLOW !!!!!!!:
#### ##############################

#### ################################################################################################# 
### Dependencies to incorporate real-time functionality and WebSocket integration with Django Channels,
### and 2 F auth ( otp) and jwt
#### ##################################################################################################

#  Install Django Channels and ASGI Redis and daphne for testing
pip3 install channels channels-redis daphne

# on  macos install redis
brew install redis

# start redis manually you should see "==> Successfully started `redis` (label: homebrew.mxcl.redis)"
brew services start redis
# verify redis is running
redis-cli ping

### For 2F Auth to work:
pip3 install django-cryptography
pip3 install django_otp
pip3 install djangorestframework-simplejwt

# on macOS, you need to install the certificates using the Install Certificates.command that comes with Python:
    Find the Install Certificates.command File:

    Here's how you can find it:
        Open Finder.
        Go to the Applications folder.
        Look for the Python folder (e.g., Python 3.8 if you have Python 3.8 installed).
        Inside the Python folder, you should find the Install Certificates.command file.

    Run the Install Certificates.command File:
        Double-click the Install Certificates.command file.
        A terminal window should open, and the command will run automatically to install the necessary SSL certificates.
# Install OpenSSL using Homebrew: first verify if you have it by "openssl --version"
brew install openssl

# Link the installed OpenSSL:
brew link openssl --force

there is a space at the end of the email password in .env ! be aware of it!
### For https on developpment server
pip3 install django-extensions
# generate a certificate ( has to be dynamically generated in docker, prob: it is interactive )
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
pip3 install Werkzeug
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem

# for Frontend :  
 to handle entering the OTP (one time password) sent via email or SMS during the login process.

 example of how the frontend can send data about match results

{
    "players": ["player1", "player2"],
    "winner": "player1",
    "played_on": "2023-05-20T14:28:23.382Z",
    "details": "Match details here."
}
