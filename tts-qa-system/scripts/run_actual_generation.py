#!/usr/bin/env python3
"""
Script to call the ACTUAL TTS API for real audio generation
This replaces the mock audio files with real TTS output
"""

import json
import sys
import os
from pathlib import Path

def main():
    print("="*70)
    print("ACTUAL TTS API AUDIO GENERATION")
    print("="*70)
    
    print("\nCurrently, the system has generated MOCK audio files for testing.")
    print("These are synthetic sine waves, not real TTS output.")
    print("\nTo generate REAL TTS audio, you need to:")
    print()
    
    print("1. Provide your TTS API endpoint:")
    print("   Example: https://your-tts-api.com/generate")
    print()
    
    print("2. Run the generation scripts with the API endpoint:")
    print("   python3 scripts/generate_references.py YOUR_API_ENDPOINT")
    print("   python3 scripts/generate_style_variations.py YOUR_API_ENDPOINT")
    print("   python3 scripts/generate_emotion_vectors.py YOUR_API_ENDPOINT")
    print()
    
    print("3. Or use the batch generator for all samples:")
    print("   python3 scripts/batch_generate.py --endpoint YOUR_API_ENDPOINT")
    print()
    
    # Check current status
    voices_dir = Path(__file__).parent.parent / 'data' / 'voices'
    if voices_dir.exists():
        wav_files = list(voices_dir.glob('*.wav'))
        total_size = sum(f.stat().st_size for f in wav_files)
        
        print(f"Current Status:")
        print(f"  - Audio files: {len(wav_files)}")
        print(f"  - Total size: {total_size / 1024 / 1024:.1f} MB")
        
        if len(wav_files) > 0:
            sample_file = wav_files[0]
            sample_size = sample_file.stat().st_size
            print(f"  - Sample file: {sample_file.name} ({sample_size/1024:.1f} KB)")
            
            if sample_size < 200_000:  # Less than 200KB suggests mock files
                print("  - Status: MOCK FILES (synthetic audio for testing)")
                print("  - Action needed: Provide API endpoint for real TTS generation")
            else:
                print("  - Status: Likely REAL TTS files")
    
    print("\n" + "="*70)
    
    # Interactive mode
    if len(sys.argv) == 1:
        print("\nWould you like to:")
        print("1. Enter your API endpoint now")
        print("2. Exit and run manually later")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            endpoint = input("Enter your TTS API endpoint: ").strip()
            if endpoint:
                print(f"\nTo generate all samples with your endpoint:")
                print(f"python3 scripts/batch_generate.py --endpoint {endpoint}")
                
                confirm = input("\nRun batch generation now? (y/n): ").strip().lower()
                if confirm == 'y':
                    os.system(f'python3 scripts/batch_generate.py --endpoint {endpoint}')
            else:
                print("No endpoint provided.")
    
    return 0

if __name__ == "__main__":
    exit(main())