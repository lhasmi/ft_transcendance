#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Debug Print 
echo "Environment Variables:"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DATABASE_NAME: $DB_NAME"
echo "DATABASE_USER: $DB_USER"
echo "DATABASE_PASSWORD: $DB_PASSWORD"
echo "DATABASE_HOST: $DB_HOST"
echo "DATABASE_PORT: $DB_PORT"

# Start the application
echo "Starting server..."
exec "$@"
