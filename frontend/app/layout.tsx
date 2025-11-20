import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Facts-Only MF Assistant | Nippon India',
  description: 'Get factual information about Nippon India Mutual Fund schemes. Facts-only. No investment advice.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
