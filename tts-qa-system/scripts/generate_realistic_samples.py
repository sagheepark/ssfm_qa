#!/usr/bin/env python3
"""
Generate realistic TTS samples based on actual API capabilities:
- Only style_label: 'normal-1' supported
- emotion_scale: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0 supported
- Focus on testing emotion_scale impact with different texts
"""

import json
import time
import sys
from pathlib import Path
from tts_api_client import TTSAPIClient

def create_realistic_samples():
    """Create samples that work with the actual API"""
    
    # Test sentences from tts-test-sentences.md 
    test_sentences = {
        "neutral": [
            "The meeting is scheduled for three o'clock in the conference room.",
            "The report needs to be submitted by Friday afternoon without fail.",
            "Please remember to turn off the lights when you leave the office.",
            "The quarterly financial report shows steady growth in all departments.",
            "The train arrives at platform seven every hour on weekdays.",
            "The document contains information about the new policy changes."
        ],
        "emotional": [
            "I can't believe you broke your promise again after everything we discussed!",
            "I really miss the old days when everyone was still here together.",
            "I'm so thrilled about the wonderful surprise party you organized for me!",
            "Don't make any noise, everyone is sleeping in the next room.",
            "Did you really win the grand prize in the competition?",
            "Let me explain this matter in a very serious and professional manner."
        ],
        "intense": [
            "Your thoughtfulness and kindness truly made my day so much better.",
            "This is absolutely the best news I've heard all year long!",
            "Everything seems to be going wrong and nothing works out anymore.",
            "Everyone needs to hear this important announcement right now!",
            "Everything is perfectly calm and there's nothing to worry about here.",
            "This is so incredibly exciting and I can barely contain myself!"
        ]
    }
    
    # Realistic test matrix
    voice_ids = ["voice_001", "voice_002"]
    emotion_scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    
    samples = []
    
    # Generate samples
    for voice_id in voice_ids:
        # Map to actual actor_id
        actor_id = "688b02990486383d463c9d1a"  # From working example
        
        # Reference samples (scale 1.0, neutral text)
        samples.append({
            'text': "This is a reference sample for voice calibration and testing.",
            'actor_id': actor_id,
            'style_label': "normal-1",
            'emotion_scale': 1.0,
            'filename': f'{voice_id}_ref.wav',
            'category': 'reference'
        })
        
        # Test different emotion scales with different text types
        for scale in emotion_scales:
            for text_type, sentences in test_sentences.items():
                for i, text in enumerate(sentences):
                    samples.append({
                        'text': text,
                        'actor_id': actor_id,
                        'style_label': "normal-1",
                        'emotion_scale': scale,
                        'filename': f'{voice_id}_{text_type}{i+1}_scale{scale}.wav',
                        'category': f'{text_type}_scale_{scale}'
                    })
    
    return samples

def generate_samples_batch(token: str, batch_size: int = 8, max_samples: int = None):
    """Generate realistic samples in batches"""
    
    print("="*70)
    print("GENERATING REALISTIC TTS SAMPLES")
    print("="*70)
    
    # Create sample list
    all_samples = create_realistic_samples()
    
    if max_samples:
        all_samples = all_samples[:max_samples]
    
    print(f"Total samples to generate: {len(all_samples)}")
    print(f"Batch size: {batch_size}")
    
    # Show sample distribution
    categories = {}
    for sample in all_samples:
        cat = sample['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nSample distribution:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} samples")
    
    # Initialize API client
    client = TTSAPIClient(token)
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    
    # Clear old files
    print(f"\nCleaning old files...")
    old_files = list(output_dir.glob('*.wav'))
    for f in old_files:
        if f.stat().st_size < 300_000:  # Remove mock files
            f.unlink()
            print(f"  Removed: {f.name}")
    
    # Process in batches
    total_success = 0
    total_failed = 0
    
    for batch_idx in range(0, len(all_samples), batch_size):
        batch_samples = all_samples[batch_idx:batch_idx + batch_size]
        batch_num = (batch_idx // batch_size) + 1
        
        print(f"\n{'='*50}")
        print(f"BATCH {batch_num}: Samples {batch_idx + 1}-{min(batch_idx + batch_size, len(all_samples))}")
        print(f"{'='*50}")
        
        # Show sample info
        for i, sample in enumerate(batch_samples):
            print(f"  {i+1}. {sample['filename']} (scale: {sample['emotion_scale']})")
            print(f"      Text: {sample['text'][:60]}...")
        
        # Generate batch
        success, failed = client.generate_audio_batch(batch_samples, output_dir)
        
        total_success += success
        total_failed += failed
        
        print(f"\nBatch {batch_num} result: {success}/{len(batch_samples)} successful")
        print(f"Running total: {total_success}/{total_success + total_failed}")
        
        # Brief pause between batches
        if batch_idx + batch_size < len(all_samples):
            print(f"Pausing 3 seconds before next batch...")
            time.sleep(3)
    
    # Final summary
    print("\n" + "="*70)
    print("GENERATION COMPLETE")
    print("="*70)
    print(f"Total successful: {total_success}/{len(all_samples)}")
    print(f"Total failed: {total_failed}")
    print(f"Success rate: {total_success/len(all_samples)*100:.1f}%")
    
    # Check generated files
    generated_files = list(output_dir.glob('*.wav'))
    real_files = [f for f in generated_files if f.stat().st_size > 200_000]
    
    print(f"\nGenerated files: {len(real_files)}")
    print(f"Average file size: {sum(f.stat().st_size for f in real_files) / len(real_files) / 1024:.1f} KB" if real_files else "N/A")
    
    # Sample analysis
    if real_files:
        print(f"\nSample files by emotion scale:")
        scale_files = {}
        for f in real_files:
            if 'scale' in f.name:
                scale = f.name.split('scale')[1].split('.')[0]
                scale_files[scale] = scale_files.get(scale, 0) + 1
        
        for scale in sorted(scale_files.keys(), key=float):
            print(f"  Scale {scale}: {scale_files[scale]} files")
    
    success_rate = total_success / len(all_samples)
    return success_rate > 0.9  # 90% success threshold

def main():
    """Main execution"""
    
    # Token from working example
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWMwMWU5YzhkMzc5M2NmNDBlMmJlMjkiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJoYXNfYWRtaW5fcGVybWlzc2lvbl9zY29wZSI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3R5cGVjYXN0LWE0YzhmIiwiYXVkIjoidHlwZWNhc3QtYTRjOGYiLCJhdXRoX3RpbWUiOjE3NTU1MzY4MDcsInVzZXJfaWQiOiJvQ21yajBPUzJJVmpQMjFxb2QyRlZGdTJsR2QyIiwic3ViIjoib0NtcmowT1MySVZqUDIxcW9kMkZWRnUybEdkMiIsImlhdCI6MTc1NTc1OTA3NSwiZXhwIjoxNzU1NzYyNjc1LCJlbWFpbCI6InNhbmdnb29AbmVvc2FwaWVuY2UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdnb29AbmVvc2FwaWVuY2UuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.UG__H6qnbLRROq3G_LW96n4Yz4iKSEdAZ0v0f9PJOXk382X8M3qSlbMyrk6lnnLQ4iJd2RjbM30lY--i4FRhaL5szeeQTorRU4sdfaKZ7RHhRZw66__5yZlALHbXEZBHmKI0bpr1X_am1VkoohiwKbCHT34VVb_tYK_6YWRtQIe0VTyeD94XOaIsQFJ5NeOCic-UHUXaV8k3IZGQ_sMBg9scaP6DvqUExJHHpv8Ln13Cq5RbeA93m-09K4BC325J5CZZr8IikEpXX3aD0fcswCN5WFwrHp2_uFx9yLEoBCds-hgN2o6k6rTVilo1rNbEClePjklustGWVC-GE4fMbg"
    
    # Get parameters
    batch_size = 6  # Conservative
    max_samples = None  # Generate all
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            max_samples = 12  # Just test first 12 samples
            print("🧪 TEST MODE: Generating only first 12 samples")
        else:
            try:
                batch_size = int(sys.argv[1])
            except ValueError:
                print("Invalid batch size, using default: 6")
    
    # Show what we'll generate
    all_samples = create_realistic_samples()
    if max_samples:
        all_samples = all_samples[:max_samples]
    
    print(f"Will generate {len(all_samples)} samples with batch size {batch_size}")
    estimated_time = (len(all_samples) / batch_size) * 10  # ~10 seconds per batch
    print(f"Estimated time: {estimated_time/60:.1f} minutes")
    
    # Confirm
    if "--test" not in sys.argv and len(sys.argv) < 2:
        response = input(f"\nProceed with generating {len(all_samples)} samples? (y/N): ")
        if response.lower() != 'y':
            print("Generation cancelled.")
            return False
    
    # Generate
    start_time = time.time()
    success = generate_samples_batch(token, batch_size, max_samples)
    elapsed = time.time() - start_time
    
    print(f"\nTotal time: {elapsed/60:.1f} minutes")
    
    if success:
        print("🎉 SUCCESS: Realistic TTS sample generation completed!")
        print("\nNOTE: These samples only vary by emotion_scale (0.5-3.0)")
        print("This tests how emotion intensity affects the same voice and text")
    else:
        print("⚠ Some issues occurred during generation")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)