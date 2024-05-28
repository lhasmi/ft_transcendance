# Use the official Node.js image from the Docker Hub
FROM node:18

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (if present)
COPY package.json ./
COPY package-lock.json* ./

# Clean npm cache and remove node_modules if they exist
RUN npm cache clean --force && rm -rf node_modules

# Ensure no npm credentials are used and use the default registry
RUN npm config set registry https://registry.npmjs.org/ && npm config delete _auth && npm config delete username && npm config delete _password && npm config delete email && npm config delete always-auth

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 5173

# Set the HOST environment variable
ENV HOST=0.0.0.0

# Start the application
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
