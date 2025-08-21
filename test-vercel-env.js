// Test that replicates the Vercel deployment environment
// This should FAIL initially, showing the exact issue

console.log('=== Testing Vercel Deployment Environment ===');

// DO NOT load .env.local - simulate Vercel environment
// require('dotenv').config({ path: '.env.local' }); // COMMENTED OUT

console.log('Simulating Vercel environment (no .env.local)...');

// Test 1: Check if environment variables are available (like in Vercel)
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

console.log('Environment check (Vercel simulation):');
console.log('  NEXT_PUBLIC_SUPABASE_URL:', supabaseUrl ? 'SET' : 'MISSING');
console.log('  NEXT_PUBLIC_SUPABASE_ANON_KEY:', supabaseKey ? 'SET' : 'MISSING');

// Test 2: Try to create Supabase client (like the app does)
try {
  const { createClient } = require('@supabase/supabase-js');
  
  const supabase = supabaseUrl && supabaseKey 
    ? createClient(supabaseUrl, supabaseKey)
    : null;
    
  console.log('Supabase client:', supabase ? 'INITIALIZED' : 'NULL');
  
  if (!supabase) {
    console.error('❌ TEST FAILED: Supabase client is null');
    console.error('This exactly matches the deployed app error: "Database connection not available"');
    console.log('\n🔧 ROOT CAUSE: Environment variables not available in Vercel environment');
    console.log('📝 EXPECTED: This test should PASS once Vercel env vars are properly configured');
    process.exit(1);
  } else {
    console.log('✅ TEST PASSED: Supabase client is initialized');
    console.log('✅ Environment variables are properly available in deployment');
  }
} catch (error) {
  console.error('❌ TEST FAILED: Error creating Supabase client:', error.message);
  process.exit(1);
}

console.log('=== Test Complete ===');