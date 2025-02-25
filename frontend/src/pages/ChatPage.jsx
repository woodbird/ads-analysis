import React, { useState, useRef, useEffect } from 'react';
import ChatInput from '../components/ChatInput';
import MessageList from '../components/MessageList';
import { sendMessage } from '../api/chatService';
import '../styles/ChatPage.css';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    // 添加用户消息
    const userMessage = {
      id: Date.now(),
      text,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      // 调用API发送消息
      const response = await sendMessage(text);
      
      // 添加AI回复
      const aiMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'ai',
        timestamp: new Date().toISOString(),
      };
      
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('发送消息失败:', error);
      
      // 添加错误消息
      const errorMessage = {
        id: Date.now() + 1,
        text: '抱歉，发生了错误，请稍后再试。',
        sender: 'ai',
        timestamp: new Date().toISOString(),
        isError: true,
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-container glassmorphism">
        <div className="chat-header">
          <h2>广告账户分析助手</h2>
          <p>询问您的广告账户表现和优化建议</p>
        </div>
        
        <MessageList messages={messages} />
        <div ref={messagesEndRef} />
        
        <ChatInput onSendMessage={handleSendMessage} disabled={loading} />
      </div>
    </div>
  );
};

export default ChatPage;
