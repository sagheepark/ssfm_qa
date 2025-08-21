// Simple test to verify Supabase connection issue
// Load environment variables from .env.local
require('dotenv').config({ path: '.env.local' });

console.log('=== Testing Supabase Environment Variables ===');

// Test 1: Check if environment variables are available
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

console.log('Environment check:');
console.log('  NEXT_PUBLIC_SUPABASE_URL:', supabaseUrl ? 'SET' : 'MISSING');
console.log('  NEXT_PUBLIC_SUPABASE_ANON_KEY:', supabaseKey ? 'SET' : 'MISSING');

if (supabaseUrl) {
  console.log('  URL preview:', supabaseUrl.substring(0, 30) + '...');
}

// Test 2: Simulate Supabase client creation like the app does
try {
  const { createClient } = require('@supabase/supabase-js');
  
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  
  const supabase = supabaseUrl && supabaseAnonKey 
    ? createClient(supabaseUrl, supabaseAnonKey)
    : null;
    
  console.log('Supabase client:', supabase ? 'INITIALIZED' : 'NULL');
  
  if (!supabase) {
    console.error('❌ TEST FAILED: Supabase client is null');
    console.error('This is why evaluations fail with "Database connection not available"');
    process.exit(1);
  } else {
    console.log('✅ TEST PASSED: Supabase client is initialized');
    console.log('✅ This means the issue is with environment variable loading in Next.js');
  }
} catch (error) {
  console.error('❌ TEST FAILED: Error creating Supabase client:', error.message);
  process.exit(1);
}

console.log('=== Test Complete ===');