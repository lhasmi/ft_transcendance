#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Start the application
echo "Starting server..."
exec "$@"
