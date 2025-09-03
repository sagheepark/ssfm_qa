/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable react/no-unescaped-entities */
'use client';

import { useState, useEffect } from 'react';
import { saveEvaluationSmart, createSessionSmart } from '@/lib/supabase';

export default function RecoverPage() {
  const [sessionData, setSessionData] = useState<any>(null);
  const [status, setStatus] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [recoveryStats, setRecoveryStats] = useState({
    total: 0,
    evaluated: 0,
    skipped: 0,
    notEvaluated: 0
  });

  useEffect(() => {
    // Scan for session data on load
    scanForSession();
  }, []);

  const scanForSession = () => {
    try {
      const stored = localStorage.getItem('tts-qa-session');
      if (stored) {
        const session = JSON.parse(stored);
        setSessionData(session);
        
        // Calculate stats
        const evaluated = session.results?.filter((r: any) => r.action !== 'skipped').length || 0;
        const skipped = session.results?.filter((r: any) => r.action === 'skipped').length || 0;
        const notEvaluated = (session.samples?.length || 0) - (session.results?.length || 0);
        
        setRecoveryStats({
          total: session.results?.length || 0,
          evaluated,
          skipped,
          notEvaluated
        });
        
        setStatus('found');
      } else {
        setStatus('not_found');
      }
    } catch (error) {
      console.error('Error scanning localStorage:', error);
      setStatus('error');
    }
  };

  const recoverToDatabase = async () => {
    if (!sessionData || !sessionData.results || sessionData.results.length === 0) {
      alert('No data to recover');
      return;
    }

    setIsSubmitting(true);
    
    try {
      // First create/update session in database
      const sessionDataForDb = {
        session_id: sessionData.session_id,
        started_at: sessionData.started_at,
        completed_at: sessionData.completed_at || new Date().toISOString(),
        samples_data: sessionData.samples
      };
      
      await createSessionSmart(sessionDataForDb);
      console.log('Session recovered to database');

      // Then save all evaluations (excluding skipped ones)
      let submittedCount = 0;
      let failedCount = 0;
      
      for (const evaluation of sessionData.results) {
        // Skip evaluations that were skipped by user
        if (evaluation.action === 'skipped') {
          continue;
        }
        
        try {
          const evaluationData = {
            session_id: evaluation.session_id || sessionData.session_id,
            sample_id: evaluation.sample_id,
            scores: evaluation.scores,
            comment: evaluation.comment,
            timestamp: evaluation.timestamp,
            duration_ms: evaluation.duration_ms || 0
          };
          
          await saveEvaluationSmart(evaluationData, sessionData);
          submittedCount++;
        } catch (error) {
          console.error('Failed to save evaluation:', error);
          failedCount++;
        }
      }
      
      alert(`Recovery complete!\n\nSuccessfully recovered: ${submittedCount} evaluations\nFailed: ${failedCount}\nSkipped: ${recoveryStats.skipped}`);
      
      // Clear localStorage after successful recovery
      if (confirm('Data recovered successfully. Clear localStorage to prevent duplicate submissions?')) {
        localStorage.removeItem('tts-qa-session');
        setSessionData(null);
        setStatus('cleared');
      }
      
    } catch (error) {
      console.error('Recovery failed:', error);
      alert('Failed to recover session. Please try the manual export option.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const exportAsJSON = () => {
    if (!sessionData) return;
    
    const blob = new Blob([JSON.stringify(sessionData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tts_qa_recovery_${sessionData.session_id}_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const exportAsCSV = () => {
    if (!sessionData || !sessionData.results) return;
    
    const evaluations = sessionData.results.filter((r: any) => r.action !== 'skipped');
    
    let csv = 'session_id,sample_id,quality,emotion,similarity,comment,timestamp,duration_ms\n';
    
    evaluations.forEach((evaluation: any) => {
      const scores = evaluation.scores || {};
      const comment = (evaluation.comment || '').replace(/"/g, '""');
      csv += `"${sessionData.session_id}","${evaluation.sample_id}",${scores.quality || ''},${scores.emotion || ''},${scores.similarity || ''},"${comment}","${evaluation.timestamp || ''}",${evaluation.duration_ms || ''}\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tts_qa_recovery_${sessionData.session_id}_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-4">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">🔧 TTS QA Session Recovery</h1>
          
          {/* Status Messages */}
          {status === 'not_found' && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
              <p className="text-yellow-800">No session found in localStorage. You may have already submitted your data or cleared your browser cache.</p>
            </div>
          )}
          
          {status === 'error' && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <p className="text-red-800">Error reading localStorage. Please try refreshing the page.</p>
            </div>
          )}
          
          {status === 'cleared' && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
              <p className="text-green-800">✅ Session recovered and localStorage cleared successfully!</p>
            </div>
          )}
          
          {/* Session Data Display */}
          {sessionData && status === 'found' && (
            <>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <h2 className="text-lg font-semibold text-blue-900 mb-3">📊 Found Session Data</h2>
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p><strong>Session ID:</strong> {sessionData.session_id}</p>
                    <p><strong>Started:</strong> {new Date(sessionData.started_at).toLocaleString()}</p>
                    <p><strong>Voice Set:</strong> {sessionData.voice_set}</p>
                  </div>
                  <div>
                    <p><strong>Progress:</strong> {sessionData.current_index + 1} / {sessionData.samples?.length || 0}</p>
                    <p><strong>Total Evaluations:</strong> {recoveryStats.total}</p>
                    {sessionData.completed_at && (
                      <p><strong>Completed:</strong> {new Date(sessionData.completed_at).toLocaleString()}</p>
                    )}
                  </div>
                </div>
                
                {/* Statistics */}
                <div className="grid grid-cols-3 gap-4 mt-4">
                  <div className="bg-white rounded p-3 text-center">
                    <div className="text-2xl font-bold text-green-600">{recoveryStats.evaluated}</div>
                    <div className="text-xs text-gray-600">Evaluated</div>
                  </div>
                  <div className="bg-white rounded p-3 text-center">
                    <div className="text-2xl font-bold text-orange-600">{recoveryStats.skipped}</div>
                    <div className="text-xs text-gray-600">Skipped</div>
                  </div>
                  <div className="bg-white rounded p-3 text-center">
                    <div className="text-2xl font-bold text-gray-600">{recoveryStats.notEvaluated}</div>
                    <div className="text-xs text-gray-600">Not Evaluated</div>
                  </div>
                </div>
                
                {sessionData.completed_at && (
                  <div className="mt-4 bg-amber-50 border border-amber-200 rounded p-3">
                    <p className="text-amber-800 text-sm">
                      ⚠️ This session was marked as completed but may not have been submitted to the database.
                      Use the recovery options below to save your work.
                    </p>
                  </div>
                )}
              </div>
              
              {/* Recovery Actions */}
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900">Recovery Options:</h3>
                
                <div className="flex flex-wrap gap-3">
                  <button
                    onClick={recoverToDatabase}
                    disabled={isSubmitting || recoveryStats.evaluated === 0}
                    className={`px-6 py-3 font-semibold rounded-lg transition-colors ${
                      isSubmitting || recoveryStats.evaluated === 0
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-green-600 hover:bg-green-700 text-white'
                    }`}
                  >
                    {isSubmitting ? '🔄 Submitting...' : '🚀 Recover to Database'}
                  </button>
                  
                  <button
                    onClick={exportAsJSON}
                    className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
                  >
                    📄 Export as JSON
                  </button>
                  
                  <button
                    onClick={exportAsCSV}
                    disabled={recoveryStats.evaluated === 0}
                    className={`px-6 py-3 font-semibold rounded-lg transition-colors ${
                      recoveryStats.evaluated === 0
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-700 text-white'
                    }`}
                  >
                    📊 Export as CSV
                  </button>
                </div>
                
                <div className="text-sm text-gray-600 mt-4">
                  <p><strong>Option 1:</strong> Click "Recover to Database" to directly submit your evaluations</p>
                  <p><strong>Option 2:</strong> Export your data and send to the research team for manual recovery</p>
                </div>
              </div>
              
              {/* Sample Preview */}
              {sessionData.results && sessionData.results.length > 0 && (
                <div className="mt-6 border-t pt-4">
                  <h4 className="font-semibold text-gray-900 mb-2">Recent Evaluations:</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {sessionData.results.slice(-5).map((result: any, idx: number) => (
                      <li key={idx}>
                        {result.action === 'skipped' ? (
                          <span>{result.sample_id}: <em className="text-orange-600">Skipped</em></span>
                        ) : result.scores ? (
                          <span>{result.sample_id}: Q={result.scores.quality}, E={result.scores.emotion}, S={result.scores.similarity}</span>
                        ) : null}
                      </li>
                    ))}
                    {sessionData.results.length > 5 && (
                      <li><em>... and {sessionData.results.length - 5} more evaluations</em></li>
                    )}
                  </ul>
                </div>
              )}
            </>
          )}
          
          {/* Manual Rescan Button */}
          <div className="mt-6 pt-6 border-t">
            <button
              onClick={scanForSession}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded transition-colors"
            >
              🔍 Rescan localStorage
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}