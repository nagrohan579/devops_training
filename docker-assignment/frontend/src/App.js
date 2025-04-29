import React, { useState, useEffect } from 'react';
import './App.css';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import UserHeader from './components/UserHeader';

function App() {
  const [messages, setMessages] = useState([]);
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [userId, setUserId] = useState('');
  const [recipientId, setRecipientId] = useState('');

  useEffect(() => {
    // Get userId from environment variable
    const id = process.env.REACT_APP_USER_ID || window.USER_ID || 'Unknown';
    setUserId(id);
    
    // Default recipient is the other user
    setRecipientId(id === 'A' ? 'B' : 'A');
    
    // Get backend host - use 'backend' when in Docker, fallback to localhost for development
    const backendHost = process.env.REACT_APP_BACKEND_HOST || 'backend';
    
    // Connect to WebSocket server using the backend service name in Docker network
    const ws = new WebSocket(`ws://${backendHost}:5000/ws/${id}`);
    
    ws.onopen = () => {
      console.log('WebSocket Connected');
      setConnected(true);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages(prevMessages => [...prevMessages, {
        from: data.from,
        text: data.text,
        timestamp: data.timestamp
      }]);
    };
    
    ws.onclose = () => {
      console.log('WebSocket Disconnected');
      setConnected(false);
    };
    
    setSocket(ws);
    
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  const sendMessage = (text) => {
    if (socket && connected && text.trim()) {
      const messageData = {
        to: recipientId,
        text,
        timestamp: new Date().toISOString()
      };
      
      socket.send(JSON.stringify(messageData));
      
      // Add message to local state
      setMessages(prevMessages => [...prevMessages, {
        from: userId,
        text,
        timestamp: messageData.timestamp
      }]);
    }
  };

  return (
    <div className="App">
      <UserHeader userId={userId} connected={connected} recipientId={recipientId} />
      <ChatWindow messages={messages} userId={userId} />
      <MessageInput sendMessage={sendMessage} />
    </div>
  );
}

export default App;
