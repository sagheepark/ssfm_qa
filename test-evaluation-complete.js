// Complete test to identify all potential evaluation saving issues
require('dotenv').config({ path: '.env.local' });

async function testEvaluationComplete() {
  console.log('=== Complete Evaluation Saving Test ===');
  
  try {
    const { createClient } = require('@supabase/supabase-js');
    
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    
    console.log('1. Environment Variables:');
    console.log(`  URL: ${supabaseUrl ? 'SET' : 'MISSING'}`);
    console.log(`  KEY: ${supabaseAnonKey ? 'SET' : 'MISSING'}`);
    
    const supabase = createClient(supabaseUrl, supabaseAnonKey);
    
    const testSessionId = `test_complete_${Date.now()}`;
    
    console.log('\n2. Testing Session Creation:');
    const sessionData = {
      session_id: testSessionId,
      started_at: new Date().toISOString(),
      samples_data: []
    };
    
    console.log('  Sending:', sessionData);
    const sessionResult = await supabase
      .from('qa_sessions')
      .insert([sessionData])
      .select();
    
    console.log('  Response:', sessionResult);
    
    if (sessionResult.error) {
      console.error('❌ Session creation failed');
      return;
    }
    console.log('✅ Session creation successful');
    
    console.log('\n3. Testing Evaluation Creation:');
    const evaluationData = {
      session_id: testSessionId,
      sample_id: 'v001_match_emo_happy_scale_2.0',
      scores: { quality: 5, emotion: 4, similarity: 3 },
      comment: 'Complete test evaluation',
      timestamp: new Date().toISOString(),
      duration_ms: 5000
    };
    
    console.log('  Sending:', evaluationData);
    const evalResult = await supabase
      .from('sample_evaluations')
      .insert([evaluationData])
      .select();
    
    console.log('  Response:', evalResult);
    
    if (evalResult.error) {
      console.error('❌ Evaluation creation failed');
      console.error('  Error code:', evalResult.error.code);
      console.error('  Error message:', evalResult.error.message);
      console.error('  Error details:', evalResult.error.details);
      console.error('  Error hint:', evalResult.error.hint);
      
      // Check specific error types
      if (evalResult.error.code === '42501') {
        console.log('\n🔧 DIAGNOSIS: RLS Policy Issue');
        console.log('  The RLS policy may not have been created correctly or applied');
        console.log('  Try this SQL in Supabase dashboard:');
        console.log('    DROP POLICY IF EXISTS "Allow anonymous evaluation creation" ON sample_evaluations;');
        console.log('    CREATE POLICY "Allow anonymous evaluation creation" ON sample_evaluations FOR INSERT WITH CHECK (true);');
      } else if (evalResult.error.code === '23503') {
        console.log('\n🔧 DIAGNOSIS: Foreign Key Constraint');
        console.log('  The session_id does not exist in qa_sessions table');
      } else if (evalResult.error.code === '23505') {
        console.log('\n🔧 DIAGNOSIS: Unique Constraint Violation');
        console.log('  Duplicate evaluation or primary key conflict');
      } else {
        console.log('\n🔧 DIAGNOSIS: Unknown Error');
        console.log('  This is a different type of database error');
      }
      
      // Clean up session
      await supabase.from('qa_sessions').delete().eq('session_id', testSessionId);
      return;
    }
    
    console.log('✅ Evaluation creation successful');
    
    console.log('\n4. Testing Data Retrieval:');
    const retrieveResult = await supabase
      .from('sample_evaluations')
      .select('*')
      .eq('session_id', testSessionId);
    
    console.log('  Retrieved data:', retrieveResult.data);
    
    console.log('\n5. Cleanup:');
    await supabase.from('sample_evaluations').delete().eq('session_id', testSessionId);
    await supabase.from('qa_sessions').delete().eq('session_id', testSessionId);
    console.log('✅ Cleanup complete');
    
    console.log('\n✅ ALL TESTS PASSED - Database operations work correctly');
    
  } catch (error) {
    console.error('❌ Test failed with JavaScript error:', error);
    console.error('  Error type:', typeof error);
    console.error('  Error instanceof Error:', error instanceof Error);
    console.error('  Error stringified:', JSON.stringify(error, null, 2));
  }
}

testEvaluationComplete().then(() => {
  console.log('\n=== Test Complete ===');
});