FROM node:18 as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React application
RUN npm run build

# Use the build as the final image
FROM node:18

WORKDIR /app

# Copy the build from the previous stage
COPY --from=build /app/build ./build

# Set environment variables
ENV PORT=3000

# Expose port 3000
EXPOSE 3000

# Serve the static files using a simple HTTP server
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
