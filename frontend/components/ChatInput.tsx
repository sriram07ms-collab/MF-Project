'use client'

import { useState, KeyboardEvent } from 'react'

interface ChatInputProps {
  onSend: (message: string) => void
  disabled?: boolean
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input)
      setInput('')
    }
  }

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex items-end gap-3">
      <div className="flex-1 relative">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about expense ratio, exit load, minimum SIP, lock-in, riskometer, benchmark..."
          disabled={disabled}
          className="w-full bg-gray-800 text-white placeholder-gray-500 rounded-xl px-4 py-3 pr-12 resize-none focus:outline-none focus:ring-2 focus:ring-groww-teal border border-gray-700 disabled:opacity-50"
          rows={1}
          style={{ minHeight: '48px', maxHeight: '120px' }}
        />
        <div className="absolute right-3 bottom-3 text-xs text-gray-500">
          Press Enter to send
        </div>
      </div>
      <button
        onClick={handleSend}
        disabled={!input.trim() || disabled}
        className="bg-groww-teal hover:bg-groww-teal-dark disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl px-6 py-3 font-medium transition-colors shadow-lg"
      >
        Send
      </button>
    </div>
  )
}



