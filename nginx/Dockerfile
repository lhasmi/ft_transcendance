# Use NGINX official image as base
FROM nginx:latest AS nginx-base

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 443
