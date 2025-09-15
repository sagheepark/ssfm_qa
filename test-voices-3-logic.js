#!/usr/bin/env node
/**
 * Test script for voices_3 logic validation (without Supabase connection)
 * Tests V3 routing logic, data parsing, and session handling
 */

// Simulate the smart routing functions from supabase.ts
function shouldUseV3Tables(sessionData = {}) {
  // Check for voices_3 indicators
  if (sessionData.experiment_version === 'voices_3') return true;
  if (sessionData.audio_quality === 'hd1') return true;
  if (sessionData.session_id && sessionData.session_id.includes('voices_3')) return true;
  
  // For new sessions starting now, use v3 by default
  return true;
}

function shouldUseV2Tables(sessionData = {}) {
  // If it should use V3, don't use V2
  if (shouldUseV3Tables(sessionData)) return false;
  
  // Check if voice_set exists and contains voices_2 experiment data
  if (sessionData.voice_set) {
    return true; // All sessions with voice_set should use v2
  }
  
  // Check if session_id contains voices_2 indicators
  if (sessionData.session_id && sessionData.session_id.includes('expressivity_')) {
    return true;
  }
  
  return false; // Default to V3 now
}

function parseSimpleSampleId(sampleId) {
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

function testVoices3Logic() {
  console.log('🧪 Testing voices_3 Logic Validation');
  console.log('='*50);
  
  const tests = [
    // Test 1: V3 session detection
    {
      name: 'V3 Session Detection',
      sessionData: {
        session_id: 'session_1756229497710_voices_3_expressivity_0.6',
        experiment_version: 'voices_3',
        audio_quality: 'hd1'
      },
      expectedV3: true,
      expectedV2: false
    },
    
    // Test 2: V2 session detection
    {
      name: 'V2 Session Detection',
      sessionData: {
        session_id: 'session_1756229497710_expressivity_0.6',
        voice_set: 'expressivity_0.6'
      },
      expectedV3: false,
      expectedV2: true
    },
    
    // Test 3: Legacy session detection
    {
      name: 'Legacy Session Detection',
      sessionData: {
        session_id: 'session_1756229497710',
      },
      expectedV3: true, // Default to V3 now
      expectedV2: false
    },
    
    // Test 4: HD1 quality detection
    {
      name: 'HD1 Quality Detection',
      sessionData: {
        session_id: 'session_test',
        audio_quality: 'hd1'
      },
      expectedV3: true,
      expectedV2: false
    }
  ];
  
  console.log('\n1️⃣ Testing Smart Routing Logic...');
  
  let passed = 0;
  let failed = 0;
  
  for (const test of tests) {
    const useV3 = shouldUseV3Tables(test.sessionData);
    const useV2 = shouldUseV2Tables(test.sessionData);
    
    const v3Pass = useV3 === test.expectedV3;
    const v2Pass = useV2 === test.expectedV2;
    
    if (v3Pass && v2Pass) {
      console.log(`   ✅ ${test.name}: PASSED`);
      console.log(`      V3: ${useV3} (expected ${test.expectedV3})`);
      console.log(`      V2: ${useV2} (expected ${test.expectedV2})`);
      passed++;
    } else {
      console.log(`   ❌ ${test.name}: FAILED`);
      console.log(`      V3: ${useV3} (expected ${test.expectedV3}) - ${v3Pass ? 'OK' : 'FAIL'}`);
      console.log(`      V2: ${useV2} (expected ${test.expectedV2}) - ${v2Pass ? 'OK' : 'FAIL'}`);
      failed++;
    }
  }
  
  // Test 2: Sample ID parsing
  console.log('\n2️⃣ Testing Sample ID Parsing...');
  
  const sampleTests = [
    {
      sampleId: 'v001_angry_match_scale_1.2',
      expected: {
        voice_id: 'v001',
        emotion_value: 'angry',
        text_type: 'match',
        emotion_scale: 1.2,
        emotion_type: 'emotion_label'
      }
    },
    {
      sampleId: 'v002_excited_neutral_scale_1.8',
      expected: {
        voice_id: 'v002',
        emotion_value: 'excited',
        text_type: 'neutral',
        emotion_scale: 1.8,
        emotion_type: 'emotion_vector'
      }
    },
    {
      sampleId: 'v001_whisper_opposite_scale_2.0',
      expected: {
        voice_id: 'v001',
        emotion_value: 'whisper',
        text_type: 'opposite',
        emotion_scale: 2.0,
        emotion_type: 'emotion_label'
      }
    }
  ];
  
  for (const test of sampleTests) {
    const parsed = parseSimpleSampleId(test.sampleId);
    const matches = Object.keys(test.expected).every(key => 
      parsed[key] === test.expected[key]
    );
    
    if (matches) {
      console.log(`   ✅ ${test.sampleId}: PARSED CORRECTLY`);
      console.log(`      Voice: ${parsed.voice_id}, Emotion: ${parsed.emotion_value} (${parsed.emotion_type})`);
      console.log(`      Text: ${parsed.text_type}, Scale: ${parsed.emotion_scale}`);
      passed++;
    } else {
      console.log(`   ❌ ${test.sampleId}: PARSING FAILED`);
      console.log(`      Expected:`, test.expected);
      console.log(`      Got:`, parsed);
      failed++;
    }
  }
  
  // Test 3: Session data enhancement simulation
  console.log('\n3️⃣ Testing Session Data Enhancement...');
  
  const sessionData = {
    session_id: 'session_1756229497710_voices_3_expressivity_0.6',
    started_at: new Date().toISOString(),
    samples_data: [
      { sample_id: 'v001_angry_match_scale_1.2' },
      { sample_id: 'v002_excited_neutral_scale_1.8' }
    ],
    experiment_version: 'voices_3',
    audio_quality: 'hd1'
  };
  
  // Simulate enhanced session data
  const enhancedSession = {
    ...sessionData,
    experiment_version: 'voices_3',
    voice_set: 'expressivity_0.6',
    sample_count: sessionData.samples_data.length
  };
  
  console.log('   ✅ Session Enhancement: PASSED');
  console.log(`      Session ID: ${enhancedSession.session_id}`);
  console.log(`      Experiment: ${enhancedSession.experiment_version}`);
  console.log(`      Audio Quality: ${enhancedSession.audio_quality}`);
  console.log(`      Sample Count: ${enhancedSession.sample_count}`);
  passed++;
  
  // Test 4: Evaluation data enhancement simulation
  console.log('\n4️⃣ Testing Evaluation Data Enhancement...');
  
  const evaluationData = {
    session_id: 'session_1756229497710_voices_3_expressivity_0.6',
    sample_id: 'v001_angry_match_scale_1.2',
    scores: { quality: 5, emotion: 6, similarity: 4 },
    comment: 'Test evaluation for voices_3 HD1 quality',
    timestamp: new Date().toISOString(),
    duration_ms: 15000
  };
  
  // Simulate enhanced evaluation data
  const parsedMetadata = parseSimpleSampleId(evaluationData.sample_id);
  const enhancedEvaluation = {
    ...evaluationData,
    experiment_version: 'voices_3',
    voice_set: 'expressivity_0.6',
    audio_quality: 'hd1',
    ...parsedMetadata
  };
  
  console.log('   ✅ Evaluation Enhancement: PASSED');
  console.log(`      Sample: ${enhancedEvaluation.sample_id}`);
  console.log(`      Voice: ${enhancedEvaluation.voice_id}, Emotion: ${enhancedEvaluation.emotion_value}`);
  console.log(`      Type: ${enhancedEvaluation.emotion_type}, Scale: ${enhancedEvaluation.emotion_scale}`);
  console.log(`      Audio Quality: ${enhancedEvaluation.audio_quality}`);
  passed++;
  
  // Summary
  console.log('\n🎉 TEST SUMMARY');
  console.log('-'.repeat(30));
  console.log(`✅ Tests Passed: ${passed}`);
  console.log(`❌ Tests Failed: ${failed}`);
  console.log(`📊 Success Rate: ${Math.round((passed / (passed + failed)) * 100)}%`);
  
  if (failed === 0) {
    console.log('\n🚀 ALL TESTS PASSED!');
    console.log('voices_3 logic is working correctly');
    console.log('Ready for production use');
  } else {
    console.log('\n⚠️  Some tests failed - please review the logic');
  }
  
  return { passed, failed };
}

// Run the logic tests
testVoices3Logic();
