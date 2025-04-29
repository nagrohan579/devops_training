#!/usr/bin/env python3
import json
import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store active connections
active_connections = {}


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)
            logger.info(f"Message sent to {user_id}")
        else:
            logger.warning(f"Cannot send message to {user_id}: user not connected")

    async def broadcast(self, message: str, exclude_user: str = None):
        for user_id, connection in self.active_connections.items():
            if exclude_user != user_id:  # Don't send to the sender
                await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return {"status": "WebSocket server running"}


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Log the received message
            logger.info(f"Received message from {user_id} to {message_data.get('to')}: {message_data.get('text')}")
            
            # Format the message to send
            formatted_message = json.dumps({
                "from": user_id,
                "text": message_data.get("text"),
                "timestamp": message_data.get("timestamp")
            })
            
            # Send to the recipient
            recipient = message_data.get("to")
            if recipient:
                await manager.send_personal_message(formatted_message, recipient)
            else:
                # If no specific recipient, broadcast to all except sender
                await manager.broadcast(formatted_message, exclude_user=user_id)
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        manager.disconnect(user_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
