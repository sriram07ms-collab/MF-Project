export default function NotFound() {
  return (
    <div className="min-h-screen bg-groww-navy flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">404</h1>
        <p className="text-gray-400 mb-8">Page not found</p>
        <a href="/" className="text-groww-teal hover:underline">
          Return to home
        </a>
      </div>
    </div>
  )
}



