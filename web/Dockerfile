# Use a Node.js base image
FROM node:latest

# Set working directory
WORKDIR /web

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Expose the port the app runs on
EXPOSE 4200

# Run the application
CMD ["ng", "serve", "--host", "0.0.0.0"]
