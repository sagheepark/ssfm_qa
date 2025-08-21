// Test to check if RLS policies allow anonymous evaluation saving
require('dotenv').config({ path: '.env.local' });

async function checkRLSPolicies() {
  console.log('=== Testing RLS Policies for Anonymous Access ===');
  
  try {
    const { createClient } = require('@supabase/supabase-js');
    
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    
    // Test with ANON key (what the app will use)
    const supabase = createClient(supabaseUrl, supabaseAnonKey);
    
    const testSession = `rls_test_${Date.now()}`;
    
    // Test session creation
    console.log('Testing session creation with anon key...');
    const sessionResult = await supabase
      .from('qa_sessions')
      .insert([{
        session_id: testSession,
        started_at: new Date().toISOString(),
        samples_data: []
      }])
      .select();
    
    if (sessionResult.error) {
      console.error('❌ Session creation blocked by RLS:', sessionResult.error.message);
      console.log('💡 Solution: Need to create RLS policy to allow anonymous session creation');
      return false;
    }
    
    console.log('✅ Session creation works with anon key');
    
    // Test evaluation creation  
    console.log('Testing evaluation creation with anon key...');
    const evalResult = await supabase
      .from('sample_evaluations')
      .insert([{
        session_id: testSession,
        sample_id: 'test_sample',
        scores: { quality: 5, emotion: 4, similarity: 3 },
        comment: 'RLS test',
        timestamp: new Date().toISOString(),
        duration_ms: 5000
      }])
      .select();
    
    if (evalResult.error) {
      console.error('❌ Evaluation creation blocked by RLS:', evalResult.error.message);
      console.log('💡 Solution: Need to create RLS policy to allow anonymous evaluation creation');
      
      // Clean up session
      await supabase.from('qa_sessions').delete().eq('session_id', testSession);
      return false;
    }
    
    console.log('✅ Evaluation creation works with anon key');
    console.log('✅ All tests pass - RLS policies are correctly configured');
    
    // Clean up
    await supabase.from('sample_evaluations').delete().eq('session_id', testSession);
    await supabase.from('qa_sessions').delete().eq('session_id', testSession);
    
    return true;
    
  } catch (error) {
    console.error('❌ TEST FAILED:', error.message);
    return false;
  }
}

checkRLSPolicies().then(success => {
  console.log('=== Test Complete ===');
  if (!success) {
    console.log('\n🔧 To fix RLS policies, run these SQL commands in Supabase dashboard:');
    console.log(`
-- Allow anonymous users to insert sessions
CREATE POLICY "Allow anonymous session creation" ON qa_sessions FOR INSERT 
WITH CHECK (true);

-- Allow anonymous users to insert evaluations  
CREATE POLICY "Allow anonymous evaluation creation" ON sample_evaluations FOR INSERT
WITH CHECK (true);

-- Allow anonymous users to update session completion
CREATE POLICY "Allow anonymous session updates" ON qa_sessions FOR UPDATE
WITH CHECK (true);
    `);
  }
  process.exit(success ? 0 : 1);
});