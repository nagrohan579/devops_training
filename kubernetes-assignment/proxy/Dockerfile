FROM node:18-alpine

WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy the proxy server code
COPY proxy.js ./

# Create directory for static files
RUN mkdir -p public

# Expose the port for the proxy server
EXPOSE 3000

# Command to run the proxy
CMD ["node", "proxy.js"]