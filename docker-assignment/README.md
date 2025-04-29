# Localhost Chat Application

A real-time chat application using Docker and WebSockets that simulates communication between two users on a localhost environment.

## Architecture

- **Frontend**: React.js
- **Backend**: Python WebSocket server with FastAPI
- **Orchestration**: Docker Compose

## Features

- Real-time messaging using WebSockets
- Containerized applications with Docker
- Separation of concerns between frontend and backend
- Simple and intuitive chat interface

## Directory Structure

```
chat-app/
├── frontend/           # React application
│   ├── Dockerfile
│   └── src/            # React components and styling
├── backend/            # Python WebSocket server 
│   ├── Dockerfile
│   └── server.py       # FastAPI WebSocket implementation
├── docker-compose.yml  # Container orchestration
└── README.md           # Project documentation
```

## How to Run

### Prerequisites

- Docker and Docker Compose installed on your machine

### Steps to Run

1. Clone this repository
2. Navigate to the project directory
3. Run the following command:

```
docker-compose up --build
```

### Access the Application

- User A: http://localhost:3000
- User B: http://localhost:3001
- WebSocket Server: ws://localhost:5000

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

