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
  voice_set?: 'expressivity_none' | 'expressivity_0.6'  // Support both V2 voice sets
  sample_count?: number
  completion_percentage?: number
}

export interface SampleEvaluationV2 extends SampleEvaluation {
  experiment_version?: string
  voice_set?: 'expressivity_none' | 'expressivity_0.6'  // Support both V2 voice sets
  voice_id?: string           // v001, v002
  emotion_type?: string       // emotion_label, emotion_vector
  emotion_value?: string      // angry, sad, excited, etc.
  text_type?: string          // match, neutral, opposite
  emotion_scale?: number      // 1.0, 1.2, 1.4, 1.6, 1.8, 2.0
}

export interface SampleMetadataV2 extends SampleMetadata {
  reference_file?: string
  experiment_version?: string
  voice_set?: 'expressivity_0.6'
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

// ===== SMART MIGRATION FUNCTIONS =====

// Helper function to detect if we should use v3 tables based on session data
export function shouldUseV3Tables(sessionData?: { voice_set?: string; session_id?: string; experiment_version?: string; audio_quality?: string }): boolean {
  // Check for voices_3 indicators
  if (sessionData?.experiment_version === 'voices_3') return true;
  if (sessionData?.audio_quality === 'hd1') return true;
  if (sessionData?.session_id?.includes('voices_3')) return true;
  
  // For new sessions starting now, use v3 by default
  return true;
}

// Helper function to detect if we should use v2 tables based on session data
export function shouldUseV2Tables(sessionData?: { voice_set?: string; session_id?: string; experiment_version?: string }): boolean {
  // Explicit V2 indicators take precedence
  if (sessionData?.experiment_version === 'voices_2') return true;
  if (sessionData?.session_id?.includes('voices_2')) return true;
  
  // If it should use V3, don't use V2
  if (shouldUseV3Tables(sessionData)) return false;
  
  // Check if voice_set exists and contains voices_2 experiment data
  if (sessionData?.voice_set && !sessionData?.session_id?.includes('voices_3')) {
    return true; // All sessions with voice_set should use v2 (unless explicitly voices_3)
  }
  
  // Check if session_id contains voices_2 indicators
  if (sessionData?.session_id?.includes('expressivity_') && !sessionData?.session_id?.includes('voices_3')) {
    return true;
  }
  
  return false; // Default to V3 now
}

// Smart wrapper functions that route to v1, v2, or v3 based on data
export async function saveEvaluationSmart(evaluation: SampleEvaluation, sessionData?: { voice_set?: 'expressivity_none' | 'expressivity_0.6'; session_id?: string; experiment_version?: string; audio_quality?: string }) {
  const useV3 = shouldUseV3Tables(sessionData);
  const useV2 = shouldUseV2Tables(sessionData);
  
  if (useV3) {
    // Enhance evaluation data for v3
    const enhancedEvaluation: SampleEvaluationV2 = {
      ...evaluation,
      experiment_version: 'voices_3',
      voice_set: 'expressivity_0.6', // voices_3 only supports expressivity_0.6
      // Parse sample_id to extract metadata: {voice}_{emotion}_{text_type}_scale_{scale}
      ...parseSimpleSampleId(evaluation.sample_id)
    };
    
    console.log('Using V3 tables for evaluation:', enhancedEvaluation);
    return await saveEvaluationV3(enhancedEvaluation);
  } else if (useV2) {
    // Enhance evaluation data for v2
    const enhancedEvaluation: SampleEvaluationV2 = {
      ...evaluation,
      experiment_version: 'voices_2',
      voice_set: sessionData?.voice_set || 'expressivity_0.6',
      // Parse sample_id to extract metadata: {voice}_{emotion}_{text_type}_scale_{scale}
      ...parseSimpleSampleId(evaluation.sample_id)
    };
    
    console.log('Using V2 tables for evaluation:', enhancedEvaluation);
    return await saveEvaluationV2(enhancedEvaluation);
  } else {
    console.log('Using V1 tables for evaluation:', evaluation);
    return await saveEvaluation(evaluation);
  }
}

export async function createSessionSmart(sessionData: Partial<QASession> & { voice_set?: 'expressivity_none' | 'expressivity_0.6'; samples?: unknown[]; experiment_version?: string; audio_quality?: string }) {
  const useV3 = shouldUseV3Tables(sessionData);
  const useV2 = shouldUseV2Tables(sessionData);
  
  if (useV3) {
    // Enhance session data for v3
    const enhancedSession: Partial<QASessionV2> = {
      ...sessionData,
      experiment_version: 'voices_3',
      voice_set: 'expressivity_0.6', // voices_3 only supports expressivity_0.6
      sample_count: sessionData.samples?.length || 0
    };
    
    console.log('Using V3 tables for session:', enhancedSession);
    return await createSessionV3(enhancedSession);
  } else if (useV2) {
    // Enhance session data for v2
    const enhancedSession: Partial<QASessionV2> = {
      ...sessionData,
      experiment_version: 'voices_2',
      voice_set: sessionData.voice_set || 'expressivity_0.6',
      sample_count: sessionData.samples?.length || 0
    };
    
    console.log('Using V2 tables for session:', enhancedSession);
    return await createSessionV2(enhancedSession);
  } else {
    console.log('Using V1 tables for session:', sessionData);
    return await createSession(sessionData);
  }
}

export async function updateSessionSmart(sessionId: string, updates: Partial<QASession>, sessionData?: { voice_set?: 'expressivity_none' | 'expressivity_0.6'; session_id?: string; experiment_version?: string; audio_quality?: string }) {
  const useV3 = shouldUseV3Tables(sessionData || { session_id: sessionId });
  const useV2 = shouldUseV2Tables(sessionData || { session_id: sessionId });
  
  if (useV3) {
    return await updateSessionV2(sessionId, updates); // Will use V3 functions when available
  } else if (useV2) {
    return await updateSessionV2(sessionId, updates);
  } else {
    return await updateSession(sessionId, updates);
  }
}

// Helper function to parse sample_id and extract metadata
function parseSimpleSampleId(sampleId: string) {
  // Expected format: {voice}_{emotion}_{text_type}_scale_{scale}
  const parts = sampleId.split('_');
  
  if (parts.length >= 5) {
    const voice_id = parts[0]; // v001, v002
    const emotion_value = parts[1]; // angry, sad, etc.
    const text_type = parts[2]; // match, neutral, opposite
    // parts[3] is "scale" keyword, parts[4] is the actual value
    const emotion_scale = parts[4] ? parseFloat(parts[4]) : 1.0;
    
    // Determine emotion_type based on known patterns
    const emotion_labels = ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown'];
    const emotion_type = emotion_labels.includes(emotion_value) ? 'emotion_label' : 'emotion_vector';
    
    return {
      voice_id,
      emotion_value,
      text_type,
      emotion_scale,
      emotion_type
    };
  }
  
  return {};
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

// ===== VOICES_3 EXPERIMENT FUNCTIONS =====

export async function saveEvaluationV3(evaluation: SampleEvaluationV2) {
  if (!supabase) {
    throw new Error('Database connection not available. Please contact the administrator.')
  }
  
  console.log('saveEvaluationV3: Attempting to save:', evaluation);
  
  // Try V3 table first, fallback to V2 if V3 doesn't exist yet
  let { data, error } = await supabase
    .from('sample_evaluations_v3')
    .insert([evaluation])
    .select()
  
  if (error && error.message.includes('relation') && error.message.includes('does not exist')) {
    console.log('V3 table not found, falling back to V2 table');
    // Fallback to V2 table
    const result = await supabase
      .from('sample_evaluations_v2')
      .insert([evaluation])
      .select()
    data = result.data;
    error = result.error;
  }
  
  console.log('saveEvaluationV3: Supabase response:', { data, error });
  
  if (error) {
    console.error('saveEvaluationV3: Supabase error details:', error);
    throw error;
  }
  
  console.log('saveEvaluationV3: Success, returning:', data[0]);
  return data[0];
}

export async function createSessionV3(sessionData: Partial<QASessionV2>) {
  if (!supabase) {
    throw new Error('Database connection not available. Please contact the administrator.')
  }
  
  console.log('createSessionV3: Attempting to upsert:', sessionData);
  
  // Try V3 table first, fallback to V2 if V3 doesn't exist yet
  let { data, error } = await supabase
    .from('qa_sessions_v3')
    .upsert([sessionData], { 
      onConflict: 'session_id',
      ignoreDuplicates: false 
    })
    .select()
  
  if (error && error.message.includes('relation') && error.message.includes('does not exist')) {
    console.log('V3 table not found, falling back to V2 table');
    // Fallback to V2 table
    const result = await supabase
      .from('qa_sessions_v2')
      .upsert([sessionData], { 
        onConflict: 'session_id',
        ignoreDuplicates: false 
      })
      .select()
    data = result.data;
    error = result.error;
  }
  
  console.log('createSessionV3: Supabase response:', { data, error });
  
  if (error) {
    console.error('createSessionV3: Supabase error details:', error);
    throw error;
  }
  
  return data[0]
}

export async function updateSessionV3(sessionId: string, updates: Partial<QASessionV2>) {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  
  // Try V3 table first, fallback to V2 if V3 doesn't exist yet
  let { data, error } = await supabase
    .from('qa_sessions_v3')
    .update(updates)
    .eq('session_id', sessionId)
    .select()
  
  if (error && error.message.includes('relation') && error.message.includes('does not exist')) {
    console.log('V3 table not found, falling back to V2 table');
    // Fallback to V2 table
    const result = await supabase
      .from('qa_sessions_v2')
      .update(updates)
      .eq('session_id', sessionId)
      .select()
    data = result.data;
    error = result.error;
  }
  
  if (error) throw error
  return data[0]
}