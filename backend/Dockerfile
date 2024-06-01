# Use a slim Python image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the correct work directory to where manage.py is located
WORKDIR /app/transcendance

# Expose port
EXPOSE 8000

# Set Django settings module
ENV DJANGO_SETTINGS_MODULE=transcendance.settings

# Use the entrypoint script to run migrations and start the server
ENTRYPOINT ["/entrypoint.sh"]
