import React, { useState } from 'react';
import './MessageInput.css';

const MessageInput = ({ sendMessage, disabled }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      sendMessage(message);
      setMessage('');
    }
  };

  return (
    <form className="message-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder={disabled ? "Reconnecting..." : "Type a message..."}
        className="message-input"
        disabled={disabled}
      />
      <button type="submit" className="send-button" disabled={!message.trim() || disabled}>
        Send
      </button>
    </form>
  );
};

export default MessageInput;
