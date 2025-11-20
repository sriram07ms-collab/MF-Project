'use client'

import { useState, useRef, useEffect } from 'react'
import MessageBubble from './MessageBubble'
import ChatInput from './ChatInput'
import { queryAPI } from '@/lib/api'

export interface Message {
  id: string
  text: string
  isUser: boolean
  source?: string
  lastUpdated?: string
  isRefusal?: boolean
  educationalLink?: string
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  // Listen for example question clicks
  useEffect(() => {
    const handleExampleQuestion = (event: CustomEvent) => {
      handleSendMessage(event.detail)
    }
    
    window.addEventListener('exampleQuestion', handleExampleQuestion as EventListener)
    return () => {
      window.removeEventListener('exampleQuestion', handleExampleQuestion as EventListener)
    }
  }, [])

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: text.trim(),
      isUser: true
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await queryAPI(text.trim())
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.answer,
        isUser: false,
        source: response.source,
        lastUpdated: response.lastUpdated,
        isRefusal: response.isRefusal,
        educationalLink: response.educationalLink
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again later.',
        isUser: false
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-gray-800 rounded-2xl shadow-2xl border border-gray-700 overflow-hidden flex flex-col" style={{ height: '600px' }}>
      {/* Chat Header */}
      <div className="bg-gray-900 px-6 py-4 border-b border-gray-700">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 bg-groww-teal rounded-full"></div>
          <h2 className="text-lg font-semibold text-white">Chat Assistant</h2>
        </div>
        <p className="text-xs text-gray-400 mt-1">No PAN/Aadhaar/OTP required</p>
      </div>

      {/* Messages Container */}
      <div 
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto p-6 space-y-4"
      >
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p>Start a conversation by asking a question</p>
            <p className="text-sm mt-2">or click an example question above</p>
          </div>
        )}
        
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <div className="flex items-center gap-2 text-gray-400">
            <div className="w-2 h-2 bg-groww-teal rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-groww-teal rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-groww-teal rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
            <span className="ml-2 text-sm">Thinking...</span>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-700 p-4 bg-gray-900">
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  )
}



