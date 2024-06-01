# Use NGINX official image as base
FROM nginx:latest AS nginx-base

# Copy custom NGINX configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

# Copy the certificate generation script
COPY generate_cert.sh /generate_cert.sh

# Make the script executable
RUN chmod +x /generate_cert.sh

# Set the entrypoint to the script
ENTRYPOINT ["/generate_cert.sh"]
