import React from 'react';
import { marked } from 'marked';
import type { Message } from './type'; // Assuming type.ts exists and exports Message interface

interface MessageItemProps {
  message: Message;
}

export default function MessageItem({ message }: MessageItemProps) {
  return (
    <div className="flex items-start space-x-4">
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
        message.isUser
          ? 'bg-red-500'
          : 'bg-yellow-500'
      }`}>
        <span className={`text-sm ${message.isUser ? 'text-white' : 'text-black font-bold'}`}>
          {message.isUser ? '●' : '📄'}
        </span>
      </div>
      <div className="text-white text-lg leading-relaxed flex-1">
        <div dangerouslySetInnerHTML={{ __html: marked.parse(message.text) }} />
      </div>
    </div>
  );
}
