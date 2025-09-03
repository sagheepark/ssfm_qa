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

// Database types - Original tables
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

// New voices_2 experiment types
export interface QASessionV2 extends QASession {
  experiment_version?: string
  voice_set?: 'expressivity_none' | 'expressivity_0.6'
  sample_count?: number
  completion_percentage?: number
}

export interface SampleEvaluationV2 extends SampleEvaluation {
  experiment_version?: string
  voice_set?: 'expressivity_none' | 'expressivity_0.6'
  voice_id?: string           // v001, v002
  emotion_type?: string       // emotion_label, emotion_vector
  emotion_value?: string      // angry, sad, excited, etc.
  text_type?: string          // match, neutral, opposite
  emotion_scale?: number      // 0.5, 1.0, 1.5, etc.
}

export interface SampleMetadataV2 extends SampleMetadata {
  reference_file?: string
  experiment_version?: string
  voice_set?: 'expressivity_none' | 'expressivity_0.6'
  created_at?: string
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

// ===== VOICES_2 EXPERIMENT FUNCTIONS =====

export async function saveEvaluationV2(evaluation: SampleEvaluationV2) {
  if (!supabase) {
    throw new Error('Database connection not available. Please contact the administrator.')
  }
  
  console.log('saveEvaluationV2: Attempting to save:', evaluation);
  
  const { data, error } = await supabase
    .from('sample_evaluations_v2')
    .insert([evaluation])
    .select()
  
  console.log('saveEvaluationV2: Supabase response:', { data, error });
  
  if (error) {
    console.error('saveEvaluationV2: Supabase error details:', error);
    throw error;
  }
  
  console.log('saveEvaluationV2: Success, returning:', data[0]);
  return data[0];
}

export async function createSessionV2(sessionData: Partial<QASessionV2>) {
  if (!supabase) {
    throw new Error('Database connection not available. Please contact the administrator.')
  }
  
  console.log('createSessionV2: Attempting to upsert:', sessionData);
  
  const { data, error } = await supabase
    .from('qa_sessions_v2')
    .upsert([sessionData], { 
      onConflict: 'session_id',
      ignoreDuplicates: false 
    })
    .select()
  
  console.log('createSessionV2: Supabase response:', { data, error });
  
  if (error) {
    console.error('createSessionV2: Supabase error details:', error);
    throw error;
  }
  
  return data[0]
}

export async function updateSessionV2(sessionId: string, updates: Partial<QASessionV2>) {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  
  const { data, error } = await supabase
    .from('qa_sessions_v2')
    .update(updates)
    .eq('session_id', sessionId)
    .select()
  
  if (error) throw error
  return data[0]
}

export async function getSampleMetadataV2() {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  
  const { data, error } = await supabase
    .from('sample_metadata_v2')
    .select('*')
  
  if (error) throw error
  return data
}

// Upload audio files to voices_2 directory
export async function uploadAudioSampleV2(file: File, filename: string) {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  
  const { data, error } = await supabase.storage
    .from('tts-audio-samples')
    .upload(`voices_2/${filename}`, file, {
      cacheControl: '3600',
      upsert: false
    })
  
  if (error) throw error
  return data
}

// Get audio URL from voices_2 directory
export async function getAudioUrlV2(filename: string): Promise<string> {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  
  const { data } = supabase.storage
    .from('tts-audio-samples')
    .getPublicUrl(`voices_2/${filename}`)
  
  return data.publicUrl
}