import React from 'react';
import './UserHeader.css';

const UserHeader = ({ userId, connected, recipientId, reconnecting }) => {
  let connectionStatus;
  let statusClass;
  
  if (connected) {
    connectionStatus = 'Connected';
    statusClass = 'connected';
  } else if (reconnecting) {
    connectionStatus = 'Reconnecting...';
    statusClass = 'reconnecting';
  } else {
    connectionStatus = 'Disconnected';
    statusClass = 'disconnected';
  }

  return (
    <div className="user-header">
      <div className="user-info">
        <h2>User {userId}</h2>
        <div className={`connection-status ${statusClass}`}>
          {connectionStatus}
        </div>
      </div>
      <div className="recipient-info">
        <span>Chatting with: User {recipientId}</span>
      </div>
    </div>
  );
};

export default UserHeader;
