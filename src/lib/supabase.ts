import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types
export interface QASession {
  session_id: string
  user_id?: string
  started_at: string
  completed_at?: string
  samples_data?: any
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
  const { data } = supabase.storage
    .from('tts-audio-samples')
    .getPublicUrl(`voices/${filename}`)
  
  return data.publicUrl
}

export async function saveEvaluation(evaluation: SampleEvaluation) {
  const { data, error } = await supabase
    .from('sample_evaluations')
    .insert([evaluation])
    .select()
  
  if (error) throw error
  return data[0]
}

export async function createSession(sessionData: Partial<QASession>) {
  const { data, error } = await supabase
    .from('qa_sessions')
    .insert([sessionData])
    .select()
  
  if (error) throw error
  return data[0]
}

export async function updateSession(sessionId: string, updates: Partial<QASession>) {
  const { data, error } = await supabase
    .from('qa_sessions')
    .update(updates)
    .eq('session_id', sessionId)
    .select()
  
  if (error) throw error
  return data[0]
}

export async function getSampleMetadata() {
  const { data, error } = await supabase
    .from('sample_metadata')
    .select('*')
  
  if (error) throw error
  return data
}