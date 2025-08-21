#!/usr/bin/env python3
"""
Test script to verify API request format for different sample types
"""

import json
from pathlib import Path

def test_api_requests():
    """Test and display API request formats"""
    
    # Load generated API requests
    requests_file = Path(__file__).parent.parent / 'data' / 'api_requests.json'
    with open(requests_file, 'r', encoding='utf-8') as f:
        api_requests = json.load(f)
    
    print("="*70)
    print("API Request Format Verification")
    print("="*70)
    
    # Group samples by type
    reference_samples = []
    style_samples = []
    audio_vector_samples = []
    prompt_vector_samples = []
    
    for item in api_requests:
        filename = item['filename']
        request = item['request']
        
        if '_ref_' in filename:
            reference_samples.append(item)
        elif '_ang_' in filename or '_sad_' in filename or '_hap_' in filename or \
             '_whi_' in filename or '_tup_' in filename or '_tdn_' in filename:
            style_samples.append(item)
        elif '_exc_' in filename or '_fur_' in filename or '_ter_' in filename:
            audio_vector_samples.append(item)
        elif '_fea_' in filename or '_sur_' in filename or '_exm_' in filename:
            prompt_vector_samples.append(item)
    
    # Display examples from each type
    print("\n1. REFERENCE SAMPLES (should have style_label='normal-1', no emotion_vector_id)")
    print("-" * 50)
    for item in reference_samples[:2]:
        print(f"\nFilename: {item['filename']}")
        req = item['request']
        print(f"  style_label: {req.get('style_label', 'NOT SET')}")
        print(f"  emotion_vector_id: {req.get('emotion_vector_id', 'NOT SET')}")
        print(f"  emotion_scale: {req.get('emotion_scale', 'NOT SET')}")
    
    print("\n2. STYLE-BASED EMOTIONS (should have specific style_label, no emotion_vector_id)")
    print("-" * 50)
    for item in style_samples[:3]:
        print(f"\nFilename: {item['filename']}")
        req = item['request']
        print(f"  style_label: {req.get('style_label', 'NOT SET')}")
        print(f"  emotion_vector_id: {req.get('emotion_vector_id', 'NOT SET')}")
        print(f"  emotion_scale: {req.get('emotion_scale', 'NOT SET')}")
        print(f"  text: {req['text'][:50]}...")
    
    print("\n3. AUDIO-BASED EMOTION VECTORS (should have style_label='normal-1' + emotion_vector_id)")
    print("-" * 50)
    for item in audio_vector_samples[:3]:
        print(f"\nFilename: {item['filename']}")
        req = item['request']
        print(f"  style_label: {req.get('style_label', 'NOT SET')}")
        print(f"  emotion_vector_id: {req.get('emotion_vector_id', 'NOT SET')}")
        print(f"  emotion_scale: {req.get('emotion_scale', 'NOT SET')}")
        print(f"  text: {req['text'][:50]}...")
    
    print("\n4. PROMPT-BASED EMOTION VECTORS (should have style_label='normal-1' + emotion_vector_id)")
    print("-" * 50)
    for item in prompt_vector_samples[:3]:
        print(f"\nFilename: {item['filename']}")
        req = item['request']
        print(f"  style_label: {req.get('style_label', 'NOT SET')}")
        print(f"  emotion_vector_id: {req.get('emotion_vector_id', 'NOT SET')}")
        print(f"  emotion_scale: {req.get('emotion_scale', 'NOT SET')}")
        print(f"  text: {req['text'][:50]}...")
    
    # Summary statistics
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total requests: {len(api_requests)}")
    print(f"Reference samples: {len(reference_samples)}")
    print(f"Style-based samples: {len(style_samples)}")
    print(f"Audio vector samples: {len(audio_vector_samples)}")
    print(f"Prompt vector samples: {len(prompt_vector_samples)}")
    
    # Validate consistency
    print("\n" + "="*70)
    print("VALIDATION")
    print("="*70)
    
    errors = []
    
    # Check reference samples
    for item in reference_samples:
        req = item['request']
        if req.get('style_label') != 'normal-1':
            errors.append(f"Reference {item['filename']} should have style_label='normal-1'")
        if 'emotion_vector_id' in req:
            errors.append(f"Reference {item['filename']} should not have emotion_vector_id")
    
    # Check style samples
    for item in style_samples:
        req = item['request']
        if req.get('style_label') == 'normal-1':
            errors.append(f"Style sample {item['filename']} should not have style_label='normal-1'")
        if 'emotion_vector_id' in req:
            errors.append(f"Style sample {item['filename']} should not have emotion_vector_id")
    
    # Check emotion vector samples
    for item in audio_vector_samples + prompt_vector_samples:
        req = item['request']
        if req.get('style_label') != 'normal-1':
            errors.append(f"Emotion vector {item['filename']} should have style_label='normal-1'")
        if 'emotion_vector_id' not in req:
            errors.append(f"Emotion vector {item['filename']} missing emotion_vector_id")
    
    if errors:
        print("✗ ERRORS FOUND:")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    else:
        print("✓ All API requests are correctly formatted!")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = test_api_requests()
    if not success:
        print("\nPlease regenerate the samples to fix the errors.")
        print("Run: python3 scripts/generate_samples.py")
    else:
        print("\nReady to generate audio samples!")
        print("Run: python3 scripts/batch_generate.py --endpoint YOUR_API_ENDPOINT")