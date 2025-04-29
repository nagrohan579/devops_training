# Localhost Chat Application

A real-time chat application using Docker and WebSockets that simulates communication between two users on a localhost environment.

## Architecture

This application is fully containerized and orchestrated using Docker Compose. It consists of three main services:

- **FrontendA**: React.js app for User A (exposed on port 3000)
- **FrontendB**: React.js app for User B (exposed on port 3001)
- **Backend**: Python FastAPI WebSocket server (exposed on port 5000)

All services are defined in `docker-compose.yml` and communicate over a Docker network. The frontend containers connect to the backend using the Docker service name (`backend`) as the host, ensuring reliable service discovery within the Docker network.

### System Diagram

![Chat App Architecture](images/chat-app-diagram.jpg)

- Each frontend container is a separate instance of the same React app, configured via environment variables to represent User A or User B.
- The backend manages WebSocket connections for both users and routes messages accordingly.

## How It Works

- When you start the app with Docker Compose, three containers are created: two for the frontend (User A and User B) and one for the backend.
- Each frontend connects to the backend WebSocket server using the service name `backend` (not `localhost`), e.g., `ws://backend:5000/ws/A` or `ws://backend:5000/ws/B`.
- Messages sent from one user are routed by the backend to the intended recipient in real time.

## Setup & Running Instructions

### Prerequisites
- Docker and Docker Compose installed on your machine

### Steps to Run

1. Clone this repository
2. Navigate to the `docker-assignment` directory
3. Run the following command:

```
docker compose up
```

This will build and start all services. No other setup is required.

### Access the Application
- User A: http://localhost:3000
- User B: http://localhost:3001
- Backend API: ws://localhost:5000

## Directory Structure

```
docker-assignment/
├── frontend/           # React application
│   ├── Dockerfile
│   └── src/            # React components and styling
├── backend/            # Python WebSocket server 
│   ├── Dockerfile
│   └── server.py       # FastAPI WebSocket implementation
├── docker-compose.yml  # Container orchestration
└── README.md           # Project documentation
```

## Issues Faced

- **Message Delivery Issue**: Initially, messages were only being delivered from User B to User A, but not the other way around. This was because the frontend was trying to access port 5000 on `localhost` inside the container, which does not work since the backend is running as a separate container. The fix was to set the environment variable `REACT_APP_BACKEND_HOST=backend` in the frontend containers, so they connect to the backend using the Docker service name, ensuring proper communication between containers.

## How to Use

1. Open User A's interface in one browser window (http://localhost:3000)
2. Open User B's interface in another browser window (http://localhost:3001)
3. Start sending messages between the two users

## Future Improvements

- Add message persistence using Redis or a database
- Implement user authentication
- Add typing indicators
- Support for image and file sharing

## Running Demo

https://github.com/user-attachments/assets/d38c3358-f6ed-459d-9783-c63dcfffb3dd

