# Use a slim Python image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set Django settings module relative to the Python module path, not the file system path.
ENV DJANGO_SETTINGS_MODULE=transcendance.settings

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


# Set the correct work directory to where manage.py is located
WORKDIR /app/transcendance


# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make entrypoint script executable
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000


# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Use Gunicorn to serve the application
CMD ["gunicorn", "transcendance.asgi:application", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]
