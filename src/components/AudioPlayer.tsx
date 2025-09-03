'use client';

import { useState, useRef, useEffect } from 'react';
import { TTSSample } from '@/lib/types';

interface AudioPlayerProps {
  sample: TTSSample;
  autoPlay?: boolean;
  voiceSet?: 'expressivity_none' | 'expressivity_0.6';
  isReference?: boolean; // Flag to indicate if this is playing a reference file
  simplified?: boolean; // Flag to show simplified UI with only filename and controls
  title?: string; // Optional title to display
  colorScheme?: 'blue' | 'orange'; // Color scheme for buttons and controls
}

export default function AudioPlayer({ sample, autoPlay = false, voiceSet = 'expressivity_none', isReference = false, simplified = false, title, colorScheme = 'blue' }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    if (audioRef.current) {
      const folder = voiceSet === 'expressivity_none' ? 'expressivity_none' : 'expressivity_0.6';
      // Use reference file if isReference flag is true
      const filename = isReference ? sample.reference_file : sample.filename;
      const fullUrl = `/voices_2/${folder}/${filename}`;
      
      console.log('AudioPlayer: Loading audio file:', filename);
      console.log('AudioPlayer: Is reference?', isReference);
      console.log('AudioPlayer: Voice set:', voiceSet);
      console.log('AudioPlayer: Full URL:', fullUrl);
      console.log('AudioPlayer: Sample scale:', sample.scale, typeof sample.scale);
      console.log('AudioPlayer: Sample ID:', sample.id);
      
      // Check if filename matches what it should be based on properties
      const expectedFilename = `${sample.voice_id}_${sample.emotion_value}_${sample.text_type}_scale_${sample.scale}.wav`;
      console.log('AudioPlayer: Expected filename:', expectedFilename);
      console.log('AudioPlayer: Filename matches expected?', sample.filename === expectedFilename);
      if (sample.filename !== expectedFilename) {
        console.warn('🔴 FILENAME MISMATCH DETECTED!');
        console.warn('Actual  :', sample.filename);
        console.warn('Expected:', expectedFilename);
      }
      
      audioRef.current.load();
      setIsLoading(true);
      setHasError(false);
    }
  }, [sample.filename, sample.reference_file, sample.voice_id, sample.text_type, sample.emotion_type, sample.emotion_value, sample.scale, sample.id, voiceSet, isReference]);

  const togglePlay = async () => {
    if (!audioRef.current) return;

    try {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        await audioRef.current.play();
      }
    } catch (error) {
      console.error('Audio playback error:', error);
      setHasError(true);
    }
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
      setIsLoading(false);
      if (autoPlay) {
        audioRef.current.play().catch(() => setHasError(true));
      }
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = parseFloat(e.target.value);
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  if (hasError) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-700 text-sm">
          ⚠️ Audio file not available: {isReference ? sample.reference_file : sample.filename}
        </p>
        <p className="text-yellow-600 text-xs mt-1">
          {isReference ? 'Reference audio (neutral baseline) not found' : 'Target audio file not found'}
        </p>
        <div className="mt-2 text-xs text-gray-500">
          {isReference ? (
            <p><strong>Voice:</strong> {sample.voice_id} | <strong>Text Type:</strong> {sample.text_type} | <strong>Emotion:</strong> {sample.emotion_value} | <strong>Reference (no scale)</strong></p>
          ) : (
            <p><strong>Voice:</strong> {sample.voice_id} | <strong>Emotion:</strong> {sample.emotion_value} | <strong>Scale:</strong> {sample.scale}</p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <audio
        ref={audioRef}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onEnded={() => setIsPlaying(false)}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onError={(e) => {
          const filename = isReference ? sample.reference_file : sample.filename;
          console.error('AudioPlayer: Error loading audio:', filename, e);
          console.error('AudioPlayer: Audio element error:', audioRef.current?.error);
          setHasError(true);
        }}
        preload="metadata"
      >
        <source src={`/voices_2/${voiceSet === 'expressivity_none' ? 'expressivity_none' : 'expressivity_0.6'}/${isReference ? sample.reference_file : sample.filename}`} type="audio/wav" />
        Your browser does not support the audio element.
      </audio>

      <div className="space-y-3">
        {simplified ? (
          <>
            {/* Title */}
            {title && (
              <h3 className={`text-lg font-bold mb-3 ${
                colorScheme === 'blue' ? 'text-blue-800' : 'text-orange-800'
              }`}>
                {title}
              </h3>
            )}
            {/* Simplified - Only Filename */}
            <div className="text-sm text-gray-600">
              <p><strong>File:</strong> {isReference ? sample.reference_file : sample.filename}</p>
            </div>
          </>
        ) : (
          <>
            {/* Full Info Display */}
            <div className="text-sm text-gray-600">
              <p><strong>File:</strong> {isReference ? sample.reference_file : sample.filename}</p>
              <p>
                <strong>Voice:</strong> {sample.voice_id} | 
                <strong>Type:</strong> {sample.text_type} | 
                <strong>Emotion:</strong> {sample.emotion_value} | 
                <strong>Scale:</strong> {sample.scale} | 
                <strong>Method:</strong> {sample.emotion_type === 'emotion_label' ? 'Label' : 'Vector'}
              </p>
            </div>

            {/* Text Content */}
            <div className="bg-gray-50 rounded p-3">
              <p className="text-sm font-medium text-gray-700">Text:</p>
              <p className="text-gray-900">&ldquo;{sample.text}&rdquo;</p>
            </div>
          </>
        )}

        {/* Controls */}
        <div className="flex items-center space-x-3">
          <button
            onClick={togglePlay}
            disabled={isLoading}
            className={`flex items-center justify-center w-10 h-10 disabled:bg-gray-400 text-white rounded-full transition-colors ${
              colorScheme === 'blue' 
                ? 'bg-blue-600 hover:bg-blue-700' 
                : 'bg-orange-600 hover:bg-orange-700'
            }`}
          >
            {isLoading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : isPlaying ? (
              <div className="flex space-x-0.5">
                <div className="w-1 h-4 bg-white"></div>
                <div className="w-1 h-4 bg-white"></div>
              </div>
            ) : (
              <div className="w-0 h-0 border-l-[6px] border-l-white border-y-[4px] border-y-transparent ml-0.5"></div>
            )}
          </button>

          {!isLoading && (
            <>
              <span className="text-xs text-gray-500 min-w-[35px]">
                {formatTime(currentTime)}
              </span>
              <input
                type="range"
                min="0"
                max={duration || 0}
                value={currentTime}
                onChange={handleSeek}
                className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
              <span className="text-xs text-gray-500 min-w-[35px]">
                {formatTime(duration)}
              </span>
            </>
          )}
        </div>
      </div>

      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 16px;
          width: 16px;
          border-radius: 50%;
          background: ${colorScheme === 'blue' ? '#3b82f6' : '#ea580c'};
          cursor: pointer;
        }
        
        .slider::-moz-range-thumb {
          height: 16px;
          width: 16px;
          border-radius: 50%;
          background: ${colorScheme === 'blue' ? '#3b82f6' : '#ea580c'};
          cursor: pointer;
          border: none;
        }
      `}</style>
    </div>
  );
}