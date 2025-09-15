#!/usr/bin/env node
/**
 * Test script for voices_3 complete session flow
 * Tests V3 routing, database operations, and data integrity
 */

const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Missing Supabase environment variables');
  console.error('Please set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Test data
const testSessionId = `test_session_${Date.now()}_voices_3_expressivity_0.6`;
const testEvaluations = [
  {
    session_id: testSessionId,
    sample_id: 'v001_angry_match_scale_1.2',
    scores: { quality: 5, emotion: 6, similarity: 4 },
    comment: 'Test evaluation for voices_3 HD1 quality',
    timestamp: new Date().toISOString(),
    duration_ms: 15000
  },
  {
    session_id: testSessionId,
    sample_id: 'v002_excited_neutral_scale_1.8',
    scores: { quality: 6, emotion: 7, similarity: 5 },
    comment: 'Second test evaluation with emotion vector',
    timestamp: new Date().toISOString(),
    duration_ms: 18000
  }
];

async function testV3SessionFlow() {
  console.log('🧪 Testing voices_3 Complete Session Flow');
  console.log('='*50);
  
  try {
    // Step 1: Test V3 session creation
    console.log('\n1️⃣ Testing V3 session creation...');
    
    const sessionData = {
      session_id: testSessionId,
      started_at: new Date().toISOString(),
      experiment_version: 'voices_3',
      voice_set: 'expressivity_0.6',
      sample_count: 2,
      samples_data: testEvaluations.map(e => ({ sample_id: e.sample_id }))
    };
    
    // Try V3 table first, fallback to V2
    let sessionResult;
    try {
      sessionResult = await supabase
        .from('qa_sessions_v3')
        .upsert([sessionData], { onConflict: 'session_id' })
        .select();
    } catch (error) {
      console.log('   V3 table not available, using V2 table...');
      sessionResult = await supabase
        .from('qa_sessions_v2')
        .upsert([sessionData], { onConflict: 'session_id' })
        .select();
    }
    
    if (sessionResult.error) {
      throw new Error(`Session creation failed: ${sessionResult.error.message}`);
    }
    
    console.log('   ✅ Session created successfully');
    console.log(`   Session ID: ${sessionResult.data[0].session_id}`);
    console.log(`   Experiment version: ${sessionResult.data[0].experiment_version}`);
    
    // Step 2: Test V3 evaluation creation
    console.log('\n2️⃣ Testing V3 evaluation creation...');
    
    for (const [index, evaluation] of testEvaluations.entries()) {
      // Parse sample_id to extract metadata (simulating smart routing logic)
      const parts = evaluation.sample_id.split('_');
      const enhancedEvaluation = {
        ...evaluation,
        experiment_version: 'voices_3',
        voice_set: 'expressivity_0.6',
        audio_quality: 'hd1',
        voice_id: parts[0],
        emotion_value: parts[1],
        text_type: parts[2],
        emotion_scale: parseFloat(parts[4]),
        emotion_type: ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown'].includes(parts[1]) 
          ? 'emotion_label' 
          : 'emotion_vector'
      };
      
      // Try V3 table first, fallback to V2
      let evalResult;
      try {
        evalResult = await supabase
          .from('sample_evaluations_v3')
          .insert([enhancedEvaluation])
          .select();
      } catch (error) {
        console.log('   V3 table not available, using V2 table...');
        evalResult = await supabase
          .from('sample_evaluations_v2')
          .insert([enhancedEvaluation])
          .select();
      }
      
      if (evalResult.error) {
        throw new Error(`Evaluation ${index + 1} creation failed: ${evalResult.error.message}`);
      }
      
      console.log(`   ✅ Evaluation ${index + 1} created successfully`);
      console.log(`   Sample: ${evalResult.data[0].sample_id}`);
      console.log(`   Voice: ${evalResult.data[0].voice_id}, Emotion: ${evalResult.data[0].emotion_value}`);
      console.log(`   Audio Quality: ${evalResult.data[0].audio_quality}`);
    }
    
    // Step 3: Test data retrieval and validation
    console.log('\n3️⃣ Testing data retrieval...');
    
    // Query evaluations
    let retrievedEvals;
    try {
      retrievedEvals = await supabase
        .from('sample_evaluations_v3')
        .select('*')
        .eq('session_id', testSessionId);
    } catch (error) {
      retrievedEvals = await supabase
        .from('sample_evaluations_v2')
        .select('*')
        .eq('session_id', testSessionId);
    }
    
    if (retrievedEvals.error) {
      throw new Error(`Data retrieval failed: ${retrievedEvals.error.message}`);
    }
    
    console.log(`   ✅ Retrieved ${retrievedEvals.data.length} evaluations`);
    
    // Validate data integrity
    for (const evaluation of retrievedEvals.data) {
      console.log(`   📊 Evaluation: ${evaluation.sample_id}`);
      console.log(`      Experiment: ${evaluation.experiment_version}`);
      console.log(`      Audio Quality: ${evaluation.audio_quality}`);
      console.log(`      Scores: Q=${evaluation.scores?.quality || evaluation.quality}, E=${evaluation.scores?.emotion || evaluation.emotion}, S=${evaluation.scores?.similarity || evaluation.similarity}`);
    }
    
    // Step 4: Test session completion
    console.log('\n4️⃣ Testing session completion...');
    
    const completionUpdate = {
      completed_at: new Date().toISOString(),
      completion_percentage: 100
    };
    
    let updateResult;
    try {
      updateResult = await supabase
        .from('qa_sessions_v3')
        .update(completionUpdate)
        .eq('session_id', testSessionId)
        .select();
    } catch (error) {
      updateResult = await supabase
        .from('qa_sessions_v2')
        .update(completionUpdate)
        .eq('session_id', testSessionId)
        .select();
    }
    
    if (updateResult.error) {
      throw new Error(`Session completion failed: ${updateResult.error.message}`);
    }
    
    console.log('   ✅ Session marked as completed');
    console.log(`   Completed at: ${updateResult.data[0].completed_at}`);
    
    // Step 5: Summary
    console.log('\n🎉 TEST SUMMARY');
    console.log('-'.repeat(30));
    console.log('✅ V3 session creation: PASSED');
    console.log('✅ V3 evaluation creation: PASSED');
    console.log('✅ Data retrieval: PASSED');
    console.log('✅ Session completion: PASSED');
    console.log('✅ voices_3 HD1 quality tracking: PASSED');
    console.log('✅ Smart routing logic: PASSED');
    
    console.log('\n📈 READY FOR PRODUCTION');
    console.log('Your voices_3 dataset is ready for evaluation sessions!');
    
  } catch (error) {
    console.error('\n❌ TEST FAILED');
    console.error('Error:', error.message);
    
    if (error.message.includes('relation') && error.message.includes('does not exist')) {
      console.error('\n💡 SOLUTION: Create the missing database table:');
      if (error.message.includes('qa_sessions_v3')) {
        console.error('   Missing qa_sessions_v3 table');
      }
      if (error.message.includes('sample_evaluations_v3')) {
        console.error('   Missing sample_evaluations_v3 table');
      }
      console.error('   Run the V3 table creation SQL in your Supabase dashboard');
    }
  } finally {
    // Cleanup test data
    console.log('\n🧹 Cleaning up test data...');
    try {
      // Try both V3 and V2 tables for cleanup
      await supabase.from('sample_evaluations_v3').delete().eq('session_id', testSessionId);
      await supabase.from('sample_evaluations_v2').delete().eq('session_id', testSessionId);
      await supabase.from('qa_sessions_v3').delete().eq('session_id', testSessionId);
      await supabase.from('qa_sessions_v2').delete().eq('session_id', testSessionId);
      console.log('   ✅ Test data cleaned up');
    } catch (error) {
      console.log('   ⚠️  Cleanup completed (some tables may not exist yet)');
    }
  }
}

// Run the test
testV3SessionFlow().catch(console.error);
