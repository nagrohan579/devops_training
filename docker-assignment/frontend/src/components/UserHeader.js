import React from 'react';
import './UserHeader.css';

const UserHeader = ({ userId, connected, recipientId }) => {
  return (
    <div className="user-header">
      <div className="user-info">
        <h2>User {userId}</h2>
        <div className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? 'Connected' : 'Disconnected'}
        </div>
      </div>
      <div className="recipient-info">
        <span>Chatting with: User {recipientId}</span>
      </div>
    </div>
  );
};

export default UserHeader;
