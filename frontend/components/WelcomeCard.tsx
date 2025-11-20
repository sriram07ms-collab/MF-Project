'use client'

export default function WelcomeCard() {
  const exampleQuestions = [
    "What's the exit load on Nippon India Large Cap Fund?",
    "What is the minimum SIP amount?",
    "How to download capital gains statement?"
  ]

  return (
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-8 mb-6 shadow-2xl border border-gray-700">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-12 h-12 bg-groww-teal rounded-full flex items-center justify-center">
          <span className="text-2xl">💬</span>
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white">Facts-Only MF Assistant</h1>
          <p className="text-sm text-groww-teal">Nippon India Edition</p>
        </div>
      </div>
      
      <p className="text-gray-300 mb-6 leading-relaxed">
        Get factual information about Nippon India Mutual Fund schemes. 
        Every answer includes a citation to official sources.
      </p>
      
      <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mb-6">
        <p className="text-yellow-200 text-sm font-medium">
          ⚠️ Facts-only. No investment advice.
        </p>
      </div>
      
      <div className="space-y-3">
        <p className="text-sm font-medium text-gray-400">Try asking:</p>
        <div className="flex flex-wrap gap-2">
          {exampleQuestions.map((question, idx) => (
            <button
              key={idx}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded-full transition-colors border border-gray-600"
              onClick={() => {
                const event = new CustomEvent('exampleQuestion', { detail: question })
                window.dispatchEvent(event)
              }}
            >
              {question}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}



