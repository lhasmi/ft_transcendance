#!/bin/sh

# Apply database migrations
python /usr/src/app/transcendance/manage.py migrate --noinput || true

# Start the server
python /usr/src/app/transcendance/manage.py runserver 0.0.0.0:8000