FROM node:lts-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG VITE_APP_API_URL
ENV VITE_APP_API_URL=$VITE_APP_API_URL
RUN npm run build

FROM nginx:latest
COPY --from=build /app/dist /bin/www
# Install OpenSSL to generate SSL certificates
RUN apt-get update && apt-get install -y openssl
# Generate self-signed SSL certificates
RUN mkdir -p /etc/nginx/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/certs/server.key \
    -out /etc/nginx/certs/server.crt \
    -subj "/CN=ft_transcendence"

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
CMD [ "nginx", "-g", "daemon off;" ]