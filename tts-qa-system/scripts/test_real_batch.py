#!/usr/bin/env python3
"""
Test real TTS generation with a small batch of different sample types
"""

import json
import sys
from pathlib import Path
from tts_api_client import TTSAPIClient

def test_small_batch():
    """Test with a few samples of different types"""
    
    print("="*70)
    print("TESTING REAL TTS GENERATION - SMALL BATCH")
    print("="*70)
    
    # Token from working example
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWMwMWU5YzhkMzc5M2NmNDBlMmJlMjkiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJoYXNfYWRtaW5fcGVybWlzc2lvbl9zY29wZSI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3R5cGVjYXN0LWE0YzhmIiwiYXVkIjoidHlwZWNhc3QtYTRjOGYiLCJhdXRoX3RpbWUiOjE3NTU1MzY4MDcsInVzZXJfaWQiOiJvQ21yajBPUzJJVmpQMjFxb2QyRlZGdTJsR2QyIiwic3ViIjoib0NtcmowT1MySVZqUDIxcW9kMkZWRnUybEdkMiIsImlhdCI6MTc1NTc1OTA3NSwiZXhwIjoxNzU1NzYyNjc1LCJlbWFpbCI6InNhbmdnb29AbmVvc2FwaWVuY2UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdnb29AbmVvc2FwaWVuY2UuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.UG__H6qnbLRROq3G_LW96n4Yz4iKSEdAZ0v0f9PJOXk382X8M3qSlbMyrk6lnnLQ4iJd2RjbM30lY--i4FRhaL5szeeQTorRU4sdfaKZ7RHhRZw66__5yZlALHbXEZBHmKI0bpr1X_am1VkoohiwKbCHT34VVb_tYK_6YWRtQIe0VTyeD94XOaIsQFJ5NeOCic-UHUXaV8k3IZGQ_sMBg9scaP6DvqUExJHHpv8Ln13Cq5RbeA93m-09K4BC325J5CZZr8IikEpXX3aD0fcswCN5WFwrHp2_uFx9yLEoBCds-hgN2o6k6rTVilo1rNbEClePjklustGWVC-GE4fMbg"
    
    # Test samples - one of each type
    test_samples = [
        # 1. Reference sample (normal-1, no emotion)
        {
            'text': "This is a reference sample for voice calibration and testing.",
            'actor_id': "688b02990486383d463c9d1a",
            'style_label': "normal-1",
            'emotion_scale': 1.0,
            'filename': 'test_reference.wav'
        },
        
        # 2. Style-based emotion (angry)
        {
            'text': "I can't believe you broke your promise again after everything we discussed!",
            'actor_id': "688b02990486383d463c9d1a",
            'style_label': "style-2",  # angry style
            'emotion_scale': 1.5,
            'filename': 'test_angry_style.wav'
        },
        
        # 3. Audio-based emotion vector (excited)
        {
            'text': "We're going on the adventure of a lifetime starting tomorrow morning!",
            'actor_id': "688b02990486383d463c9d1a",
            'style_label': "normal-1",
            'emotion_vector_id': "68a6b0ca2edfc11a25045538",  # excited
            'emotion_scale': 2.0,
            'filename': 'test_excited_vector.wav'
        },
        
        # 4. Prompt-based emotion vector (fear)
        {
            'text': "I'm really scared about what might happen if this goes wrong.",
            'actor_id': "688b02990486383d463c9d1a", 
            'style_label': "normal-1",
            'emotion_vector_id': "68a6b0f7b436060efdc6bc83",  # fear
            'emotion_scale': 2.5,
            'filename': 'test_fear_vector.wav'
        }
    ]
    
    print(f"Testing {len(test_samples)} samples:")
    for i, sample in enumerate(test_samples, 1):
        print(f"  {i}. {sample['filename']} - ", end="")
        if sample['style_label'] != 'normal-1':
            print(f"Style: {sample['style_label']}")
        elif 'emotion_vector_id' in sample:
            print(f"Emotion Vector: {sample['emotion_vector_id'][:8]}...")
        else:
            print("Reference (normal-1)")
    
    # Initialize API client
    client = TTSAPIClient(token)
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    
    # Generate the test batch
    print(f"\nGenerating test samples...")
    success, failed = client.generate_audio_batch(test_samples, output_dir)
    
    # Analyze results
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    print(f"Success: {success}/{len(test_samples)}")
    print(f"Failed: {failed}")
    
    if success == len(test_samples):
        print("🎉 ALL TEST SAMPLES GENERATED SUCCESSFULLY!")
        
        # Check file sizes
        print("\nGenerated files:")
        for sample in test_samples:
            file_path = output_dir / sample['filename']
            if file_path.exists():
                size_kb = file_path.stat().st_size / 1024
                print(f"  ✓ {sample['filename']}: {size_kb:.1f} KB")
            else:
                print(f"  ✗ {sample['filename']}: Missing")
        
        print("\n✅ Ready to generate all 438 samples!")
        return True
    
    else:
        print("❌ Some test samples failed. Check the issues before proceeding.")
        return False

def check_existing_files():
    """Check what files already exist"""
    
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    
    if not output_dir.exists():
        print("No voices directory found.")
        return
    
    wav_files = list(output_dir.glob('*.wav'))
    
    if not wav_files:
        print("No audio files found.")
        return
    
    print(f"\nExisting audio files: {len(wav_files)}")
    
    # Categorize by size (rough heuristic)
    mock_files = []
    real_files = []
    
    for f in wav_files:
        size = f.stat().st_size
        if size < 200_000:  # Less than 200KB likely mock
            mock_files.append(f)
        else:
            real_files.append(f)
    
    print(f"  Mock files (< 200KB): {len(mock_files)}")
    print(f"  Real files (≥ 200KB): {len(real_files)}")
    
    if real_files:
        print("  Recent real files:")
        for f in sorted(real_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
            size_kb = f.stat().st_size / 1024
            print(f"    {f.name}: {size_kb:.1f} KB")

def main():
    """Main execution"""
    
    # Check existing files first
    check_existing_files()
    
    # Run the test
    success = test_small_batch()
    
    if success:
        print("\n" + "="*70)
        print("NEXT STEPS")
        print("="*70)
        print("Test successful! You can now run the full generation:")
        print()
        print("  # Conservative (5 per batch, ~70 minutes)")
        print("  python3 scripts/generate_all_real_samples.py 5 --confirm")
        print()
        print("  # Faster (10 per batch, ~35 minutes)")  
        print("  python3 scripts/generate_all_real_samples.py 10 --confirm")
    else:
        print("\n❌ Fix the issues before running full generation.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)