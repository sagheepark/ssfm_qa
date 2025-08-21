// API route to check environment variables in deployment
import { NextResponse } from 'next/server';

export async function GET() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  const envCheck = {
    url: supabaseUrl ? 'SET' : 'MISSING',
    key: supabaseKey ? 'SET' : 'MISSING',
    urlPreview: supabaseUrl ? supabaseUrl.substring(0, 30) + '...' : 'N/A',
    timestamp: new Date().toISOString(),
    nodeEnv: process.env.NODE_ENV,
    message: supabaseUrl && supabaseKey ? 'Environment variables are available' : 'Environment variables are missing'
  };

  return NextResponse.json(envCheck);
}