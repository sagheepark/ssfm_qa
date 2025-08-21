'use client';

import { useState } from 'react';
import { EvaluationScores } from '@/lib/types';

interface EvaluationFormProps {
  onSubmit: (scores: EvaluationScores, comment?: string) => void;
  isSubmitting?: boolean;
}

export default function EvaluationForm({ onSubmit, isSubmitting = false }: EvaluationFormProps) {
  const [scores, setScores] = useState<EvaluationScores>({
    quality: 0,
    emotion: 0,
    similarity: 0
  });
  const [comment, setComment] = useState('');

  const handleScoreChange = (dimension: keyof EvaluationScores, value: number) => {
    setScores(prev => ({
      ...prev,
      [dimension]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (scores.quality > 0 && scores.emotion > 0 && scores.similarity > 0) {
      onSubmit(scores, comment || undefined);
    }
  };

  const isFormValid = scores.quality > 0 && scores.emotion > 0 && scores.similarity > 0;

  const ScaleButtons = ({ 
    dimension, 
    label, 
    description 
  }: { 
    dimension: keyof EvaluationScores; 
    label: string;
    description: string;
  }) => (
    <div className="space-y-2">
      <div>
        <h3 className="font-semibold text-gray-900">{label}</h3>
        <p className="text-sm text-gray-600">{description}</p>
      </div>
      <div className="flex space-x-1">
        {[1, 2, 3, 4, 5, 6, 7].map((value) => (
          <button
            key={value}
            type="button"
            onClick={() => handleScoreChange(dimension, value)}
            className={`w-10 h-10 rounded-full text-sm font-medium transition-all ${
              scores[dimension] === value
                ? 'bg-blue-600 text-white ring-2 ring-blue-600 ring-offset-2'
                : scores[dimension] > 0 && scores[dimension] !== value
                ? 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                : 'bg-white border-2 border-gray-300 text-gray-700 hover:border-blue-400 hover:bg-blue-50'
            }`}
          >
            {value}
          </button>
        ))}
      </div>
      <div className="flex justify-between text-xs text-gray-500">
        <span>Poor (1)</span>
        <span>Excellent (7)</span>
      </div>
    </div>
  );

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Rate This Sample</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <ScaleButtons
          dimension="quality"
          label="Quality"
          description="Overall audio quality and technical completeness"
        />
        
        <ScaleButtons
          dimension="emotion"
          label="Emotion Expression"
          description="How well the intended emotion is expressed"
        />
        
        <ScaleButtons
          dimension="similarity"
          label="Speaker Similarity"
          description="How similar this sounds to the original speaker"
        />

        <div className="space-y-2">
          <label htmlFor="comment" className="block font-semibold text-gray-900">
            Comments (Optional)
          </label>
          <textarea
            id="comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Any additional observations..."
            rows={3}
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <button
          type="submit"
          disabled={!isFormValid || isSubmitting}
          className={`w-full py-3 px-4 rounded-md text-white font-medium transition-colors ${
            isFormValid && !isSubmitting
              ? 'bg-blue-600 hover:bg-blue-700'
              : 'bg-gray-400 cursor-not-allowed'
          }`}
        >
          {isSubmitting ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Submitting...</span>
            </div>
          ) : (
            'Submit Rating'
          )}
        </button>
      </form>
    </div>
  );
}