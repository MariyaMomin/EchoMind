import React from 'react';
import { Bot, User, Info } from 'lucide-react';
import clsx from 'clsx';

const MessageBubble = ({ message, getConfidenceBadge }) => {
  const isUser = message.type === 'user';
  const isSystem = message.type === 'system';
  const isError = message.type === 'error';

  return (
    <div
      className={clsx(
        'flex gap-3',
        isUser && 'flex-row-reverse',
        (isSystem || isError) && 'justify-center'
      )}
    >
      {/* Avatar */}
      {!isSystem && !isError && (
        <div
          className={clsx(
            'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
            isUser ? 'bg-primary-500' : 'bg-purple-500'
          )}
        >
          {isUser ? <User size={18} className="text-white" /> : <Bot size={18} className="text-white" />}
        </div>
      )}

      {/* Message Content */}
      <div
        className={clsx(
          'max-w-2xl',
          isUser && 'ml-auto'
        )}
      >
        {/* Main bubble */}
        <div
          className={clsx(
            'rounded-2xl px-4 py-3 shadow-sm',
            isUser && 'bg-primary-500 text-white',
            !isUser && !isSystem && !isError && 'bg-white text-gray-800 border border-gray-200',
            isSystem && 'bg-purple-100 text-purple-900 border border-purple-200',
            isError && 'bg-red-100 text-red-900 border border-red-200'
          )}
        >
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          
          {/* Confidence badge for assistant messages */}
          {message.type === 'assistant' && message.confidence && (
            <div className="mt-2">
              {getConfidenceBadge(message.confidence)}
            </div>
          )}

          {/* Key points */}
          {message.keyPoints && message.keyPoints.length > 0 && (
            <div className="mt-3 pt-3 border-t border-gray-200">
              <p className="text-xs font-semibold text-gray-600 mb-1">Key Points:</p>
              <ul className="space-y-1">
                {message.keyPoints.map((point, idx) => (
                  <li key={idx} className="text-xs text-gray-700 flex items-start gap-1">
                    <span className="text-primary-500 mt-0.5">•</span>
                    <span>{point}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Sources */}
          {message.sources && message.sources.length > 0 && (
            <div className="mt-3 pt-3 border-t border-gray-200">
              <p className="text-xs font-semibold text-gray-600 mb-1 flex items-center gap-1">
                <Info size={12} />
                Sources:
              </p>
              <div className="space-y-1">
                {message.sources.map((source, idx) => (
                  <div key={idx} className="text-xs">
                    <span className="font-medium text-gray-700">{source.source_name}</span>
                    {source.source_url && (
                      <a
                        href={source.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:underline ml-1"
                      >
                        [Link]
                      </a>
                    )}
                    <span className="text-gray-500 ml-1">
                      (Trust: {(source.trust_score * 100).toFixed(0)}%)
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Timestamp */}
        <p className="text-xs text-gray-400 mt-1 px-2">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </div>
  );
};

export default MessageBubble;
