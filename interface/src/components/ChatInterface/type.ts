export default  interface Thought {
  id: string;
  content: string;
  isExpanded?: boolean;
}

export interface ChatMessage {
  content: string;
  isFinal?: boolean;
}

export interface Message {
  id: number;
  text: string;
  isUser: boolean;
  timestamp: Date;
}
