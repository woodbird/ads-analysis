import React, { useState } from 'react';
import '../styles/ChatInput.css';

const ChatInput = ({ onSendMessage, disabled }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className="chat-input-container">
      <form onSubmit={handleSubmit} className="chat-form">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="询问您的广告账户表现..."
          disabled={disabled}
          className="chat-input"
        />
        <button 
          type="submit" 
          disabled={disabled || !message.trim()} 
          className="send-button"
        >
          {disabled ? '发送中...' : '发送'}
        </button>
      </form>
    </div>
  );
};

export default ChatInput;
