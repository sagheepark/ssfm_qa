// Test actual evaluation saving functionality
require('dotenv').config({ path: '.env.local' });

async function testEvaluationSaving() {
  console.log('=== Testing Evaluation Saving ===');
  
  try {
    const { createClient } = require('@supabase/supabase-js');
    
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
    
    if (!supabaseUrl || !supabaseAnonKey) {
      throw new Error('Environment variables not available');
    }
    
    // Try with service role key to bypass RLS for testing
    const testKey = supabaseServiceKey || supabaseAnonKey;
    const supabase = createClient(supabaseUrl, testKey);
    
    console.log('Using key type:', supabaseServiceKey ? 'SERVICE_ROLE' : 'ANON');
    
    // Test data that should work with current database schema
    const testEvaluation = {
      session_id: `test_session_${Date.now()}`,
      sample_id: 'v001_match_emo_happy_scale_2.0',
      scores: { quality: 5, emotion: 4, similarity: 3 },
      comment: 'Test evaluation from TDD',
      timestamp: new Date().toISOString(),
      duration_ms: 5000
    };
    
    // First create a session (required for foreign key)
    console.log('Creating test session...');
    const sessionResult = await supabase
      .from('qa_sessions')
      .insert([{
        session_id: testEvaluation.session_id,
        started_at: new Date().toISOString(),
        samples_data: []
      }])
      .select();
    
    if (sessionResult.error) {
      console.error('❌ Session creation failed:', sessionResult.error);
      return false;
    }
    
    console.log('✅ Session created successfully');
    
    // Now test evaluation saving
    console.log('Saving test evaluation...');
    const evalResult = await supabase
      .from('sample_evaluations')
      .insert([testEvaluation])
      .select();
    
    if (evalResult.error) {
      console.error('❌ Evaluation saving failed:', evalResult.error);
      return false;
    }
    
    console.log('✅ Evaluation saved successfully');
    console.log('✅ TEST PASSED: Database operations work correctly');
    
    // Clean up
    await supabase.from('sample_evaluations').delete().eq('session_id', testEvaluation.session_id);
    await supabase.from('qa_sessions').delete().eq('session_id', testEvaluation.session_id);
    console.log('✅ Test data cleaned up');
    
    return true;
    
  } catch (error) {
    console.error('❌ TEST FAILED:', error.message);
    return false;
  }
}

testEvaluationSaving().then(success => {
  console.log('=== Test Complete ===');
  process.exit(success ? 0 : 1);
});