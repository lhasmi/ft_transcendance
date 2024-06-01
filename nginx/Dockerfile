# Use the official Nginx image as a base
FROM nginx:latest

# Install OpenSSL to generate SSL certificates
RUN apt-get update && apt-get install -y openssl

# Generate self-signed SSL certificates
RUN mkdir -p /etc/nginx/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/certs/server.key \
    -out /etc/nginx/certs/server.crt \
    -subj "/CN=ft_transcendence"

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 443
