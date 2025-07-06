import React, { useState, useRef, useEffect } from 'react';
import Header from './Header';
import MessageList from './MessageList';
import InputArea from './InputArea';
import type { Message } from './type';
import { Marked } from 'marked';
import * as uuid from 'uuid';

export default function WatsonXChatbot() {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hi, I am Woxsen Bot, I am from School of Technology. Want to Know something about Woxsen?",
      isUser: true,
      timestamp: new Date()
    },
    {
      id: 2,
      text: "As a global university, Woxsen aims to empower its students with a global mind-set through a cutting-edge curriculum, world-class pedagogy, industry connections and international partnerships.",
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const [isHeaderVisible, setIsHeaderVisible] = useState(true);
  const [lastScrollTop, setLastScrollTop] = useState(0);


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleScroll = () => {
    const currentScrollTop = chatContainerRef.current?.scrollTop || 0;

    if (currentScrollTop > lastScrollTop && currentScrollTop > 50) {
      // Scrolling down and scrolled past 50px
      setIsHeaderVisible(false);
    } else {
      // Scrolling up or at the top
      setIsHeaderVisible(true);
    }
    setLastScrollTop(currentScrollTop);
  };

  useEffect(() => {
    const chatContainer = chatContainerRef.current;
    if (chatContainer) {
      chatContainer.addEventListener('scroll', handleScroll);
      return () => {
        chatContainer.removeEventListener('scroll', handleScroll);
      };
    }
  }, [lastScrollTop]);



  useEffect(() => {
    if (!localStorage.getItem('userid')) {
      const userid = uuid.v4();
      localStorage.setItem('userid', userid);
    }
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim() || isTyping) return;

    const userMessage = {
      id: Date.now(),
      text: inputText,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    // Backend URL provided by the user (corrected port)
    const backendUrl = 'http://10.107.29.63:8000';
    const eventSource = new EventSource(`${backendUrl}/chat?question=${encodeURIComponent(inputText)}&userid=${localStorage.getItem('userid')}`);

    let aiResponseText = '';
    const aiMessageId = Date.now() + 1;

    eventSource.onmessage = (event: MessageEvent) => {
      aiResponseText += event.data.replace(/<br>/g, '\n'); // Replace <br> with newline for display
      setMessages(prev => {
        const existingMessageIndex = prev.findIndex(msg => msg.id === aiMessageId);
        if (existingMessageIndex > -1) {
          const updatedMessages = [...prev];
          updatedMessages[existingMessageIndex] = {
            ...updatedMessages[existingMessageIndex],
            text: aiResponseText,
          };
          return updatedMessages;
        } else {
          const aiMessage = {
            id: aiMessageId,
            text: aiResponseText,
            isUser: false,
            timestamp: new Date()
          };
          return [...prev, aiMessage];
        }
      });
    };

    eventSource.onerror = (err) => {
      console.error('EventSource failed:', err);
      eventSource.close();
      setIsTyping(false);
    };

    eventSource.onopen = () => {
      console.log('EventSource connected');
    };

    eventSource.addEventListener('end', () => {
      console.log('Stream ended');
      eventSource.close();
      setIsTyping(false);
    });
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!isTyping) {
        handleSendMessage();
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-black text-white">
      <Header isVisible={isHeaderVisible} />
      <div ref={chatContainerRef} className="flex-1 overflow-y-auto pt-20">
        <MessageList messages={messages} isTyping={isTyping} messagesEndRef={messagesEndRef} />
      </div>
      <InputArea
        inputText={inputText}
        setInputText={setInputText}
        handleSendMessage={handleSendMessage}
        handleKeyPress={handleKeyPress}
        isTyping={isTyping}
      />
    </div>
  );
}
