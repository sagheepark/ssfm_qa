#!/usr/bin/env node

/**
 * Test script to validate RLS policy fix for v2 tables
 */

const { createClient } = require('@supabase/supabase-js');

// Load environment variables
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Missing Supabase environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function testRLSFix() {
  console.log('🔧 Testing RLS Policy Fix for V2 Tables');
  console.log('=' .repeat(50));
  
  const testSessionId = `test-rls-fix-${Date.now()}`;
  
  try {
    // Test 1: Create session in qa_sessions_v2
    console.log('\n1. Testing qa_sessions_v2 creation:');
    const sessionData = {
      session_id: testSessionId,
      started_at: new Date().toISOString(),
      experiment_version: 'voices_2',
      voice_set: 'expressivity_none',
      sample_count: 25,
      samples_data: { test: 'data' }
    };
    
    const { data: sessionResult, error: sessionError } = await supabase
      .from('qa_sessions_v2')
      .insert([sessionData])
      .select();
    
    if (sessionError) {
      console.error('  ❌ Session creation failed:', sessionError);
      console.error('  Error code:', sessionError.code);
      console.error('  Error message:', sessionError.message);
      
      if (sessionError.code === '42501') {
        console.log('\n🔧 SOLUTION NEEDED:');
        console.log('  Run the SQL policy fix in your Supabase dashboard:');
        console.log(`
CREATE POLICY "Allow all operations on qa_sessions_v2" ON public.qa_sessions_v2 
  FOR ALL USING (true) WITH CHECK (true);
        `);
      }
      
      return false;
    }
    
    console.log('  ✅ Session created successfully');
    
    // Test 2: Create evaluation in sample_evaluations_v2
    console.log('\n2. Testing sample_evaluations_v2 creation:');
    const evaluationData = {
      session_id: testSessionId,
      sample_id: 'v001_angry_match_scale_1.0',
      scores: { quality: 7, emotion: 8, similarity: 6 },
      comment: 'Test evaluation after RLS fix',
      experiment_version: 'voices_2',
      voice_set: 'expressivity_none',
      voice_id: 'v001',
      emotion_type: 'emotion_label',
      emotion_value: 'angry',
      text_type: 'match',
      emotion_scale: 1.0
    };
    
    const { data: evalResult, error: evalError } = await supabase
      .from('sample_evaluations_v2')
      .insert([evaluationData])
      .select();
    
    if (evalError) {
      console.error('  ❌ Evaluation creation failed:', evalError);
      console.error('  Error code:', evalError.code);
      return false;
    }
    
    console.log('  ✅ Evaluation created successfully');
    
    // Test 3: Update session
    console.log('\n3. Testing session update:');
    const { data: updateResult, error: updateError } = await supabase
      .from('qa_sessions_v2')
      .update({ 
        completed_at: new Date().toISOString(),
        completion_percentage: 100
      })
      .eq('session_id', testSessionId)
      .select();
    
    if (updateError) {
      console.error('  ❌ Session update failed:', updateError);
      return false;
    }
    
    console.log('  ✅ Session updated successfully');
    
    // Cleanup
    console.log('\n4. Cleanup:');
    await supabase.from('sample_evaluations_v2').delete().eq('session_id', testSessionId);
    await supabase.from('qa_sessions_v2').delete().eq('session_id', testSessionId);
    console.log('  ✅ Test data cleaned up');
    
    console.log('\n🎉 ALL TESTS PASSED!');
    console.log('✅ RLS policies are working correctly');
    console.log('🚀 Your app should work now');
    
    return true;
    
  } catch (error) {
    console.error('\n💥 Test failed with error:', error);
    
    // Cleanup on error
    try {
      await supabase.from('sample_evaluations_v2').delete().eq('session_id', testSessionId);
      await supabase.from('qa_sessions_v2').delete().eq('session_id', testSessionId);
    } catch (cleanupError) {
      // Ignore cleanup errors
    }
    
    return false;
  }
}

testRLSFix().then(success => {
  process.exit(success ? 0 : 1);
}).catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});