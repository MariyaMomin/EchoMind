import React, { useState, useRef, useEffect } from 'react';
import { Send, AlertCircle, Phone, MessageCircle, CheckCircle2, AlertTriangle } from 'lucide-react';
import { sendQuery } from '../services/api';
import EmergencyBanner from './EmergencyBanner';
import MessageBubble from './MessageBubble';
import ResourceCard from './ResourceCard';

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      type: 'system',
      content: "Hello, I'm EchoMind 💙 I'm here to help you find mental wellness resources and support. What's on your mind today?",
      timestamp: new Date(),
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [showEmergencyBanner, setShowEmergencyBanner] = useState(false);
  const [emergencyContacts, setEmergencyContacts] = useState([]);
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim() || isLoading) return;

    const userMessage = {
      id: `user_${Date.now()}`,
      type: 'user',
      content: inputText.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Call API
      const response = await sendQuery({
        query: userMessage.content,
        session_id: sessionId,
        user_location: null, // Could be added via geolocation
        preferences: {}
      });

      // Handle emergency banner
      if (response.urgency_level === 'critical' || response.urgency_level === 'high') {
        setShowEmergencyBanner(true);
        setEmergencyContacts(response.emergency_contacts || []);
      }

      // Add AI response
      const aiMessage = {
        id: response.response_id,
        type: 'assistant',
        content: response.synthesized_answer?.answer || "I'm having trouble processing that right now.",
        urgency: response.urgency_level,
        confidence: response.synthesized_answer?.confidence,
        confidenceScore: response.synthesized_answer?.confidence_score,
        sources: response.synthesized_answer?.sources || [],
        keyPoints: response.synthesized_answer?.key_points || [],
        relatedTopics: response.synthesized_answer?.related_topics || [],
        resources: response.recommended_resources || [],
        nextSteps: response.next_steps || [],
        timestamp: new Date(response.timestamp),
      };

      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = {
        id: `error_${Date.now()}`,
        type: 'error',
        content: 'I apologize, but I encountered an issue. Please try again or contact support if the problem persists.',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const getConfidenceBadge = (confidence) => {
    const badges = {
      high: { color: 'bg-wellness-green', icon: CheckCircle2, text: 'High Confidence' },
      medium: { color: 'bg-wellness-yellow', icon: AlertTriangle, text: 'Medium Confidence' },
      low: { color: 'bg-wellness-red', icon: AlertCircle, text: 'Low Confidence' }
    };
    
    const badge = badges[confidence] || badges.medium;
    const Icon = badge.icon;
    
    return (
      <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs text-white ${badge.color}`}>
        <Icon size={12} />
        {badge.text}
      </div>
    );
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3 shadow-sm">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center">
              <MessageCircle className="text-white" size={24} />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-800">EchoMind</h1>
              <p className="text-xs text-gray-500">Mental Wellness Support</p>
            </div>
          </div>
          <Phone className="text-primary-500 cursor-pointer hover:text-primary-600" size={24} />
        </div>
      </header>

      {/* Emergency Banner */}
      {showEmergencyBanner && (
        <EmergencyBanner 
          contacts={emergencyContacts}
          onClose={() => setShowEmergencyBanner(false)}
        />
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.map((message) => (
            <div key={message.id}>
              <MessageBubble message={message} getConfidenceBadge={getConfidenceBadge} />
              
              {/* Show resources if available */}
              {message.type === 'assistant' && message.resources?.length > 0 && (
                <div className="mt-4 space-y-2">
                  <h3 className="text-sm font-semibold text-gray-700">Recommended Resources:</h3>
                  <div className="grid gap-2">
                    {message.resources.map((resource, idx) => (
                      <ResourceCard key={idx} resource={resource} />
                    ))}
                  </div>
                </div>
              )}

              {/* Show next steps if available */}
              {message.type === 'assistant' && message.nextSteps?.length > 0 && (
                <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="text-sm font-semibold text-blue-900 mb-2">Next Steps:</h3>
                  <ul className="space-y-1">
                    {message.nextSteps.map((step, idx) => (
                      <li key={idx} className="text-sm text-blue-800 flex items-start gap-2">
                        <span className="text-blue-500 mt-0.5">•</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-center gap-2 text-gray-500">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
              <span className="text-sm">EchoMind is thinking...</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-4 py-4 shadow-lg">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSendMessage} className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your message here..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!inputText.trim() || isLoading}
              className="bg-primary-500 text-white px-6 py-3 rounded-full hover:bg-primary-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2 font-medium"
            >
              <Send size={20} />
              <span className="hidden sm:inline">Send</span>
            </button>
          </form>
          <p className="text-xs text-gray-500 text-center mt-2">
            Confidential • Available 24/7 • Your well-being matters
          </p>
        </div>
      </div>
    </div>
  );
};

export default Chat;
