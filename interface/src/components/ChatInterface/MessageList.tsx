import React, { type RefObject } from 'react';
import MessageItem from './MessageItem';
import type { Message } from './type';

interface MessageListProps {
  messages: Message[];
  isTyping: boolean;
  messagesEndRef: RefObject<HTMLDivElement | null>;
}

export default function MessageList({ messages, isTyping, messagesEndRef }: MessageListProps) {
  return (
    <div className="flex-1 flex justify-center items-stretch overflow-y-auto py-8">
      <div className="space-y-6 min-h-full w-[98vw] max-w-5xl mx-auto mt-8" style={{ scrollBehavior: 'smooth' }}>
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <p>start your conversation with woxsen bot iam from school fo technology</p>
          </div>
        ) : (
          messages.map((message) => (
            <MessageItem key={message.id} message={message} />
          ))
        )}

        {isTyping && (
          <div className="flex items-start space-x-4">
            <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-black text-sm font-bold">📄</span>
            </div>
            <div className="text-white text-lg leading-relaxed flex-1">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
