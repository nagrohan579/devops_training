FROM node:18

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV PORT=3000

# Expose port 3000
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]
