#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Generate self-signed SSL certificate
mkdir -p /etc/nginx/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/certs/server.key -out /etc/nginx/certs/server.crt -subj "/CN=example.com/O=example.com/C=US"

# Start NGINX
nginx -g "daemon off;"
