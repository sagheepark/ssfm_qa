#!/usr/bin/env python3
"""
Export voices_3 evaluation data from Supabase for analysis
Supports both V2 and V3 table structures
"""

import os
import pandas as pd
from supabase import create_client, Client
import json
from datetime import datetime
import sys

def get_supabase_client():
    """Initialize Supabase client"""
    url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    key = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    
    if not url or not key:
        print("Error: Supabase environment variables not found")
        print("Please set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY")
        return None
    
    return create_client(url, key)

def export_v3_evaluations(supabase: Client, output_file: str = None):
    """Export V3 evaluation data"""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"analysis/voices_3_evaluations_{timestamp}.csv"
    
    try:
        # Try to query V3 tables first
        print("Attempting to query sample_evaluations_v3 table...")
        response = supabase.table("sample_evaluations_v3").select("*").execute()
        
        if response.data:
            print(f"Found {len(response.data)} evaluations in V3 table")
            df = pd.DataFrame(response.data)
        else:
            # Fallback to V2 table with voices_3 filter
            print("V3 table empty, checking V2 table for voices_3 data...")
            response = supabase.table("sample_evaluations_v2").select("*").eq("experiment_version", "voices_3").execute()
            
            if response.data:
                print(f"Found {len(response.data)} voices_3 evaluations in V2 table")
                df = pd.DataFrame(response.data)
            else:
                print("No voices_3 data found in either V3 or V2 tables")
                return None
        
        # Process the data
        if 'scores' in df.columns:
            # If scores is still JSON, expand it
            if df['scores'].dtype == 'object':
                scores_expanded = pd.json_normalize(df['scores'])
                df = pd.concat([df.drop('scores', axis=1), scores_expanded], axis=1)
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"Data exported to: {output_file}")
        
        # Print summary
        print(f"\nData Summary:")
        print(f"Total evaluations: {len(df)}")
        if 'experiment_version' in df.columns:
            print(f"Experiment versions: {df['experiment_version'].value_counts().to_dict()}")
        if 'voice_id' in df.columns:
            print(f"Voice distribution: {df['voice_id'].value_counts().to_dict()}")
        if 'audio_quality' in df.columns:
            print(f"Audio quality: {df['audio_quality'].value_counts().to_dict()}")
        
        return output_file
        
    except Exception as e:
        print(f"Error exporting data: {e}")
        return None

def export_v3_sessions(supabase: Client, output_file: str = None):
    """Export V3 session data"""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"analysis/voices_3_sessions_{timestamp}.csv"
    
    try:
        # Try V3 table first
        print("Attempting to query qa_sessions_v3 table...")
        response = supabase.table("qa_sessions_v3").select("*").execute()
        
        if response.data:
            print(f"Found {len(response.data)} sessions in V3 table")
            df = pd.DataFrame(response.data)
        else:
            # Fallback to V2 table
            print("V3 table empty, checking V2 table for voices_3 data...")
            response = supabase.table("qa_sessions_v2").select("*").eq("experiment_version", "voices_3").execute()
            
            if response.data:
                print(f"Found {len(response.data)} voices_3 sessions in V2 table")
                df = pd.DataFrame(response.data)
            else:
                print("No voices_3 session data found")
                return None
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"Session data exported to: {output_file}")
        
        return output_file
        
    except Exception as e:
        print(f"Error exporting session data: {e}")
        return None

def main():
    """Main export function"""
    print("voices_3 Data Export Utility")
    print("="*40)
    
    # Initialize Supabase client
    supabase = get_supabase_client()
    if not supabase:
        sys.exit(1)
    
    # Export evaluations
    eval_file = export_v3_evaluations(supabase)
    
    # Export sessions
    session_file = export_v3_sessions(supabase)
    
    if eval_file:
        print(f"\n✅ Export complete!")
        print(f"Evaluations: {eval_file}")
        if session_file:
            print(f"Sessions: {session_file}")
        
        print(f"\nTo run analysis:")
        print(f"python analysis/tts_analysis_v3.py")
    else:
        print(f"\n❌ No data to export. Make sure you have completed some voices_3 evaluation sessions.")

if __name__ == "__main__":
    main()
