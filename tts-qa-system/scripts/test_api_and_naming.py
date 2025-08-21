#!/usr/bin/env python3
"""
Test script to verify API POST functionality and file naming rules
"""

import json
import yaml
import os
from pathlib import Path

def load_config():
    """Load configuration from YAML file"""
    config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_filename(voice_id, text_idx, variant_type, variant_value=None, scale=None):
    """
    Generate filename according to the naming rules:
    - Reference: {voice_id}_{text_idx}_ref.wav
    - Style variation: {voice_id}_{text_idx}_style_{style_name}.wav
    - Audio-based emotion: {voice_id}_{text_idx}_emo_audio{n}_scale_{scale}.wav
    - Prompt-based emotion: {voice_id}_{text_idx}_emo_prompt{n}_scale_{scale}.wav
    """
    
    if variant_type == 'reference':
        return f"{voice_id}_{text_idx}_ref.wav"
    elif variant_type == 'style':
        return f"{voice_id}_{text_idx}_style_{variant_value}.wav"
    elif variant_type == 'emotion_audio':
        return f"{voice_id}_{text_idx}_emo_audio{variant_value}_scale_{scale}.wav"
    elif variant_type == 'emotion_prompt':
        return f"{voice_id}_{text_idx}_emo_prompt{variant_value}_scale_{scale}.wav"
    else:
        raise ValueError(f"Unknown variant type: {variant_type}")

def create_api_request(config, voice_id, text, style_label="normal-1", 
                      emotion_vector_id=None, emotion_scale=1.0):
    """
    Create API request payload according to the specification
    """
    request = {
        "text": text,
        "actor_id": voice_id,
        "style_label": style_label,
        "emotion_scale": emotion_scale,
        "tempo": config['api_defaults']['tempo'],
        "pitch": config['api_defaults']['pitch'],
        "lang": config['api_defaults']['lang'],
        "mode": config['api_defaults']['mode'],
        "bp_c_l": config['api_defaults']['bp_c_l'],
        "retake": config['api_defaults']['retake'],
        "adjust_lastword": config['api_defaults']['adjust_lastword'],
        "style_label_version": config['api_defaults']['style_label_version']
    }
    
    # Add emotion_vector_id only if provided
    if emotion_vector_id:
        request["emotion_vector_id"] = emotion_vector_id
        request["style_label"] = "normal-1"  # Force normal-1 when using emotion_vector
    
    return request

def test_naming_rules():
    """Test all naming rule scenarios"""
    print("Testing Naming Rules:")
    print("=" * 50)
    
    test_cases = [
        # Reference
        {
            'params': {'voice_id': 'v001', 'text_idx': 't001', 'variant_type': 'reference'},
            'expected': 'v001_t001_ref.wav'
        },
        # Style variation
        {
            'params': {'voice_id': 'v001', 'text_idx': 't002', 'variant_type': 'style', 'variant_value': 'happy-1'},
            'expected': 'v001_t002_style_happy-1.wav'
        },
        # Audio-based emotion
        {
            'params': {'voice_id': 'v002', 'text_idx': 't003', 'variant_type': 'emotion_audio', 'variant_value': '1', 'scale': 1.5},
            'expected': 'v002_t003_emo_audio1_scale_1.5.wav'
        },
        # Prompt-based emotion
        {
            'params': {'voice_id': 'v002', 'text_idx': 't001', 'variant_type': 'emotion_prompt', 'variant_value': '2', 'scale': 2.0},
            'expected': 'v002_t001_emo_prompt2_scale_2.0.wav'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        result = generate_filename(**test['params'])
        status = "✓" if result == test['expected'] else "✗"
        print(f"Test {i}: {status}")
        print(f"  Expected: {test['expected']}")
        print(f"  Got:      {result}")
        if result != test['expected']:
            print(f"  ERROR: Mismatch!")
        print()

def test_api_requests():
    """Test API request generation for different scenarios"""
    print("\nTesting API Request Generation:")
    print("=" * 50)
    
    config = load_config()
    
    test_scenarios = [
        {
            'name': 'Reference (normal-1, no emotion_vector)',
            'params': {
                'voice_id': 'voice_001',
                'text': config['test_parameters']['texts'][0],
                'style_label': 'normal-1',
                'emotion_scale': 1.0
            }
        },
        {
            'name': 'Style variation (style-2)',
            'params': {
                'voice_id': 'voice_001',
                'text': config['test_parameters']['texts'][0],
                'style_label': 'style-2',
                'emotion_scale': 1.5
            }
        },
        {
            'name': 'Audio-based emotion vector',
            'params': {
                'voice_id': 'voice_001',
                'text': config['test_parameters']['texts'][0],
                'emotion_vector_id': config['test_parameters']['emotion_vectors']['audio_based'][0]['id'],
                'emotion_scale': 2.0
            }
        },
        {
            'name': 'Prompt-based emotion vector',
            'params': {
                'voice_id': 'voice_002',
                'text': config['test_parameters']['texts'][1],
                'emotion_vector_id': config['test_parameters']['emotion_vectors']['prompt_based'][0]['id'],
                'emotion_scale': 2.5
            }
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{scenario['name']}:")
        request = create_api_request(config, **scenario['params'])
        print(json.dumps(request, indent=2, ensure_ascii=False))

def test_sample_counts():
    """Calculate and verify total sample counts"""
    print("\nSample Count Verification:")
    print("=" * 50)
    
    config = load_config()
    
    n_voices = len(config['test_parameters']['voice_ids'])
    n_texts = len(config['test_parameters']['texts'])
    n_styles = len(config['test_parameters']['style_labels']) - 1  # Exclude normal-1
    n_audio_emotions = len(config['test_parameters']['emotion_vectors']['audio_based'])
    n_prompt_emotions = len(config['test_parameters']['emotion_vectors']['prompt_based'])
    n_scales = len(config['test_parameters']['emotion_scales'])
    
    # Calculate sample counts
    reference_samples = n_voices * n_texts
    style_samples = n_voices * n_texts * n_styles * n_scales
    audio_emotion_samples = n_voices * n_texts * n_audio_emotions * n_scales
    prompt_emotion_samples = n_voices * n_texts * n_prompt_emotions * n_scales
    
    total_samples = reference_samples + style_samples + audio_emotion_samples + prompt_emotion_samples
    
    print(f"Voice IDs: {n_voices}")
    print(f"Texts: {n_texts}")
    print(f"Style labels (excluding normal-1): {n_styles}")
    print(f"Audio-based emotions: {n_audio_emotions}")
    print(f"Prompt-based emotions: {n_prompt_emotions}")
    print(f"Emotion scales: {n_scales}")
    print()
    print(f"Reference samples: {reference_samples} = {n_voices} voices × {n_texts} texts")
    print(f"Style variations: {style_samples} = {n_voices} × {n_texts} × {n_styles} styles × {n_scales} scales")
    print(f"Audio emotion variations: {audio_emotion_samples} = {n_voices} × {n_texts} × {n_audio_emotions} emotions × {n_scales} scales")
    print(f"Prompt emotion variations: {prompt_emotion_samples} = {n_voices} × {n_texts} × {n_prompt_emotions} emotions × {n_scales} scales")
    print()
    print(f"TOTAL SAMPLES: {total_samples}")
    print()
    
    # Verify against expected
    expected_total = 438  # From plan.md
    if total_samples == expected_total:
        print(f"✓ Sample count matches expected: {expected_total}")
    else:
        print(f"✗ Sample count mismatch! Expected: {expected_total}, Got: {total_samples}")

def main():
    """Run all tests"""
    print("TTS QA System - API and Naming Rules Test")
    print("=" * 70)
    
    # Test naming rules
    test_naming_rules()
    
    # Test API request generation
    test_api_requests()
    
    # Verify sample counts
    test_sample_counts()
    
    print("\n" + "=" * 70)
    print("Test completed. Please review the output above.")
    print("\nNOTE: This is a dry run. No actual API calls were made.")
    print("Update the API endpoint in config.yaml before running the actual generation.")

if __name__ == "__main__":
    main()