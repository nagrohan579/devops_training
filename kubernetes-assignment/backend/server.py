#!/usr/bin/env python3
import json
import asyncio
import logging
import os
import sys
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis
import pymongo
from pymongo import MongoClient

# Configure logging with more details
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Connect to Redis (with retries for kubernetes startup)
def get_redis_connection():
    redis_host = os.environ.get("REDIS_HOST", "redis")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
    max_retries = 5
    retry_delay = 5  # seconds
    
    logger.info(f"Redis configuration: Host={redis_host}, Port={redis_port}")
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Connecting to Redis at {redis_host}:{redis_port} (attempt {attempt+1}/{max_retries})")
            r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
            r.ping()  # Test connection
            logger.info("Successfully connected to Redis")
            return r
        except redis.ConnectionError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Failed to connect to Redis: {e}. Retrying in {retry_delay} seconds...")
                import time
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to Redis after {max_retries} attempts: {e}")
                raise

# Connect to MongoDB (with retries for kubernetes startup)
def get_mongo_connection():
    mongo_host = os.environ.get("MONGO_HOST", "mongodb")
    mongo_port = int(os.environ.get("MONGO_PORT", 27017))
    max_retries = 5
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Connecting to MongoDB at {mongo_host}:{mongo_port} (attempt {attempt+1}/{max_retries})")
            client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/")
            # Test connection
            client.admin.command('ismaster')
            db = client.chat_app
            messages_collection = db.messages
            logger.info("Successfully connected to MongoDB")
            return messages_collection
        except pymongo.errors.ConnectionFailure as e:
            if attempt < max_retries - 1:
                logger.warning(f"Failed to connect to MongoDB: {e}. Retrying in {retry_delay} seconds...")
                import time
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to MongoDB after {max_retries} attempts: {e}")
                raise

# Initialize Redis and MongoDB connections with proper error handling
try:
    redis_client = get_redis_connection()
    messages_collection = get_mongo_connection()
except Exception as e:
    logger.error(f"Failed to initialize connections: {e}")
    redis_client = None
    messages_collection = None

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        self.pubsub = None
        self.listener_task = None
        self.initialize_redis()
    
    def initialize_redis(self):
        """Initialize Redis PubSub connection with proper error handling"""
        if redis_client:
            try:
                self.pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
                self.pubsub.subscribe('chat_messages')
                logger.info("Successfully subscribed to Redis 'chat_messages' channel")
                # Test Redis pub/sub
                test_message = {
                    'type': 'system',
                    'text': 'Redis pub/sub test message',
                    'timestamp': datetime.now().isoformat()
                }
                redis_client.publish('chat_messages', json.dumps(test_message))
                logger.info(f"Published test message to Redis: {test_message}")
            except Exception as e:
                logger.error(f"Failed to initialize Redis PubSub: {e}")
                self.pubsub = None

    async def start_redis_listener(self):
        """Start the Redis message listener in a proper async context"""
        if not self.listener_task and self.pubsub:
            self.listener_task = asyncio.create_task(self.redis_listener())
            logger.info("Redis listener task started")
        else:
            # If Redis isn't available, periodically retry connecting
            self.listener_task = asyncio.create_task(self.redis_reconnector())
            logger.info("Redis reconnection task started")

    async def redis_reconnector(self):
        """Periodically try to reconnect to Redis if it's not available"""
        while True:
            if not self.pubsub and redis_client:
                logger.info("Attempting to reconnect Redis pubsub...")
                self.initialize_redis()
                if self.pubsub:
                    logger.info("Redis reconnected, starting listener...")
                    asyncio.create_task(self.redis_listener())
                    break
            await asyncio.sleep(10)  # Try reconnecting every 10 seconds

    async def redis_listener(self):
        """Listen for messages from Redis and forward them to the appropriate WebSocket connections"""
        if not self.pubsub:
            logger.error("Redis PubSub not initialized")
            return
            
        logger.info("Starting Redis message listener")
        try:
            while True:
                try:
                    message = self.pubsub.get_message()
                    if message and message['type'] == 'message':
                        logger.info(f"Received message from Redis: {message}")
                        try:
                            data = json.loads(message['data'])
                            
                            # Skip processing if it's a system message
                            if data.get('type') == 'system':
                                logger.info(f"Redis listener received system message: {data.get('text')}")
                                continue

                            user_id = data.get('to')
                            logger.info(f"Processing message to user {user_id}. Active connections: {list(self.active_connections.keys())}")
                            
                            if user_id in self.active_connections:
                                formatted_message = json.dumps({
                                    'from': data.get('from'),
                                    'text': data.get('text'),
                                    'timestamp': data.get('timestamp')
                                })
                                
                                # Use direct WebSocket delivery
                                try:
                                    await self.active_connections[user_id].send_text(formatted_message)
                                    logger.info(f"Message sent to {user_id} successfully via Redis")
                                except Exception as e:
                                    logger.error(f"Error sending message to {user_id}: {str(e)}")
                                    # Handle disconnected socket
                                    if user_id in self.active_connections:
                                        self.disconnect(user_id)
                            else:
                                logger.warning(f"Cannot deliver message: User {user_id} not connected or not found")
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to decode message data: {message['data']}: {str(e)}")
                        except Exception as e:
                            logger.error(f"Error processing Redis message: {str(e)}")
                    
                    # Small delay to prevent CPU overuse
                    await asyncio.sleep(0.01)
                except redis.RedisError as e:
                    logger.error(f"Redis error in listener: {str(e)}")
                    await asyncio.sleep(1)  # Wait a bit on Redis error
                    # Try to reconnect Redis
                    self.initialize_redis()
                    if not self.pubsub:  # If reconnection failed, exit the loop
                        break
                except Exception as e:
                    logger.error(f"Unexpected error in Redis listener: {str(e)}")
                    await asyncio.sleep(1)  # Longer delay on error
        except asyncio.CancelledError:
            logger.info("Redis listener task was cancelled")
        except Exception as e:
            logger.error(f"Redis listener crashed: {str(e)}")
            # Try to restart the listener
            if not self.listener_task.cancelled():
                self.listener_task = asyncio.create_task(self.redis_listener())

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected. Active connections: {list(self.active_connections.keys())}")
        
        # Test WebSocket connection by sending a system message
        try:
            welcome_message = {
                "from": "system", 
                "text": f"Welcome User {user_id}! You are now connected.", 
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send_text(json.dumps(welcome_message))
            logger.info(f"Welcome message sent to {user_id}")
            
            # Notify other users that this user has connected
            other_user_id = 'B' if user_id == 'A' else 'A'
            if other_user_id in self.active_connections:
                notification_message = {
                    "from": "system",
                    "text": f"User {user_id} is now online and ready to chat!",
                    "timestamp": datetime.now().isoformat()
                }
                await self.active_connections[other_user_id].send_text(json.dumps(notification_message))
                logger.info(f"Sent connection notification about User {user_id} to User {other_user_id}")
        except Exception as e:
            logger.error(f"Failed to send welcome message to {user_id}: {str(e)}")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected. Active connections: {list(self.active_connections.keys())}")

    async def send_personal_message(self, message: str, user_id: str):
        """Send a message directly via WebSocket connection"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(message)
                logger.info(f"Direct message sent to {user_id}")
                return True
            except Exception as e:
                logger.error(f"Error sending direct message to {user_id}: {str(e)}")
                # Handle disconnected socket
                self.disconnect(user_id)
                return False
        else:
            logger.warning(f"Cannot send message to {user_id}: user not connected")
            return False

    async def handle_ping(self, websocket: WebSocket, user_id: str):
        """Handle ping message from client"""
        try:
            pong_message = {
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send_text(json.dumps(pong_message))
            logger.debug(f"Sent pong to {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending pong to {user_id}: {str(e)}")
            return False

    async def publish_message(self, message_data):
        """Publish a message to Redis and store in MongoDB"""
        try:
            # Add timestamp if not present
            if 'timestamp' not in message_data:
                message_data['timestamp'] = datetime.now().isoformat()
                
            # Log detailed message info
            from_user = message_data.get('from')
            to_user = message_data.get('to')
            text = message_data.get('text')
            logger.info(f"Processing message: From={from_user}, To={to_user}, Text={text}")
            
            # Store message in MongoDB if available - Fix the MongoDB collection check
            if messages_collection is not None:
                message_record = {
                    'from': from_user,
                    'to': to_user,
                    'text': text,
                    'timestamp': message_data.get('timestamp')
                }
                messages_collection.insert_one(message_record)
                logger.info(f"Message stored in MongoDB: {message_record}")
            
            # Create formatted message for WebSocket delivery
            formatted_message = json.dumps({
                'from': from_user,
                'text': text,
                'timestamp': message_data.get('timestamp')
            })
            
            # First try direct delivery for immediate feedback
            direct_delivery = False
            if to_user in self.active_connections:
                logger.info(f"Attempting direct delivery to {to_user}")
                direct_delivery = await self.send_personal_message(formatted_message, to_user)
                if direct_delivery:
                    logger.info(f"Successfully delivered message directly to {to_user}")
            
            # Also publish to Redis to ensure delivery through subscription system
            if redis_client is not None:
                try:
                    # Use json.dumps to ensure proper serialization
                    redis_message = json.dumps(message_data)
                    redis_client.publish('chat_messages', redis_message)
                    logger.info(f"Message published to Redis: {redis_message}")
                    return True
                except Exception as e:
                    logger.error(f"Failed to publish to Redis: {str(e)}")
                    if not direct_delivery:
                        # If Redis failed and direct delivery also failed, log error
                        logger.error(f"Complete message delivery failure to {to_user}")
                        return False
                    return direct_delivery
            else:
                # If no Redis, rely only on direct delivery result
                if not direct_delivery:
                    logger.error(f"Cannot deliver message to {to_user}: No Redis and WebSocket delivery failed")
                    return False
                return direct_delivery
        except Exception as e:
            logger.error(f"Error in publish_message: {str(e)}")
            return False


manager = ConnectionManager()

# Start the Redis listener when the app starts
@app.on_event("startup")
async def startup_event():
    """Start background tasks when the app starts"""
    logger.info("Application starting up...")
    await manager.start_redis_listener()


@app.get("/")
async def get():
    # Check real Redis connection status
    redis_status = "Connected" if redis_client and manager.pubsub else "Disconnected"
    mongo_status = "Connected" if messages_collection else "Disconnected"
    active_users = list(manager.active_connections.keys())
    
    return {
        "status": "WebSocket server running",
        "redis": redis_status,
        "mongodb": mongo_status,
        "active_users": active_users
    }


# New endpoint to get message history
@app.get("/messages/{user_id}")
async def get_message_history(user_id: str):
    """Get message history for a specific user"""
    try:
        if messages_collection is None:
            logger.error("Cannot retrieve message history: MongoDB not connected")
            raise HTTPException(status_code=503, detail="Database not available")
        
        logger.info(f"Retrieving message history for user {user_id}")
        
        # Find all messages where the user is either sender or recipient
        query = {"$or": [{"from": user_id}, {"to": user_id}]}
        
        # Sort by timestamp and limit to most recent 100 messages
        cursor = messages_collection.find(query).sort("timestamp", 1).limit(100)
        
        # Convert to list and format for response
        messages = []
        for msg in cursor:
            # MongoDB ObjectId is not JSON serializable, so we convert it to string
            msg["_id"] = str(msg["_id"])
            messages.append(msg)
        
        logger.info(f"Retrieved {len(messages)} messages for user {user_id}")
        return {"messages": messages}
    except Exception as e:
        logger.error(f"Error retrieving message history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve message history: {str(e)}")


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                
                # Handle ping messages separately
                if message_data.get('type') == 'ping':
                    logger.debug(f"Received ping from {user_id}")
                    await manager.handle_ping(websocket, user_id)
                    continue
                
                # Validate the message format for chat messages
                if 'to' not in message_data or 'text' not in message_data:
                    logger.warning(f"Invalid message format from {user_id}: {data}")
                    continue
                
                # Confirm the sender is correctly identified
                to_user = message_data.get('to')
                text = message_data.get('text')
                
                # Log the received message
                logger.info(f"Received message from {user_id} to {to_user}: {text}")
                
                # Add sender info to the message
                message_data['from'] = user_id
                
                # Check if recipient is connected
                recipient_connected = to_user in manager.active_connections
                if not recipient_connected:
                    logger.warning(f"Recipient {to_user} is not connected")
                    error_msg = {
                        "from": "system",
                        "text": f"User {to_user} is not currently online. They will receive your message when they connect.",
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send_text(json.dumps(error_msg))
                
                # Publish the message via Redis and MongoDB
                success = await manager.publish_message(message_data)
                
                # Let the sender know if there was a problem that wasn't just the recipient being offline
                if not success and recipient_connected:
                    error_msg = {
                        "from": "system",
                        "text": f"Failed to deliver your message to User {to_user}",
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send_text(json.dumps(error_msg))
                    
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from {user_id}: {data}")
            except Exception as e:
                logger.error(f"Error processing message from {user_id}: {str(e)}")
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user {user_id}")
        manager.disconnect(user_id)
        
        # Notify other users about the disconnection
        other_user_id = 'B' if user_id == 'A' else 'A'
        if other_user_id in manager.active_connections:
            try:
                disconnect_msg = {
                    "from": "system",
                    "text": f"User {user_id} has gone offline.",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.active_connections[other_user_id].send_text(json.dumps(disconnect_msg))
                logger.info(f"Sent disconnect notification about User {user_id} to User {other_user_id}")
            except Exception as e:
                logger.error(f"Error sending disconnect notification: {str(e)}")
    except Exception as e:
        logger.error(f"Error in WebSocket connection for {user_id}: {str(e)}")
        manager.disconnect(user_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
