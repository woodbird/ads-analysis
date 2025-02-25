import React from 'react';
import '../styles/Message.css';

const Message = ({ message }) => {
  const { text, sender, isError } = message;
  
  // 处理消息中的换行
  const formattedText = text.split('\n').map((line, i) => (
    <React.Fragment key={i}>
      {line}
      {i < text.split('\n').length - 1 && <br />}
    </React.Fragment>
  ));

  return (
    <div className={`message ${sender}-message ${isError ? 'error-message' : ''}`}>
      <div className="message-avatar">
        {sender === 'user' ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        <div className="message-text">{formattedText}</div>
      </div>
    </div>
  );
};

export default Message;
