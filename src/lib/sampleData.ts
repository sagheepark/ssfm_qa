import { TTSSample } from './types';

// Helper function to get the reference filename for a given sample
export function getReferenceFilename(sample: TTSSample): string {
  // Reference files are neutral baseline samples with style_label: "normal-1"
  // Same text content as target but with no emotion (neutral baseline)
  return `${sample.voice_id}_${sample.emotion_value}_${sample.text_type}_reference.wav`;
}

// Sample data with actual text content from generation
// Note: voiceSet parameter removed as it's handled at AudioPlayer level, not sample generation
export function generateSamplePool(): TTSSample[] {
  const voices = ['v001', 'v002'];
  const textTypes = ['match', 'neutral', 'opposite'];
  const emotionLabels = ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown'];
  const emotionVectors = ['excited', 'furious', 'terrified', 'fear', 'surprise', 'excitement'];
  const scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0];
  
  const emotionTexts = {
    // Emotion Labels
    angry: {
      match: "I can't believe you broke your promise again after everything we discussed!",
      neutral: "The meeting is scheduled for three o'clock in the conference room.",
      opposite: "Your thoughtfulness and kindness truly made my day so much better."
    },
    sad: {
      match: "I really miss the old days when everyone was still here together.",
      neutral: "The report needs to be submitted by Friday afternoon without fail.",
      opposite: "This is absolutely the best news I've heard all year long!"
    },
    happy: {
      match: "I'm so thrilled about the wonderful surprise party you organized for me!",
      neutral: "Please remember to turn off the lights when you leave the office.",
      opposite: "Everything seems to be going wrong and nothing works out anymore."
    },
    whisper: {
      match: "Don't make any noise, everyone is sleeping in the next room.",
      neutral: "The quarterly financial report shows steady growth in all departments.",
      opposite: "Everyone needs to hear this important announcement right now!"
    },
    toneup: {
      match: "Did you really win the grand prize in the competition?",
      neutral: "The train arrives at platform seven every hour on weekdays.",
      opposite: "Everything is perfectly calm and there's nothing to worry about here."
    },
    tonedown: {
      match: "Let me explain this matter in a very serious and professional manner.",
      neutral: "The document contains information about the new policy changes.",
      opposite: "This is so incredibly exciting and I can barely contain myself!"
    },
    // Emotion Vectors
    excited: {
      match: "We're going on the adventure of a lifetime starting tomorrow morning!",
      neutral: "The temperature today is expected to reach seventy-two degrees.",
      opposite: "I'm too exhausted and drained to do anything at all today."
    },
    furious: {
      match: "This is absolutely unacceptable and I demand an explanation immediately!",
      neutral: "The library closes at eight o'clock on weekday evenings.",
      opposite: "I completely understand your position and I'm not upset at all."
    },
    terrified: {
      match: "Something is moving in the shadows and I don't know what it is!",
      neutral: "The coffee machine is located on the third floor break room.",
      opposite: "I feel completely safe and protected in this wonderful place."
    },
    fear: {
      match: "I'm really scared about what might happen if this goes wrong.",
      neutral: "The new software update will be installed next Tuesday morning.",
      opposite: "I have complete confidence that everything will work out perfectly."
    },
    surprise: {
      match: "Oh my goodness, I never expected to see you here today!",
      neutral: "The parking lot is located behind the main building entrance.",
      opposite: "This is exactly what I predicted would happen all along."
    },
    excitement: {
      match: "I can hardly wait to share this amazing news with everyone!",
      neutral: "Please fill out the form and return it to the front desk.",
      opposite: "This is rather boring and I'm not interested in it at all."
    }
  };

  const samples: TTSSample[] = [];

  // Generate emotion_label samples
  voices.forEach(voice => {
    textTypes.forEach(textType => {
      emotionLabels.forEach(emotion => {
        scales.forEach(scale => {
          const filename = `${voice}_${emotion}_${textType}_scale_${scale.toFixed(1)}.wav`;
          const sample: TTSSample = {
            id: filename.replace('.wav', ''),
            filename,
            voice_id: voice,
            text_type: textType,
            emotion_type: 'emotion_label',
            emotion_value: emotion,
            scale,
            text: emotionTexts[emotion as keyof typeof emotionTexts][textType as keyof typeof emotionTexts['angry']],
            category: 'emotion_label',
            reference_file: getReferenceFilename({
              voice_id: voice,
              text_type: textType,
              emotion_value: emotion
            } as TTSSample)
          };
          samples.push(sample);
        });
      });
    });
  });

  // Generate emotion_vector samples
  voices.forEach(voice => {
    textTypes.forEach(textType => {
      emotionVectors.forEach(emotion => {
        scales.forEach(scale => {
          const filename = `${voice}_${emotion}_${textType}_scale_${scale.toFixed(1)}.wav`;
          const sample: TTSSample = {
            id: filename.replace('.wav', ''),
            filename,
            voice_id: voice,
            text_type: textType,
            emotion_type: 'emotion_vector',
            emotion_value: emotion,
            scale,
            text: emotionTexts[emotion as keyof typeof emotionTexts][textType as keyof typeof emotionTexts['angry']],
            category: 'emotion_vector',
            reference_file: getReferenceFilename({
              voice_id: voice,
              text_type: textType,
              emotion_value: emotion
            } as TTSSample)
          };
          samples.push(sample);
        });
      });
    });
  });

  return samples;
}

export function getRandomSamples(count: number = 25): TTSSample[] {
  // voiceSet is handled at AudioPlayer component level, not at sample generation level
  const allSamples = generateSamplePool();
  const shuffled = [...allSamples].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

export function getSampleMetadata() {
  return {
    total_samples: 432, // 6 emotion_labels + 6 emotion_vectors = 12 emotions × 2 voices × 3 texts × 6 scales
    total_references: 144, // 2 expressivity × 2 voices × 12 emotions × 3 text_types = 144 reference files
    emotion_label_samples: 216, // 6 × 2 × 3 × 6
    emotion_vector_samples: 216, // 6 × 2 × 3 × 6
    voices: ['v001', 'v002'],
    emotion_labels: ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown'],
    emotion_vectors: ['excited', 'furious', 'terrified', 'fear', 'surprise', 'excitement'],
    text_types: ['match', 'neutral', 'opposite'],
    scales: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
    voice_sets: ['expressivity_none', 'expressivity_0.6'],
    naming_structure: {
      target: '{voice_id}_{emotion}_{text_type}_scale_{scale}.wav',
      reference: '{voice_id}_{emotion}_{text_type}_reference.wav'
    },
    reference_description: 'Two sets: expressivity_none (original text) and expressivity_0.6 (text + "|0.6"), both use style_label: "normal-1"'
  };
}