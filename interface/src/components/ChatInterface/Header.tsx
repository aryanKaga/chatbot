import React from 'react';
import { MoreVertical } from 'lucide-react';

interface HeaderProps {
  isVisible: boolean;
}

export default function Header({ isVisible }: HeaderProps) {
  return (
    <div className={`fixed top-0 left-0 right-0 z-10 flex items-center justify-between p-6 bg-black border-b border-red-500 transition-transform duration-300 ${isVisible ? 'translate-y-0' : '-translate-y-full'}`}>
      {/* Logo */}
      <div className="flex items-center space-x-3">
        <img src="/src/assets/woxsen.svg" alt="Woxsen Logo" className="h-16" />
      </div>
      <div className="flex items-center space-x-4">
        <img src="/src/assets/bot.svg" alt="Bot Logo" className="h-16" />
      </div>
    </div>
  );
}
