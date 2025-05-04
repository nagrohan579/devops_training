import React, { useState, useEffect, useRef } from 'react';
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
  const [connectionAttempt, setConnectionAttempt] = useState(0);
  const [reconnecting, setReconnecting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  
  // Use refs to keep track of the latest state in useEffect callbacks
  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const isConnectingRef = useRef(false);
  const messagesRef = useRef([]);
  
  // Keep messagesRef in sync with messages state
  useEffect(() => {
    messagesRef.current = messages;
  }, [messages]);
  
  useEffect(() => {
    // Get userId from environment variable or window.USER_ID (injected by proxy)
    const id = process.env.REACT_APP_USER_ID || window.USER_ID || 'Unknown';
    console.log('Setting user ID to:', id);
    setUserId(id);
    
    // Default recipient is the other user
    const recipient = id === 'A' ? 'B' : 'A';
    console.log('Setting recipient ID to:', recipient);
    setRecipientId(recipient);

    // Load message history when component mounts
    fetchMessageHistory(id);
    
    // Create WebSocket connection using same origin as the page
    connectWebSocket(id);
    
    // Cleanup function for when component unmounts
    return () => {
      cleanupWebSocket();
    };
  }, []);
  
  // Function to fetch message history from the backend
  const fetchMessageHistory = async (id) => {
    try {
      setIsLoading(true);
      console.log(`Fetching message history for user ${id}...`);
      
      // Get backend host from window.location
      const protocol = window.location.protocol;
      const host = window.location.host;
      const url = `${protocol}//${host}/messages/${id}`;
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to fetch messages: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log(`Received ${data.messages.length} messages from history`);
      
      // Process the messages and add them to state
      const receivedMessages = data.messages.map(msg => ({
        from: msg.from,
        text: msg.text,
        timestamp: msg.timestamp
      }));
      
      setMessages(receivedMessages);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching message history:', error);
      setIsLoading(false);
    }
  };
  
  useEffect(() => {
    // Reconnect WebSocket when connectionAttempt changes (except for initial value)
    if (connectionAttempt > 0) {
      console.log(`Reconnection attempt #${connectionAttempt}`);
      setReconnecting(true);
      connectWebSocket(userId);
    }
  }, [connectionAttempt, userId]);
  
  const cleanupWebSocket = () => {
    if (socketRef.current) {
      console.log('Cleaning up WebSocket connection');
      
      // Remove all event listeners to prevent memory leaks
      socketRef.current.onopen = null;
      socketRef.current.onclose = null;
      socketRef.current.onerror = null;
      socketRef.current.onmessage = null;
      
      // Close the connection
      socketRef.current.close();
      socketRef.current = null;
    }
    
    // Clear any pending reconnection timeouts
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    setSocket(null);
  };
  
  const connectWebSocket = (id) => {
    // Prevent multiple simultaneous connection attempts
    if (isConnectingRef.current) {
      console.log('Connection attempt already in progress, skipping');
      return;
    }
    
    isConnectingRef.current = true;
    
    // Clean up existing connection
    cleanupWebSocket();
    
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/${id}`;
    
    console.log(`Connecting to WebSocket at: ${wsUrl}`);
    
    try {
      const ws = new WebSocket(wsUrl);
      socketRef.current = ws;
      
      ws.onopen = () => {
        console.log('WebSocket Connected');
        setConnected(true);
        setReconnecting(false);
        isConnectingRef.current = false;
        
        // Add ping interval to keep connection alive
        const pingInterval = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'ping' }));
            console.log('Ping sent to keep connection alive');
          } else {
            clearInterval(pingInterval);
          }
        }, 15000); // Send ping every 15 seconds
        
        // Store ping interval for cleanup
        ws.pingInterval = pingInterval;
      };
      
      ws.onmessage = (event) => {
        console.log('WebSocket message received:', event.data);
        
        try {
          const data = JSON.parse(event.data);
          
          // Ignore ping/pong messages
          if (data.type === 'ping' || data.type === 'pong') {
            console.log('Received ping/pong message');
            return;
          }
          
          // Handle system messages
          if (data.from === 'system') {
            console.log('System message:', data.text);
            return;
          }
          
          console.log('Adding message to state:', data);
          
          // Check if this is a duplicate message we already have
          const isDuplicate = messagesRef.current.some(
            msg => msg.timestamp === data.timestamp && 
                  msg.from === data.from && 
                  msg.text === data.text
          );
          
          if (!isDuplicate) {
            setMessages(prevMessages => [...prevMessages, {
              from: data.from,
              text: data.text,
              timestamp: data.timestamp
            }]);
          } else {
            console.log('Detected duplicate message, ignoring');
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
      
      ws.onclose = (event) => {
        console.log(`WebSocket closed with code ${event.code}, reason: ${event.reason || 'No reason provided'}`);
        setConnected(false);
        isConnectingRef.current = false;
        
        // Clear ping interval
        if (ws.pingInterval) {
          clearInterval(ws.pingInterval);
        }
        
        // Implement reconnection with exponential backoff
        const delay = Math.min(1000 * Math.pow(2, Math.min(connectionAttempt, 6)), 30000);
        console.log(`Will attempt to reconnect in ${delay}ms (attempt ${connectionAttempt + 1})`);
        
        setReconnecting(true);
        reconnectTimeoutRef.current = setTimeout(() => {
          setConnectionAttempt(prev => prev + 1);
        }, delay);
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        isConnectingRef.current = false;
      };
      
      setSocket(ws);
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      isConnectingRef.current = false;
      
      // Try again after a delay
      setReconnecting(true);
      reconnectTimeoutRef.current = setTimeout(() => {
        setConnectionAttempt(prev => prev + 1);
      }, 5000);
    }
  };

  const sendMessage = (text) => {
    if (!text.trim()) return;
    
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      const messageData = {
        to: recipientId,
        text,
        timestamp: new Date().toISOString()
      };
      
      console.log('Sending message:', messageData);
      socketRef.current.send(JSON.stringify(messageData));
      
      // Add message to local state
      setMessages(prevMessages => [...prevMessages, {
        from: userId,
        text,
        timestamp: messageData.timestamp
      }]);
    } else {
      console.warn('Cannot send message: WebSocket not open');
      
      if (!connected) {
        alert('You are currently disconnected. Message could not be sent. Reconnecting...');
        setConnectionAttempt(prev => prev + 1);
      }
    }
  };

  return (
    <div className="App">
      <UserHeader 
        userId={userId} 
        connected={connected} 
        recipientId={recipientId}
        reconnecting={reconnecting}
      />
      <ChatWindow 
        messages={messages} 
        userId={userId} 
        isLoading={isLoading} 
      />
      <MessageInput sendMessage={sendMessage} disabled={!connected} />
    </div>
  );
}

export default App;
