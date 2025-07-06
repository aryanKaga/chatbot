import React from 'react';
import { Send } from 'lucide-react';

interface InputAreaProps {
  inputText: string;
  setInputText: (text: string) => void;
  handleSendMessage: () => void;
  handleKeyPress: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  isTyping: boolean;
}

export default function InputArea({
  inputText,
  setInputText,
  handleSendMessage,
  handleKeyPress,
  isTyping,
}: InputAreaProps) {
  return (
    <div className="p-6 bg-black">
      <div className="relative max-w-6xl mx-auto">
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Pass Your Prompt here"
          className="w-full p-4 pr-16 bg-gray-800 border border-gray-600 rounded-2xl text-white placeholder-gray-500 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
          rows="1"
          style={{ minHeight: '60px' }}
        />
        <button
          onClick={handleSendMessage}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 p-2 text-gray-400 hover:text-white disabled:text-gray-600 disabled:cursor-not-allowed transition-colors"
          title="Send message"
        >
          <Send className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
}
