'use client'

import { Message } from './ChatInterface'

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  if (message.isUser) {
    return (
      <div className="flex justify-end">
        <div className="bg-groww-teal text-white rounded-2xl rounded-tr-sm px-5 py-3 max-w-[80%] shadow-lg">
          <p className="text-sm leading-relaxed">{message.text}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <div className="bg-gray-700 text-gray-100 rounded-2xl rounded-tl-sm px-5 py-3 max-w-[80%] shadow-lg">
        <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
        
        {message.isRefusal && message.educationalLink && (
          <a
            href={message.educationalLink}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-3 inline-block text-xs text-groww-teal hover:underline"
          >
            Learn more about investor education →
          </a>
        )}
        
        {message.source && (
          <div className="mt-3 pt-3 border-t border-gray-600">
            <a
              href={message.source}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-groww-teal hover:underline flex items-center gap-1"
            >
              <span>📎</span>
              <span>View source</span>
            </a>
            {message.lastUpdated && (
              <p className="text-xs text-gray-400 mt-1">
                Last updated from sources: {message.lastUpdated}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}



