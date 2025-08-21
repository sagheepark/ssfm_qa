// Test RLS policy issue in deployed environment
require('dotenv').config({ path: '.env.local' });

async function testDeployedRLSIssue() {
  console.log('=== Testing Deployed RLS Issue ===');
  
  try {
    const { createClient } = require('@supabase/supabase-js');
    
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    
    if (!supabaseUrl || !supabaseAnonKey) {
      console.error('❌ Environment variables not available locally');
      return;
    }
    
    const supabase = createClient(supabaseUrl, supabaseAnonKey);
    
    console.log('Testing with anon key (same as deployed app)...');
    
    // Test session creation first
    const testSessionId = `test_rls_${Date.now()}`;
    
    console.log('1. Creating test session...');
    const sessionResult = await supabase
      .from('qa_sessions')
      .insert([{
        session_id: testSessionId,
        started_at: new Date().toISOString(),
        samples_data: []
      }])
      .select();
    
    if (sessionResult.error) {
      console.error('❌ Session creation failed:', sessionResult.error);
      console.log('🔧 This is likely the RLS policy blocking anonymous users');
      console.log('📝 Solution: Create RLS policy for anonymous session creation');
      return;
    }
    
    console.log('✅ Session created successfully');
    
    // Test evaluation creation
    console.log('2. Creating test evaluation...');
    const evalResult = await supabase
      .from('sample_evaluations')
      .insert([{
        session_id: testSessionId,
        sample_id: 'test_sample_123',
        scores: { quality: 5, emotion: 4, similarity: 3 },
        comment: 'Test evaluation',
        timestamp: new Date().toISOString(),
        duration_ms: 5000
      }])
      .select();
    
    if (evalResult.error) {
      console.error('❌ Evaluation creation failed:', evalResult.error);
      console.log('🔧 This matches the "[object Object]" error in the app!');
      console.log('📝 Solution: Create RLS policy for anonymous evaluation creation');
      
      // Clean up session
      await supabase.from('qa_sessions').delete().eq('session_id', testSessionId);
      return;
    }
    
    console.log('✅ Evaluation created successfully');
    console.log('✅ No RLS issues - something else is causing the error');
    
    // Clean up
    await supabase.from('sample_evaluations').delete().eq('session_id', testSessionId);
    await supabase.from('qa_sessions').delete().eq('session_id', testSessionId);
    
  } catch (error) {
    console.error('❌ Test failed with error:', error);
  }
}

testDeployedRLSIssue().then(() => {
  console.log('\n💡 MOST LIKELY ISSUE:');
  console.log('The "[object Object]" error is probably a Supabase RLS policy error.');
  console.log('You need to create RLS policies in Supabase dashboard to allow anonymous access.');
  console.log('\n=== Test Complete ===');
});