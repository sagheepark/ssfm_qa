#!/usr/bin/env python3
"""
Test only the emotion configurations we know work:
- normal-1 style (reference)
- emotion_vector_id with different scales
"""

import json
import sys
from pathlib import Path
from tts_api_client import TTSAPIClient

def test_valid_configurations():
    """Test only configurations that should work based on the notebook"""
    
    print("="*70)
    print("TESTING VALID EMOTION CONFIGURATIONS")
    print("="*70)
    
    # Token from working example
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWMwMWU5YzhkMzc5M2NmNDBlMmJlMjkiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJoYXNfYWRtaW5fcGVybWlzc2lvbl9zY29wZSI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3R5cGVjYXN0LWE0YzhmIiwiYXVkIjoidHlwZWNhc3QtYTRjOGYiLCJhdXRoX3RpbWUiOjE3NTU1MzY4MDcsInVzZXJfaWQiOiJvQ21yajBPUzJJVmpQMjFxb2QyRlZGdTJsR2QyIiwic3ViIjoib0NtcmowT1MySVZqUDIxcW9kMkZWRnUybEdkMiIsImlhdCI6MTc1NTc1OTA3NSwiZXhwIjoxNzU1NzYyNjc1LCJlbWFpbCI6InNhbmdnb29AbmVvc2FwaWVuY2UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdnb29AbmVvc2FwaWVuY2UuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.UG__H6qnbLRROq3G_LW96n4Yz4iKSEdAZ0v0f9PJOXk382X8M3qSlbMyrk6lnnLQ4iJd2RjbM30lY--i4FRhaL5szeeQTorRU4sdfaKZ7RHhRZw66__5yZlALHbXEZBHmKI0bpr1X_am1VkoohiwKbCHT34VVb_tYK_6YWRtQIe0VTyeD94XOaIsQFJ5NeOCic-UHUXaV8k3IZGQ_sMBg9scaP6DvqUExJHHpv8Ln13Cq5RbeA93m-09K4BC325J5CZZr8IikEpXX3aD0fcswCN5WFwrHp2_uFx9yLEoBCds-hgN2o6k6rTVilo1rNbEClePjklustGWVC-GE4fMbg"
    
    # Test samples - only valid configurations
    test_samples = [
        # 1. Reference sample (normal-1, no emotion) - KNOWN TO WORK
        {
            'text': "This is a reference sample for voice calibration and testing.",
            'actor_id': "688b02990486383d463c9d1a",
            'style_label': "normal-1",
            'emotion_scale': 1.0,
            'filename': 'test_ref_valid.wav'
        },
        
        # 2. Emotion vector - excited, scale 1.0
        {
            'text': "We're going on the adventure of a lifetime starting tomorrow morning!",
            'actor_id': "688b02990486383d463c9d1a",
            'style_label': "normal-1",
            'emotion_vector_id': "68a6b0ca2edfc11a25045538",  # excited
            'emotion_scale': 1.0,
            'filename': 'test_excited_1.0.wav'
        },
        
        # 3. Emotion vector - excited, scale 2.0
        {
            'text': "We're going on the adventure of a lifetime starting tomorrow morning!",
            'actor_id': "688b02990486383d463c9d1a",
            'style_label': "normal-1",
            'emotion_vector_id': "68a6b0ca2edfc11a25045538",  # excited
            'emotion_scale': 2.0,
            'filename': 'test_excited_2.0.wav'
        },
        
        # 4. Different emotion vector - fear
        {
            'text': "I'm really scared about what might happen if this goes wrong.",
            'actor_id': "688b02990486383d463c9d1a",
            'style_label': "normal-1",
            'emotion_vector_id': "68a6b0f7b436060efdc6bc83",  # fear
            'emotion_scale': 1.5,
            'filename': 'test_fear_1.5.wav'
        }
    ]
    
    print(f"Testing {len(test_samples)} valid configurations:")
    for i, sample in enumerate(test_samples, 1):
        print(f"  {i}. {sample['filename']}")
        print(f"     Text: {sample['text'][:50]}...")
        print(f"     Style: {sample['style_label']}")
        if 'emotion_vector_id' in sample:
            print(f"     Emotion Vector: {sample['emotion_vector_id'][:8]}...")
            print(f"     Scale: {sample['emotion_scale']}")
        print()
    
    # Initialize API client
    client = TTSAPIClient(token)
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    
    # Generate the test batch
    print(f"Generating test samples...")
    success, failed = client.generate_audio_batch(test_samples, output_dir)
    
    # Analyze results
    print("\n" + "="*70)
    print("VALIDATION RESULTS")
    print("="*70)
    print(f"Success: {success}/{len(test_samples)}")
    print(f"Failed: {failed}")
    
    if success == len(test_samples):
        print("🎉 ALL VALID CONFIGURATIONS WORKING!")
        
        # Check file sizes and differences
        print("\nGenerated files:")
        for sample in test_samples:
            file_path = output_dir / sample['filename']
            if file_path.exists():
                size_kb = file_path.stat().st_size / 1024
                print(f"  ✓ {sample['filename']}: {size_kb:.1f} KB")
            else:
                print(f"  ✗ {sample['filename']}: Missing")
        
        print("\n✅ Emotion vectors and scales are working!")
        print("❗ Style labels (style-2, style-3, etc.) are NOT supported by this API")
        print("🔄 Need to revise the plan to use only emotion_vector_id for emotions")
        return True
    
    else:
        print("❌ Some valid configurations failed.")
        return False

def main():
    """Main execution"""
    
    success = test_valid_configurations()
    
    if success:
        print("\n" + "="*70)
        print("CONCLUSION")
        print("="*70)
        print("✅ API supports:")
        print("   - style_label: 'normal-1' (reference/baseline)")
        print("   - emotion_vector_id with various emotion_scale values")
        print()
        print("❌ API does NOT support:")
        print("   - Custom style_label values (style-2, style-3, etc.)")
        print()
        print("📝 REVISED APPROACH:")
        print("   - Use only emotion_vector_id for all emotions")
        print("   - Generate multiple scales (0.5, 1.0, 1.5, 2.0, 2.5, 3.0) for each emotion")
        print("   - Skip style-based emotions from tts-test-sentences.md")
        print("   - Focus on the 6 emotion vectors we have IDs for")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)