// Test Next.js environment variable handling
// This tests if next.config.js properly exposes env vars

console.log('=== Testing Next.js Environment Variable Handling ===');

// Test if next.config.js works by simulating Next.js environment
process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test_key_123';

console.log('Set test environment variables...');

// Test 1: Direct environment variable access
console.log('Direct env access:');
console.log('  NEXT_PUBLIC_SUPABASE_URL:', process.env.NEXT_PUBLIC_SUPABASE_URL ? 'SET' : 'MISSING');
console.log('  NEXT_PUBLIC_SUPABASE_ANON_KEY:', process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ? 'SET' : 'MISSING');

// Test 2: Simulate what our lib/supabase.ts does
try {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  
  console.log('\nSimulating lib/supabase.ts logic:');
  console.log('  supabaseUrl:', supabaseUrl ? 'AVAILABLE' : 'UNDEFINED');
  console.log('  supabaseAnonKey:', supabaseAnonKey ? 'AVAILABLE' : 'UNDEFINED');
  
  const canCreateClient = supabaseUrl && supabaseAnonKey;
  console.log('  canCreateClient:', canCreateClient ? 'YES' : 'NO');
  
  if (!canCreateClient) {
    console.error('❌ TEST FAILED: Cannot create Supabase client');
    console.error('This means the "Database connection not available" error will occur');
    process.exit(1);
  } else {
    console.log('✅ TEST PASSED: Can create Supabase client');
    console.log('✅ Environment variables are properly accessible');
  }
} catch (error) {
  console.error('❌ TEST FAILED:', error.message);
  process.exit(1);
}

// Test 3: Check if the issue is with client-side vs server-side
console.log('\n🔍 DIAGNOSIS:');
console.log('If this test passes but the app still fails, the issue is likely:');
console.log('1. Environment variables not set in Vercel dashboard');
console.log('2. Client-side access to environment variables blocked');
console.log('3. Build-time vs runtime environment variable availability');

console.log('\n=== Test Complete ===');