export default function DatabaseConnectionError() {
  return (
    <div className="min-h-screen bg-red-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg border-l-4 border-red-500 p-8">
        <div className="flex items-center mb-6">
          <div className="flex-shrink-0">
            <svg className="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="ml-4">
            <h1 className="text-xl font-bold text-red-800">Database Connection Error</h1>
            <p className="text-red-600">The application cannot connect to the database.</p>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">For Administrators:</h2>
          <p className="text-gray-700 mb-4">
            This error occurs because required environment variables are not configured in the deployment.
          </p>
          
          <div className="space-y-4">
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Required Environment Variables:</h3>
              <div className="bg-gray-100 p-3 rounded font-mono text-sm">
                <div>NEXT_PUBLIC_SUPABASE_URL</div>
                <div>NEXT_PUBLIC_SUPABASE_ANON_KEY</div>
              </div>
            </div>

            <div>
              <h3 className="font-medium text-gray-900 mb-2">Steps to Fix:</h3>
              <ol className="list-decimal list-inside space-y-1 text-gray-700 text-sm">
                <li>Go to your Vercel project dashboard</li>
                <li>Navigate to Settings → Environment Variables</li>
                <li>Add the required environment variables</li>
                <li>Redeploy the application</li>
              </ol>
            </div>
          </div>
        </div>

        <div className="text-center">
          <button 
            onClick={() => window.location.reload()} 
            className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded"
          >
            Retry Connection
          </button>
        </div>
      </div>
    </div>
  );
}