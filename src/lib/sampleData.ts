import { TTSSample } from './types';

// Sample data with actual text content from generation
export function generateSamplePool(): TTSSample[] {
  const voices = ['v001', 'v002'];
  const textTypes = ['match', 'neutral', 'opposite'];
  const emotions = ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown'];
  const scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0];
  
  const emotionTexts = {
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
    }
  };

  const samples: TTSSample[] = [];

  voices.forEach(voice => {
    textTypes.forEach(textType => {
      emotions.forEach(emotion => {
        scales.forEach(scale => {
          const filename = `${voice}_${textType}_emo_${emotion}_scale_${scale.toFixed(1)}.wav`;
          const sample: TTSSample = {
            id: filename.replace('.wav', ''),
            filename,
            voice_id: voice,
            text_type: textType,
            emotion_type: 'emotion_label',
            emotion_value: emotion,
            scale,
            text: emotionTexts[emotion as keyof typeof emotionTexts][textType as keyof typeof emotionTexts['angry']],
            category: 'emotion_label'
          };
          samples.push(sample);
        });
      });
    });
  });

  return samples;
}

export function getRandomSamples(count: number = 25): TTSSample[] {
  const allSamples = generateSamplePool();
  const shuffled = [...allSamples].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

export function getSampleMetadata() {
  return {
    total_samples: 216,
    emotion_label_samples: 216,
    emotion_vector_samples: 0, // Currently failed in generation
    voices: ['v001', 'v002'],
    emotions: ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown'],
    text_types: ['match', 'neutral', 'opposite'],
    scales: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
    naming_structure: '{voice_id}_{text_type}_emo_{emotion}_{scale}.wav'
  };
}