'use client'

import { useState, useRef, useEffect } from 'react'
import ChatInterface from '@/components/ChatInterface'
import WelcomeCard from '@/components/WelcomeCard'

export default function Home() {
  return (
    <main className="min-h-screen bg-groww-navy flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        <WelcomeCard />
        <ChatInterface />
      </div>
      <footer className="mt-8 text-center text-sm text-groww-gray">
        <p>Data sourced from Nippon India Mutual Fund websites</p>
        <p className="mt-2">MUTUAL FUND INVESTMENTS ARE SUBJECT TO MARKET RISKS. Facts-only. No investment advice.</p>
      </footer>
    </main>
  )
}
