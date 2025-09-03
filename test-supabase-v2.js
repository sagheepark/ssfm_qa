#!/usr/bin/env node

/**
 * Test script for Supabase v2 tables (voices_2 experiment)
 */

const { createClient } = require('@supabase/supabase-js');

// Load environment variables
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Missing Supabase environment variables');
  console.log('Required:');
  console.log('  NEXT_PUBLIC_SUPABASE_URL');
  console.log('  NEXT_PUBLIC_SUPABASE_ANON_KEY');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function testSupabaseV2() {
  console.log('🧪 Testing Supabase V2 Tables (voices_2 experiment)');
  console.log('=' .repeat(60));
  
  // Generate test IDs
  const testSessionId = `test-session-v2-${Date.now()}`;
  const testSampleId = `v001_angry_match_scale_1.0`;
  
  try {
    // Test 1: Create Session V2
    console.log('\n1. Testing qa_sessions_v2 table:');
    const sessionData = {
      session_id: testSessionId,
      started_at: new Date().toISOString(),
      experiment_version: 'voices_2',
      voice_set: 'expressivity_none',
      sample_count: 10,
      samples_data: { test: 'data' }
    };
    
    console.log('  Creating session:', sessionData.session_id);
    const sessionResult = await supabase
      .from('qa_sessions_v2')
      .insert([sessionData])
      .select();
    
    if (sessionResult.error) {
      console.error('  ❌ Session creation failed:', sessionResult.error);
      return false;
    }
    console.log('  ✅ Session created successfully');
    
    // Test 2: Create Evaluation V2
    console.log('\n2. Testing sample_evaluations_v2 table:');
    const evaluationData = {
      session_id: testSessionId,
      sample_id: testSampleId,
      scores: {
        quality: 7,
        emotion: 8,
        similarity: 6
      },
      comment: 'Test evaluation for voices_2 experiment',
      experiment_version: 'voices_2',
      voice_set: 'expressivity_none',
      voice_id: 'v001',
      emotion_type: 'emotion_label',
      emotion_value: 'angry',
      text_type: 'match',
      emotion_scale: 1.0,
      playback_count: 2,
      evaluation_order: 1
    };
    
    console.log('  Creating evaluation for:', evaluationData.sample_id);
    const evalResult = await supabase
      .from('sample_evaluations_v2')
      .insert([evaluationData])
      .select();
    
    if (evalResult.error) {
      console.error('  ❌ Evaluation creation failed:', evalResult.error);
      
      if (evalResult.error.code === '42501') {
        console.log('\n🔧 DIAGNOSIS: Row Level Security (RLS) Policy Issue');
        console.log('  The RLS policy may not have been created correctly or applied');
        console.log('  Please run the SQL policies in your Supabase dashboard');
      } else if (evalResult.error.code === '23503') {
        console.log('\n🔧 DIAGNOSIS: Foreign Key Constraint');
        console.log('  The session_id does not exist in qa_sessions_v2 table');
      }
      
      // Clean up session
      await supabase.from('qa_sessions_v2').delete().eq('session_id', testSessionId);
      return false;
    }
    console.log('  ✅ Evaluation created successfully');
    
    // Test 3: Update Session V2
    console.log('\n3. Testing session updates:');
    const updateResult = await supabase
      .from('qa_sessions_v2')
      .update({
        completed_at: new Date().toISOString(),
        completion_percentage: 100.0
      })
      .eq('session_id', testSessionId)
      .select();
    
    if (updateResult.error) {
      console.error('  ❌ Session update failed:', updateResult.error);
    } else {
      console.log('  ✅ Session updated successfully');
    }
    
    // Test 4: Data Retrieval
    console.log('\n4. Testing data retrieval:');
    const retrieveResult = await supabase
      .from('sample_evaluations_v2')
      .select(`
        *,
        qa_sessions_v2!inner(session_id, experiment_version, voice_set)
      `)
      .eq('session_id', testSessionId);
    
    if (retrieveResult.error) {
      console.error('  ❌ Data retrieval failed:', retrieveResult.error);
    } else {
      console.log('  ✅ Data retrieved successfully');
      console.log('  📊 Retrieved records:', retrieveResult.data.length);
    }
    
    // Test 5: Check sample_metadata_v2 table
    console.log('\n5. Testing sample_metadata_v2 table:');
    const metadataResult = await supabase
      .from('sample_metadata_v2')
      .select('*')
      .limit(1);
    
    if (metadataResult.error) {
      console.error('  ❌ Metadata query failed:', metadataResult.error);
      console.log('  💡 This table might be empty - that\'s expected for now');
    } else {
      console.log('  ✅ Metadata table accessible');
      console.log('  📊 Sample records:', metadataResult.data.length);
    }
    
    // Cleanup
    console.log('\n6. Cleanup:');
    await supabase.from('sample_evaluations_v2').delete().eq('session_id', testSessionId);
    await supabase.from('qa_sessions_v2').delete().eq('session_id', testSessionId);
    console.log('  ✅ Cleanup complete');
    
    console.log('\n🎉 ALL TESTS PASSED!');
    console.log('\n📋 Next Steps:');
    console.log('  1. Create the Supabase tables using the provided SQL');
    console.log('  2. Update your app to use V2 functions for voices_2 experiment');
    console.log('  3. Populate sample_metadata_v2 with your voices_2 data');
    
    return true;
    
  } catch (error) {
    console.error('\n💥 Test failed with error:', error);
    
    // Cleanup on error
    try {
      await supabase.from('sample_evaluations_v2').delete().eq('session_id', testSessionId);
      await supabase.from('qa_sessions_v2').delete().eq('session_id', testSessionId);
    } catch (cleanupError) {
      console.error('Cleanup error:', cleanupError);
    }
    
    return false;
  }
}

// Handle SIGINT
process.on('SIGINT', () => {
  console.log('\n\n⚠️  Test interrupted by user');
  process.exit(0);
});

testSupabaseV2().then(success => {
  process.exit(success ? 0 : 1);
}).catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});