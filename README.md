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
python -m pip install Pillow
python manage.py migrate



### Before you start
myapp.Player.profile_picture: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".

#### Integration in Frontend : few tips (26.04.2024)

**Base URL:** The base URL for accessing the API is `http://127.0.0.1:8000/`. 

**1. User Registration**
- **Endpoint:** `POST /register/`
- **Payload:**
  ```json
  {
    "username": "newuser",
    "password": "password123",
    "email": "user@example.com"
  }
  ```
- **Success Response:** HTTP 201 (Created) with token
  ```json
  {
    "message": "User created successfully",
    "token": "abc123xyz"
  }
  ```
- **Error Response:** HTTP 400 (Bad Request) with error message
  ```json
  {
    "error": "A user with that username already exists."
  }
  ```

**2. User Login**
- **Endpoint:** `POST /login/`
- **Payload:**
  ```json
  {
    "username": "existinguser",
    "password": "password123"
  }
  ```
- **Success Response:** HTTP 200 (OK) with token
  ```json
  {
    "token": "xyz123abc"
  }
  ```
- **Error Response:** HTTP 404 (Not Found) with error message
  ```json
  {
    "error": "Invalid Credentials"
  }
  ```

**3. Update User Profile**
- **Endpoint:** `PUT /update-profile/`
- **Required:** User must be authenticated.
- **Payload:**
  ```json
  {
    "username": "updateduser",
    "email": "newemail@example.com",
    "password": "newpassword123"  // Optional
  }
  ```
- **Success Response:** HTTP 200 (OK) with confirmation message
  ```json
  {
    "message": "User profile updated successfully"
  }
  ```
- **Headers:** Include the Authorization header with the token.
  ```
  Authorization: Token xyz123abc
  ```

### Additional Tips
- **Testing:** I recommend using tools like Postman or similar to thoroughly test these endpoints before integrating them into the frontend.

##### For the form handling profile pictures
 the frontend form that submits to this API should use enctype="multipart/form-data" 


#### ################################################################################################# 
### Dependencies to incorporate real-time functionality and WebSocket integration with Django Channels,
#### ##################################################################################################

#  Install Django Channels and ASGI Redis and daphne for testing
pip install channels channels-redis daphne

# on  macos install redis
brew install redis

# start redis manually you should see "==> Successfully started `redis` (label: homebrew.mxcl.redis)"
brew services start redis
# verify redis is running
redis-cli ping

# call it admin pass admin email admin@example.com, confirm with y
python manage.py migrate
python manage.py createsuperuser

# 42auth
pip install django-oauth-toolkit

python manage.py runserver


