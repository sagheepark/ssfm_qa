'use client';

import { useState, useEffect } from 'react';
import { EvaluationScores, QASession, EvaluationResult } from '@/lib/types';
import { getRandomSamples, getSampleMetadata } from '@/lib/sampleData';
import { saveEvaluationSmart, createSessionSmart, supabase } from '@/lib/supabase';
import AudioPlayer from '@/components/AudioPlayer';
import EvaluationForm from '@/components/EvaluationForm';
import DatabaseConnectionError from '@/components/DatabaseConnectionError';

export default function TTSQAApp() {
  const [session, setSession] = useState<QASession | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // All hooks must be called unconditionally at the top
  // Initialize or load session from localStorage
  useEffect(() => {
    const savedSession = localStorage.getItem('tts-qa-session');
    if (savedSession) {
      try {
        const parsed = JSON.parse(savedSession);
        // Handle legacy sessions without voice_set
        if (!parsed.voice_set) {
          parsed.voice_set = 'expressivity_0.6';
        }
        setSession(parsed);
      } catch (error) {
        console.error('Error parsing saved session:', error);
        localStorage.removeItem('tts-qa-session');
      }
    }
  }, []);

  // Save session to localStorage whenever it changes
  useEffect(() => {
    if (session) {
      localStorage.setItem('tts-qa-session', JSON.stringify(session));
    }
  }, [session]);

  // Check if database connection is available AFTER all hooks
  if (!supabase) {
    return <DatabaseConnectionError />;
  }

  const startNewSession = async (voiceSet: 'expressivity_0.6' = 'expressivity_0.6') => {
    const samples = getRandomSamples(25);
    const newSession: QASession = {
      session_id: `session_${Date.now()}_voices_3_${voiceSet}`, // Add voices_3 identifier
      samples,
      current_index: 0,
      results: [],
      started_at: new Date().toISOString(),
      voice_set: voiceSet
    };
    
    // Create session data outside try block for error logging
    const sessionData = {
      session_id: newSession.session_id,
      started_at: newSession.started_at,
      samples_data: samples,
      experiment_version: 'voices_3', // Add experiment version
      audio_quality: 'hd1' // Add audio quality indicator
    };
    
    try {
      // Create session in Supabase
      await createSessionSmart(sessionData);
      
      setSession(newSession);
      localStorage.removeItem('tts-qa-session'); // Clear any old session
    } catch (error) {
      console.error('Error creating session:', error);
      console.error('Session data that failed:', sessionData);
      console.error('Error details:', error instanceof Error ? error.message : String(error));
      // Fall back to local storage only
      setSession(newSession);
      localStorage.removeItem('tts-qa-session');
    }
  };

  const saveEvaluationLocally = (scores: EvaluationScores, comment?: string) => {
    if (!session) return;

    const result: EvaluationResult = {
      session_id: session.session_id,
      sample_id: session.samples[session.current_index].id,
      scores,
      comment,
      timestamp: new Date().toISOString(),
      duration_ms: Date.now() - new Date(session.started_at).getTime()
    };

    // Update or add the evaluation in the results array
    const updatedResults = [...session.results];
    const existingIndex = updatedResults.findIndex(r => r.sample_id === result.sample_id);
    
    if (existingIndex >= 0) {
      // Update existing evaluation
      updatedResults[existingIndex] = result;
    } else {
      // Add new evaluation
      updatedResults.push(result);
    }

    const updatedSession = {
      ...session,
      results: updatedResults
    };

    setSession(updatedSession);
  };

  const submitAllEvaluations = async () => {
    if (!session || session.results.length === 0) {
      alert('No evaluations to submit');
      return;
    }

    setIsSubmitting(true);
    
    try {
      // First create/update session in database
      const sessionData = {
        session_id: session.session_id,
        started_at: session.started_at,
        completed_at: new Date().toISOString(),
        samples_data: session.samples,
        experiment_version: 'voices_3', // Add V3 identification
        audio_quality: 'hd1', // Add HD1 quality indicator
        voice_set: session.voice_set
      };
      
      await createSessionSmart(sessionData);
      console.log('Session created in database');

      // Then save all evaluations to database (only non-skipped ones)
      for (const evaluation of session.results) {
        // Skip evaluations that were skipped by user
        if (evaluation.action === 'skipped') {
          continue;
        }
        
        const evaluationData = {
          session_id: evaluation.session_id || session.session_id,
          sample_id: evaluation.sample_id,
          scores: evaluation.scores!,
          comment: evaluation.comment,
          timestamp: evaluation.timestamp,
          duration_ms: evaluation.duration_ms || 0
        };
        
        // Pass complete session context for V3 routing
        const sessionContext = {
          voice_set: session.voice_set,
          session_id: session.session_id,
          experiment_version: 'voices_3',
          audio_quality: 'hd1'
        };
        
        await saveEvaluationSmart(evaluationData, sessionContext);
      }
      
      console.log(`Successfully submitted ${session.results.length} evaluations to database`);
      
      // Mark session as completed
      const completedSession = {
        ...session,
        completed_at: new Date().toISOString()
      };
      
      setSession(completedSession);
      alert(`Successfully submitted ${session.results.length} evaluations!`);
      
    } catch (error) {
      console.error('Error submitting evaluations:', error);
      
      let errorMessage = 'Unknown error';
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'object' && error !== null) {
        errorMessage = JSON.stringify(error, null, 2);
      } else {
        errorMessage = String(error);
      }
      
      alert(`Failed to submit evaluations: ${errorMessage}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const goToPrevious = () => {
    if (!session || session.current_index === 0) return;
    setSession({
      ...session,
      current_index: session.current_index - 1
    });
  };

  const goToNext = async () => {
    if (!session) return;
    
    const nextIndex = session.current_index + 1;
    
    // If this is the last sample, auto-submit and mark session as completed
    if (nextIndex >= session.samples.length) {
      // Auto-submit all evaluations before marking complete
      console.log('Last sample reached - auto-submitting evaluations...');
      
      setIsSubmitting(true);
      
      try {
        // First create/update session in database
        const sessionData = {
          session_id: session.session_id,
          started_at: session.started_at,
          completed_at: new Date().toISOString(),
          samples_data: session.samples,
          experiment_version: 'voices_3', // Add V3 identification
          audio_quality: 'hd1', // Add HD1 quality indicator
          voice_set: session.voice_set
        };
        
        await createSessionSmart(sessionData);
        console.log('Session created in database');

        // Then save all evaluations to database (only non-skipped ones)
        let submittedCount = 0;
        for (const evaluation of session.results) {
          // Skip evaluations that were skipped by user
          if (evaluation.action === 'skipped') {
            continue;
          }
          
          const evaluationData = {
            session_id: evaluation.session_id || session.session_id,
            sample_id: evaluation.sample_id,
            scores: evaluation.scores!,
            comment: evaluation.comment,
            timestamp: evaluation.timestamp,
            duration_ms: evaluation.duration_ms || 0
          };
          
          // Pass complete session context for V3 routing
          const sessionContext = {
            voice_set: session.voice_set,
            session_id: session.session_id,
            experiment_version: 'voices_3',
            audio_quality: 'hd1'
          };
          
          await saveEvaluationSmart(evaluationData, sessionContext);
          submittedCount++;
        }
        
        console.log(`Successfully auto-submitted ${submittedCount} evaluations to database`);
        
        // Mark session as completed after successful submission
        setSession({
          ...session,
          completed_at: new Date().toISOString()
        });
      } catch (error) {
        console.error('Failed to auto-submit evaluations:', error);
        alert('Failed to submit evaluations. Please use "Stop & Submit" button to retry.');
      } finally {
        setIsSubmitting(false);
      }
      
      return;
    }
    
    setSession({
      ...session,
      current_index: nextIndex
    });
  };

  const skipCurrentSample = () => {
    if (!session) return;
    
    const currentSample = session.samples[session.current_index];
    
    // Record the skip action
    const skipResult: EvaluationResult = {
      sample_id: currentSample.id,
      timestamp: new Date().toISOString(),
      action: 'skipped',
      skip_reason: 'user_choice',
      scores: null,
      comment: undefined
    };
    
    const updatedResults = [...session.results];
    const existingIndex = updatedResults.findIndex(r => r.sample_id === currentSample.id);
    
    if (existingIndex >= 0) {
      updatedResults[existingIndex] = skipResult;
    } else {
      updatedResults.push(skipResult);
    }
    
    // Move to next sample
    const nextIndex = session.current_index + 1;
    
    if (nextIndex >= session.samples.length) {
      // If this is the last sample, mark session as completed
      setSession({
        ...session,
        results: updatedResults,
        completed_at: new Date().toISOString()
      });
    } else {
      setSession({
        ...session,
        results: updatedResults,
        current_index: nextIndex
      });
    }
  };

  // Helper function to check if current sample has been evaluated
  const getCurrentEvaluation = () => {
    if (!session) return null;
    return session.results.find(r => r.sample_id === session.samples[session.current_index].id);
  };

  // Helper function to check if current sample is fully evaluated
  const isCurrentSampleEvaluated = () => {
    const evaluation = getCurrentEvaluation();
    return evaluation && 
           evaluation.scores &&
           evaluation.scores.quality > 0 && 
           evaluation.scores.emotion > 0 && 
           evaluation.scores.similarity > 0;
  };

  const restartSession = () => {
    localStorage.removeItem('tts-qa-session');
    setSession(null);
    // Force reload to ensure clean state
    window.location.reload();
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
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-900">
                <div className="space-y-1">
                  <p><strong>Samples per session:</strong> 25</p>
                  <p><strong>Total sample pool:</strong> {metadata.total_samples}</p>
                  <p><strong>Voices:</strong> {metadata.voices.join(', ')} (HD1 Quality)</p>
                  <p><strong>Audio Quality:</strong> <span className="text-green-600 font-semibold">HD1 Premium</span></p>
                </div>
                <div className="space-y-1">
                  <p><strong>Emotions:</strong> {metadata.emotion_labels.length + metadata.emotion_vectors.length} types</p>
                  <p><strong>Text types:</strong> {metadata.text_types.join(', ')}</p>
                  <p><strong>Estimated time:</strong> ~15 minutes</p>
                  <p><strong>Dataset:</strong> <span className="text-purple-600 font-semibold">voices_3</span></p>
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

              <div className="bg-amber-50 border border-amber-200 rounded-lg p-6 mb-6">
              <h3 className="font-semibold text-amber-900 mb-3">Ready to Evaluate voices_3 Dataset:</h3>
              <p className="text-sm text-amber-800 mb-4">
                Start evaluating the latest HD1 premium quality voice samples with enhanced expressivity and optimized audio generation.
              </p>
              
              <div className="max-w-md mx-auto">
                <div className="border border-amber-300 rounded-lg p-6 bg-white">
                  <h4 className="font-medium text-gray-900 mb-2">🎵 HD1 Premium Quality Dataset (voices_3)</h4>
                  <p className="text-sm text-gray-600 mb-4">
                    Latest generation voice samples featuring HD1 audio quality, new voice IDs (v001, v002), 
                    and enhanced expressivity controls. All 504 samples ready for evaluation.
                  </p>
                  <button
                    onClick={() => startNewSession('expressivity_0.6')}
                    className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
                  >
                    Start HD1 Quality Evaluation
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const currentSample = session.samples[session.current_index];
  const isCompleted = session.completed_at !== undefined;

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
                <p><strong>Dataset:</strong> <span className="text-purple-600 font-semibold">voices_3 (HD1 Quality)</span></p>
                <p><strong>Voice Set:</strong> {session.voice_set === 'expressivity_0.6' ? 'Enhanced Voices (0.6)' : 'Standard Voices'}</p>
                <p><strong>Samples evaluated:</strong> {session.results.length}</p>
                <p><strong>Duration:</strong> {session.completed_at ? new Date(session.completed_at).toLocaleString() : 'Unknown'}</p>
                <p><strong>Audio Quality:</strong> <span className="text-green-600 font-semibold">HD1 Premium</span></p>
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
            <div>
              <h1 className="text-2xl font-bold text-gray-900">TTS Quality Assessment</h1>
              <p className="text-sm text-gray-600 mt-1 max-w-lg">
                Listen to both audio samples below. The Reference Audio is the neutral baseline. 
                Evaluate how well the Target Audio expresses the intended emotion compared to this neutral baseline.
              </p>
              <div className="mt-2 flex gap-2">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  session.voice_set === 'expressivity_0.6' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-blue-100 text-blue-800'
                }`}>
                  {session.voice_set === 'expressivity_0.6' ? 'Enhanced Voices (0.6)' : 'Standard Voices'}
                </span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  voices_3 Dataset
                </span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                  HD1 Quality
                </span>
              </div>
            </div>
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

        {/* Shared Text Content */}
        <div className="bg-gradient-to-r from-slate-50 to-gray-100 border-2 border-gray-300 rounded-lg p-6 mb-6 shadow-sm">
          <p className="text-lg font-semibold text-gray-800 mb-2">Text:</p>
          <p className="text-gray-900 text-lg font-medium">&ldquo;{currentSample.text}&rdquo;</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Audio Players */}
          <div className="space-y-4">
            {/* Reference Audio - Neutral baseline without emotion */}
            <div>
              <AudioPlayer 
                sample={currentSample}
                voiceSet={session.voice_set}
                isReference={true}
                simplified={true}
                title="Reference Audio (Neutral)"
                colorScheme="blue"
              />
            </div>
            
            {/* Target Sample Audio */}
            <div>
              <AudioPlayer 
                sample={currentSample} 
                voiceSet={session.voice_set}
                simplified={true}
                title={`Target Sample (With ${currentSample.emotion_type === 'emotion_label' ? 'Emotion Label' : 'Emotion Vector'}: ${currentSample.emotion_value}, Scale: ${currentSample.scale})`}
                colorScheme="orange"
              />
            </div>
          </div>

          {/* Evaluation Form */}
          <div>
            <EvaluationForm 
              onSubmit={saveEvaluationLocally}
              initialScores={getCurrentEvaluation()?.scores || undefined}
              initialComment={getCurrentEvaluation()?.comment}
            />
          </div>
        </div>

        {/* Enhanced Navigation */}
        <div className="mt-6 space-y-4">
          {/* Primary Navigation */}
          <div className="flex justify-between items-center">
            <button
              onClick={goToPrevious}
              disabled={session.current_index === 0}
              className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              <span>Previous</span>
            </button>

            <div className="flex space-x-3">
              {/* Skip Button */}
              <button
                onClick={skipCurrentSample}
                disabled={session.current_index >= session.samples.length - 1}
                className={`flex items-center space-x-2 px-4 py-2 font-medium rounded-lg border transition-colors ${
                  session.current_index >= session.samples.length - 1
                    ? 'border-gray-300 text-gray-400 cursor-not-allowed'
                    : 'border-orange-300 text-orange-600 hover:border-orange-400 hover:text-orange-700 hover:bg-orange-50'
                }`}
              >
                <span>Skip</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                </svg>
              </button>

              {/* Primary CTA Next Button */}
              <button
                onClick={goToNext}
                disabled={!isCurrentSampleEvaluated() || isSubmitting}
                className={`flex items-center space-x-2 px-6 py-3 font-semibold rounded-lg transition-colors ${
                  isCurrentSampleEvaluated() && !isSubmitting
                    ? 'bg-blue-600 hover:bg-blue-700 text-white'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                <span>
                  {isSubmitting 
                    ? 'Submitting...' 
                    : session.current_index >= session.samples.length - 1 
                      ? 'Complete & Submit' 
                      : 'Next'}
                </span>
                {!isSubmitting && (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          {/* Separated Control Section */}
          <div className="border-t pt-4">
            <div className="flex justify-between items-center">
              <div className="flex space-x-3">
                <button
                  onClick={restartSession}
                  className="px-3 py-1 text-sm border border-red-300 text-red-600 hover:border-red-400 hover:text-red-700 rounded transition-colors"
                >
                  Reset Session
                </button>
                <button
                  onClick={submitAllEvaluations}
                  disabled={isSubmitting || session.results.length === 0}
                  className={`px-3 py-1 text-sm border rounded transition-colors ${
                    session.results.length > 0 && !isSubmitting
                      ? 'border-gray-400 text-gray-600 hover:border-gray-500 hover:text-gray-700'
                      : 'border-gray-300 text-gray-400 cursor-not-allowed'
                  }`}
                >
                  {isSubmitting ? 'Submitting...' : `Stop & Submit (${session.results.length})`}
                </button>
              </div>

              <div className="text-sm text-gray-600">
                Evaluated: {session.results.length} / {session.samples.length}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}