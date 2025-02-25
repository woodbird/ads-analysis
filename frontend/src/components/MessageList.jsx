import React from 'react';
import Message from './Message';
import '../styles/MessageList.css';

const MessageList = ({ messages }) => {
  if (messages.length === 0) {
    return (
      <div className="message-list empty-list">
        <div className="welcome-message">
          <h3>欢迎使用广告账户分析助手</h3>
          <p>您可以询问以下问题：</p>
          <ul>
            <li>我的广告账户最近7天的表现如何？</li>
            <li>我的广告投放效果怎么样？</li>
            <li>有哪些优化建议？</li>
            <li>我的转化成本是否合理？</li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="message-list">
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
    </div>
  );
};

export default MessageList;
