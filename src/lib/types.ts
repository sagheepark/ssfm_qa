// TTS QA System Types
export interface TTSSample {
  id: string;
  filename: string;
  voice_id: string;
  text_type: string;
  emotion_type: string;
  emotion_value: string;
  scale: number;
  text: string;
  category: string;
}

export interface EvaluationScores {
  quality: number;
  emotion: number;
  similarity: number;
}

export interface EvaluationResult {
  session_id: string;
  sample_id: string;
  scores: EvaluationScores;
  comment?: string;
  timestamp: string;
  duration_ms: number;
}

export interface QASession {
  session_id: string;
  samples: TTSSample[];
  current_index: number;
  results: EvaluationResult[];
  started_at: string;
  completed_at?: string;
  voice_set: 'expressivity_none' | 'expressivity_0.6';
}