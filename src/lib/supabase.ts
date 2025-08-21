import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

// Debug environment variables in development
if (typeof window !== 'undefined') {
  console.log('Supabase environment check:', {
    url: supabaseUrl ? 'SET' : 'MISSING',
    key: supabaseAnonKey ? 'SET' : 'MISSING',
    urlValue: supabaseUrl?.substring(0, 20) + '...',
  });
}

// Create supabase client only if environment variables are available
export const supabase = supabaseUrl && supabaseAnonKey 
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null

// Database types
export interface QASession {
  session_id: string
  user_id?: string
  started_at: string
  completed_at?: string
  samples_data?: unknown
  created_at: string
}

export interface SampleEvaluation {
  id?: number
  session_id: string
  sample_id: string
  scores: {
    quality: number
    emotion: number
    similarity: number
  }
  comment?: string
  timestamp?: string
  duration_ms?: number
  // Enhanced for analysis
  evaluator_id?: string        // Track who evaluated (for mixed effects)
  reference_sample_id?: string // Link to reference audio for comparison
  playback_count?: number      // How many times audio was played
  evaluation_order?: number    // Order within session (fatigue effects)
}

export interface SampleMetadata {
  sample_id: string
  filename: string
  voice_id: string
  text_type: string
  emotion_type: string
  emotion_value: string
  scale: number
  text_content: string
  category: string
  audio_url: string
}

// Helper functions
export async function uploadAudioSample(file: File, filename: string) {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  
  const { data, error } = await supabase.storage
    .from('tts-audio-samples')
    .upload(`voices/${filename}`, file, {
      cacheControl: '3600',
      upsert: false
    })
  
  if (error) throw error
  return data
}

export async function getAudioUrl(filename: string): Promise<string> {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  
  const { data } = supabase.storage
    .from('tts-audio-samples')
    .getPublicUrl(`voices/${filename}`)
  
  return data.publicUrl
}

export async function saveEvaluation(evaluation: SampleEvaluation) {
  if (!supabase) {
    throw new Error('Database connection not available. Please contact the administrator.')
  }
  
  console.log('saveEvaluation: Attempting to save:', evaluation);
  
  const { data, error } = await supabase
    .from('sample_evaluations')
    .insert([evaluation])
    .select()
  
  console.log('saveEvaluation: Supabase response:', { data, error });
  
  if (error) {
    console.error('saveEvaluation: Supabase error details:', error);
    throw error;
  }
  
  console.log('saveEvaluation: Success, returning:', data[0]);
  return data[0];
}

export async function createSession(sessionData: Partial<QASession>) {
  if (!supabase) {
    throw new Error('Database connection not available. Please contact the administrator.')
  }
  
  console.log('createSession: Attempting to upsert:', sessionData);
  
  const { data, error } = await supabase
    .from('qa_sessions')
    .upsert([sessionData], { 
      onConflict: 'session_id',
      ignoreDuplicates: false 
    })
    .select()
  
  console.log('createSession: Supabase response:', { data, error });
  
  if (error) {
    console.error('createSession: Supabase error details:', error);
    throw error;
  }
  
  return data[0]
}

export async function updateSession(sessionId: string, updates: Partial<QASession>) {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  
  const { data, error } = await supabase
    .from('qa_sessions')
    .update(updates)
    .eq('session_id', sessionId)
    .select()
  
  if (error) throw error
  return data[0]
}

export async function getSampleMetadata() {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  
  const { data, error } = await supabase
    .from('sample_metadata')
    .select('*')
  
  if (error) throw error
  return data
}