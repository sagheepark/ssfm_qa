'use client';

import { useState, useEffect } from 'react';
import { EvaluationScores, QASession, EvaluationResult } from '@/lib/types';
import { getRandomSamples, getSampleMetadata } from '@/lib/sampleData';
import AudioPlayer from '@/components/AudioPlayer';
import EvaluationForm from '@/components/EvaluationForm';

export default function TTSQAApp() {
  const [session, setSession] = useState<QASession | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Initialize or load session from localStorage
  useEffect(() => {
    const savedSession = localStorage.getItem('tts-qa-session');
    if (savedSession) {
      try {
        const parsed = JSON.parse(savedSession);
        setSession(parsed);
      } catch (error) {
        console.error('Error parsing saved session:', error);
        startNewSession();
      }
    }
  }, []);

  // Save session to localStorage whenever it changes
  useEffect(() => {
    if (session) {
      localStorage.setItem('tts-qa-session', JSON.stringify(session));
    }
  }, [session]);

  const startNewSession = () => {
    const samples = getRandomSamples(25);
    const newSession: QASession = {
      session_id: `session_${Date.now()}`,
      samples,
      current_index: 0,
      results: [],
      started_at: new Date().toISOString()
    };
    setSession(newSession);
    localStorage.removeItem('tts-qa-session'); // Clear any old session
  };

  const submitEvaluation = async (scores: EvaluationScores, comment?: string) => {
    if (!session) return;

    setIsSubmitting(true);
    
    // Simulate API submission delay
    await new Promise(resolve => setTimeout(resolve, 500));

    const result: EvaluationResult = {
      session_id: session.session_id,
      sample_id: session.samples[session.current_index].id,
      scores,
      comment,
      timestamp: new Date().toISOString(),
      duration_ms: Date.now() - new Date(session.started_at).getTime()
    };

    const updatedSession = {
      ...session,
      results: [...session.results, result],
      current_index: session.current_index + 1
    };

    // Mark session as completed if this was the last sample
    if (updatedSession.current_index >= session.samples.length) {
      updatedSession.completed_at = new Date().toISOString();
    }

    setSession(updatedSession);
    setIsSubmitting(false);

    // Save result to downloads (simulating data collection)
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `evaluation_${result.sample_id}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const goToPrevious = () => {
    if (!session || session.current_index === 0) return;
    setSession({
      ...session,
      current_index: session.current_index - 1
    });
  };

  const goToNext = () => {
    if (!session || session.current_index >= session.results.length) return;
    setSession({
      ...session,
      current_index: session.current_index + 1
    });
  };

  const restartSession = () => {
    localStorage.removeItem('tts-qa-session');
    startNewSession();
  };

  if (!session) {
    const metadata = getSampleMetadata();
    
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
          <div className="text-center space-y-6">
            <h1 className="text-3xl font-bold text-gray-900">TTS Quality Assessment</h1>
            
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h2 className="text-lg font-semibold text-blue-900 mb-4">Session Overview</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p><strong>Samples per session:</strong> 25</p>
                  <p><strong>Total sample pool:</strong> {metadata.total_samples}</p>
                  <p><strong>Voices:</strong> {metadata.voices.join(', ')}</p>
                </div>
                <div>
                  <p><strong>Emotions:</strong> {metadata.emotions.length}</p>
                  <p><strong>Text types:</strong> {metadata.text_types.join(', ')}</p>
                  <p><strong>Estimated time:</strong> ~15 minutes</p>
                </div>
              </div>
            </div>

            <div className="space-y-4 text-left">
              <h3 className="font-semibold text-gray-900">Instructions:</h3>
              <ul className="list-disc list-inside space-y-2 text-gray-700">
                <li>You will evaluate 25 randomly selected TTS samples</li>
                <li>Rate each sample on 3 dimensions (1-7 scale)</li>
                <li>Listen to each sample at least once before rating</li>
                <li>Your progress is automatically saved</li>
                <li>Results are downloaded as JSON files for analysis</li>
              </ul>
            </div>

            <button
              onClick={startNewSession}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
            >
              Start New Session
            </button>
          </div>
        </div>
      </div>
    );
  }

  const currentSample = session.samples[session.current_index];
  const isCompleted = session.completed_at !== undefined;
  const hasResult = session.current_index < session.results.length;

  if (isCompleted) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
          <div className="text-center space-y-6">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            
            <h1 className="text-3xl font-bold text-gray-900">Session Completed!</h1>
            
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <h2 className="text-lg font-semibold text-green-900 mb-4">Results Summary</h2>
              <div className="text-sm space-y-2">
                <p><strong>Session ID:</strong> {session.session_id}</p>
                <p><strong>Samples evaluated:</strong> {session.results.length}</p>
                <p><strong>Duration:</strong> {session.completed_at ? new Date(session.completed_at).toLocaleString() : 'Unknown'}</p>
                <p><strong>Results downloaded:</strong> {session.results.length} JSON files</p>
              </div>
            </div>

            <button
              onClick={restartSession}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
            >
              Start New Session
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">TTS Quality Assessment</h1>
            <div className="text-sm text-gray-600">
              Sample {session.current_index + 1} of {session.samples.length}
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="mt-4">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span>{Math.round(((session.current_index) / session.samples.length) * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((session.current_index) / session.samples.length) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Audio Players */}
          <div className="space-y-4">
            {/* Reference Audio */}
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Reference Audio (No Emotion)</h3>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <AudioPlayer 
                  sample={{
                    ...currentSample,
                    filename: `${currentSample.voice_id}_${currentSample.text_type}_reference_${currentSample.emotion_value}.wav`,
                    emotion_value: 'none',
                    emotion_type: 'reference',
                    scale: 1.0,
                    id: `${currentSample.voice_id}_${currentSample.text_type}_reference_${currentSample.emotion_value}`
                  }} 
                />
              </div>
            </div>
            
            {/* Test Sample Audio */}
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Test Sample (With Emotion)</h3>
              <AudioPlayer sample={currentSample} />
            </div>
          </div>

          {/* Evaluation Form */}
          <div>
            {hasResult ? (
              <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                <h2 className="text-xl font-semibold text-green-800 mb-4">✅ Sample Rated</h2>
                <div className="space-y-2 text-sm">
                  <p><strong>Quality:</strong> {session.results[session.current_index].scores.quality}/7</p>
                  <p><strong>Emotion:</strong> {session.results[session.current_index].scores.emotion}/7</p>
                  <p><strong>Similarity:</strong> {session.results[session.current_index].scores.similarity}/7</p>
                  {session.results[session.current_index].comment && (
                    <p><strong>Comment:</strong> {session.results[session.current_index].comment}</p>
                  )}
                </div>
              </div>
            ) : (
              <EvaluationForm 
                onSubmit={submitEvaluation}
                isSubmitting={isSubmitting}
              />
            )}
          </div>
        </div>

        {/* Navigation */}
        <div className="mt-6 flex justify-between">
          <button
            onClick={goToPrevious}
            disabled={session.current_index === 0}
            className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            <span>Previous</span>
          </button>

          <button
            onClick={restartSession}
            className="text-red-600 hover:text-red-800 text-sm"
          >
            Restart Session
          </button>

          <button
            onClick={goToNext}
            disabled={session.current_index >= session.results.length}
            className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span>Next</span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}