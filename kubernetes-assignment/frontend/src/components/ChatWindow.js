import React, { useRef, useEffect } from 'react';
import './ChatWindow.css';

const ChatWindow = ({ messages, userId, isLoading }) => {
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-window">
      {isLoading ? (
        <div className="loading-indicator">
          <div className="loading-spinner"></div>
          <p>Loading message history...</p>
        </div>
      ) : messages.length === 0 ? (
        <div className="no-messages">No messages yet. Start a conversation!</div>
      ) : (
        messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.from === userId ? 'sent' : 'received'}`}
          >
            <div className="message-bubble">
              <div className="message-text">{message.text}</div>
              <div className="message-time">{formatTime(message.timestamp)}</div>
            </div>
          </div>
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;
