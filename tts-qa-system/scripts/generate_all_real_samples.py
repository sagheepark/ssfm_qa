#!/usr/bin/env python3
"""
Generate all 438 real TTS samples using the proper API workflow
Based on TDD approach and the working API client
"""

import json
import time
import sys
from pathlib import Path
from tts_api_client import TTSAPIClient

def load_sample_metadata():
    """Load the generated sample metadata"""
    metadata_file = Path(__file__).parent.parent / 'data' / 'sample_metadata.json'
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_samples_for_api(samples: list) -> list:
    """Convert sample metadata to API format"""
    
    api_samples = []
    
    for sample in samples:
        # Map voice_id to actual actor_id (from notebook example)
        actor_id_map = {
            'voice_001': '688b02990486383d463c9d1a',  # From working example
            'voice_002': '688b02990486383d463c9d1a'   # Use same for now, can be updated
        }
        
        api_sample = {
            'text': sample['text'],
            'actor_id': actor_id_map.get(sample['voice_id'], '688b02990486383d463c9d1a'),
            'style_label': 'normal-1',  # Default
            'emotion_scale': sample.get('scale', 1.0),
            'filename': sample['filename']
        }
        
        # Handle different emotion types
        if sample['type'] == 'style':
            # Map emotion names to style labels
            style_map = {
                'angry': 'style-2',
                'sad': 'style-3', 
                'happy': 'style-4',
                'whisper': 'style-5',
                'toneup': 'style-6',
                'tonedown': 'style-7'
            }
            emotion_name = sample.get('emotion', '')
            api_sample['style_label'] = style_map.get(emotion_name, 'normal-1')
            
        elif sample['type'] in ['audio', 'prompt']:
            # Use emotion vector ID
            emotion_vector_map = {
                'excited': '68a6b0ca2edfc11a25045538',
                'furious': '68a6b0d2b436060efdc6bc80', 
                'terrified': '68a6b0d9b436060efdc6bc82',
                'fear': '68a6b0f7b436060efdc6bc83',
                'surprise': '68a6b10255e3b2836e609969',
                'excitement': '68a6b1062edfc11a2504553b'
            }
            emotion_name = sample.get('emotion', '')
            emotion_vector_id = emotion_vector_map.get(emotion_name)
            if emotion_vector_id:
                api_sample['emotion_vector_id'] = emotion_vector_id
        
        api_samples.append(api_sample)
    
    return api_samples

def generate_samples_in_batches(token: str, batch_size: int = 10):
    """Generate all samples in manageable batches"""
    
    print("="*70)
    print("GENERATING ALL 438 REAL TTS SAMPLES")
    print("="*70)
    
    # Load sample metadata
    metadata = load_sample_metadata()
    all_samples = metadata['samples']
    
    print(f"Total samples to generate: {len(all_samples)}")
    print(f"Batch size: {batch_size}")
    print(f"Estimated batches: {(len(all_samples) + batch_size - 1) // batch_size}")
    
    # Convert to API format
    api_samples = convert_samples_for_api(all_samples)
    
    # Initialize API client
    client = TTSAPIClient(token)
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    
    # Remove old mock files first
    print(f"\nCleaning old mock files...")
    mock_files = list(output_dir.glob('*.wav'))
    for f in mock_files:
        if f.stat().st_size < 300_000:  # Less than 300KB likely mock
            f.unlink()
            print(f"  Removed mock: {f.name}")
    
    # Process in batches
    total_success = 0
    total_failed = 0
    
    for batch_idx in range(0, len(api_samples), batch_size):
        batch_samples = api_samples[batch_idx:batch_idx + batch_size]
        batch_num = (batch_idx // batch_size) + 1
        
        print(f"\n{'='*50}")
        print(f"BATCH {batch_num}: Samples {batch_idx + 1}-{min(batch_idx + batch_size, len(api_samples))}")
        print(f"{'='*50}")
        
        # Show sample types in this batch
        types_in_batch = {}
        for sample in batch_samples:
            sample_type = "reference" if "_ref_" in sample['filename'] else \
                         "style" if sample.get('style_label') != 'normal-1' else \
                         "emotion_vector"
            types_in_batch[sample_type] = types_in_batch.get(sample_type, 0) + 1
        
        print(f"Batch composition: {types_in_batch}")
        
        # Generate batch
        success, failed = client.generate_audio_batch(batch_samples, output_dir)
        
        total_success += success
        total_failed += failed
        
        print(f"Batch {batch_num} result: {success}/{len(batch_samples)} successful")
        print(f"Running total: {total_success}/{total_success + total_failed}")
        
        # Brief pause between batches to be nice to the API
        if batch_idx + batch_size < len(api_samples):
            print(f"Pausing 2 seconds before next batch...")
            time.sleep(2)
    
    # Final summary
    print("\n" + "="*70)
    print("GENERATION COMPLETE")
    print("="*70)
    print(f"Total successful: {total_success}/{len(api_samples)}")
    print(f"Total failed: {total_failed}")
    print(f"Success rate: {total_success/len(api_samples)*100:.1f}%")
    
    # Verify files
    wav_files = list(output_dir.glob('*.wav'))
    real_files = [f for f in wav_files if f.stat().st_size > 200_000]  # Real TTS files
    
    print(f"\nGenerated audio files: {len(real_files)}")
    print(f"Expected: {len(api_samples)}")
    
    if len(real_files) >= len(api_samples) * 0.95:  # 95% success threshold
        print("🎉 SUCCESS: Generation completed successfully!")
        return True
    else:
        print("⚠ Some samples may have failed. Check the output directory.")
        return False

def main():
    """Main execution"""
    
    # Token from the working example
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWMwMWU5YzhkMzc5M2NmNDBlMmJlMjkiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJoYXNfYWRtaW5fcGVybWlzc2lvbl9zY29wZSI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3R5cGVjYXN0LWE0YzhmIiwiYXVkIjoidHlwZWNhc3QtYTRjOGYiLCJhdXRoX3RpbWUiOjE3NTU1MzY4MDcsInVzZXJfaWQiOiJvQ21yajBPUzJJVmpQMjFxb2QyRlZGdTJsR2QyIiwic3ViIjoib0NtcmowT1MySVZqUDIxcW9kMkZWRnUybEdkMiIsImlhdCI6MTc1NTc1OTA3NSwiZXhwIjoxNzU1NzYyNjc1LCJlbWFpbCI6InNhbmdnb29AbmVvc2FwaWVuY2UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdnb29AbmVvc2FwaWVuY2UuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.UG__H6qnbLRROq3G_LW96n4Yz4iKSEdAZ0v0f9PJOXk382X8M3qSlbMyrk6lnnLQ4iJd2RjbM30lY--i4FRhaL5szeeQTorRU4sdfaKZ7RHhRZw66__5yZlALHbXEZBHmKI0bpr1X_am1VkoohiwKbCHT34VVb_tYK_6YWRtQIe0VTyeD94XOaIsQFJ5NeOCic-UHUXaV8k3IZGQ_sMBg9scaP6DvqUExJHHpv8Ln13Cq5RbeA93m-09K4BC325J5CZZr8IikEpXX3aD0fcswCN5WFwrHp2_uFx9yLEoBCds-hgN2o6k6rTVilo1rNbEClePjklustGWVC-GE4fMbg"
    
    # Get batch size from command line or use default
    batch_size = 5  # Conservative batch size for API stability
    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
        except ValueError:
            print("Invalid batch size, using default: 5")
    
    print(f"Starting generation with batch size: {batch_size}")
    
    # Estimate total time
    estimated_time = (438 / batch_size) * 8  # ~8 seconds per batch
    print(f"Estimated total time: {estimated_time/60:.1f} minutes")
    
    # Confirm before starting
    if len(sys.argv) < 2 or sys.argv[-1] != "--confirm":
        response = input("\nProceed with generating all 438 samples? (y/N): ")
        if response.lower() != 'y':
            print("Generation cancelled.")
            return False
    
    # Start generation
    start_time = time.time()
    success = generate_samples_in_batches(token, batch_size)
    elapsed = time.time() - start_time
    
    print(f"\nTotal time: {elapsed/60:.1f} minutes")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)