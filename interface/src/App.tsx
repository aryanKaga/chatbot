import React from 'react';
import ChatInterface from './components/ChatInterface/ChatInterface';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="app">
      {/* Removed heading and other components */}
      <ChatInterface />
    </div>
  );
};

export default App;
