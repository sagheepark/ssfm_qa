#!/usr/bin/env python3
"""
Test both emotion_label and emotion_vector_id from tts-test-sentences.md
"""

import requests
import json
import time
from pathlib import Path

def test_emotion_labels_and_vectors():
    """Test the actual emotion labels and vector IDs from the test sentences file"""
    
    print("="*70)
    print("TESTING EMOTION LABELS AND VECTOR IDs")
    print("="*70)
    
    # Token from working example
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2MzM2OSwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU1NzYzMzY5LCJleHAiOjE3NTU3NjY5NjksImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.EScBGAzSA87MnXRAPsnvwq6Ejbpf3xgfZQvmmM9kf32X49WNKyp4LoLjxmmTXmcY0C66AV4cXkyTdlS89IoD5cgrTw3KdkAPFhLbEnkj5iR18qQuELtND3XV5bFVvgbVLrRD18lrQTd-G09CmU23qmBnNEzAQ6CcEVphTe-8JEqPAGRrepMjP3heWV3UgMDpXe3SmYT5dNHAL_mCpUNFLG7-j8zezu8U8QGqGti_v7agCI-q3Y5dZvxTG3-tIT293wlsVZ_diJMS9sCw5e-Y4pwoyzeeXobgxl2TfyuacF0QIk2eN8L7KsPWWInzDzMUj6ms4IWhIIKS4BnGyGdWgA"
    
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://dev.icepeak.ai"
    
    # Test cases from tts-test-sentences.md
    test_cases = [
        # Test emotion_label cases
        {
            "name": "emotion_label: Angry",
            "request": {
                "text": "I can't believe you broke your promise again after everything we discussed!",
                "actor_id": "688b02990486383d463c9d1a",
                "style_label": "normal-1",
                "emotion_label": "Angry",
                "emotion_scale": 1.5,
                "tempo": 1,
                "pitch": 0,
                "lang": "auto",
                "mode": "one-vocoder",
                "retake": True,
                "adjust_lastword": 0,
                "style_label_version": "v1"
            }
        },
        {
            "name": "emotion_label: Happy",
            "request": {
                "text": "I'm so thrilled about the wonderful surprise party you organized for me!",
                "actor_id": "688b02990486383d463c9d1a",
                "style_label": "normal-1",
                "emotion_label": "Happy",
                "emotion_scale": 2.0,
                "tempo": 1,
                "pitch": 0,
                "lang": "auto",
                "mode": "one-vocoder",
                "retake": True,
                "adjust_lastword": 0,
                "style_label_version": "v1"
            }
        },
        {
            "name": "emotion_label: Sad",
            "request": {
                "text": "I really miss the old days when everyone was still here together.",
                "actor_id": "688b02990486383d463c9d1a",
                "style_label": "normal-1",
                "emotion_label": "Sad",
                "emotion_scale": 1.8,
                "tempo": 1,
                "pitch": 0,
                "lang": "auto",
                "mode": "one-vocoder",
                "retake": True,
                "adjust_lastword": 0,
                "style_label_version": "v1"
            }
        },
        
        # Test emotion_vector_id cases (emotion_label should be None/empty)
        {
            "name": "emotion_vector_id: Excited",
            "request": {
                "text": "We're going on the adventure of a lifetime starting tomorrow morning!",
                "actor_id": "688b02990486383d463c9d1a",
                "style_label": "normal-1",
                "emotion_label": None,
                "emotion_vector_id": "68a6b0ca2edfc11a25045538",
                "emotion_scale": 2.0,
                "tempo": 1,
                "pitch": 0,
                "lang": "auto",
                "mode": "one-vocoder",
                "retake": True,
                "adjust_lastword": 0,
                "style_label_version": "v1"
            }
        },
        {
            "name": "emotion_vector_id: Furious",
            "request": {
                "text": "This is absolutely unacceptable and I demand an explanation immediately!",
                "actor_id": "688b02990486383d463c9d1a",
                "style_label": "normal-1",
                "emotion_label": None,
                "emotion_vector_id": "68a6b0d2b436060efdc6bc80",
                "emotion_scale": 2.5,
                "tempo": 1,
                "pitch": 0,
                "lang": "auto",
                "mode": "one-vocoder",
                "retake": True,
                "adjust_lastword": 0,
                "style_label_version": "v1"
            }
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"   Text: {test_case['request']['text'][:50]}...")
        
        # Show request details
        if test_case['request'].get('emotion_label'):
            print(f"   emotion_label: {test_case['request']['emotion_label']}")
        if test_case['request'].get('emotion_vector_id'):
            print(f"   emotion_vector_id: {test_case['request']['emotion_vector_id'][:8]}...")
        print(f"   emotion_scale: {test_case['request']['emotion_scale']}")
        
        try:
            response = requests.post(
                f"{base_url}/api/speak/batch/post", 
                headers=headers, 
                json=[test_case['request']],  # Wrap in array
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"   ✓ SUCCESS")
                results.append((test_case['name'], True, "OK"))
            else:
                error_msg = response.json().get('message', {}).get('msg', 'unknown error')
                print(f"   ✗ FAILED: {response.status_code} - {error_msg}")
                results.append((test_case['name'], False, error_msg))
                
        except Exception as e:
            print(f"   ✗ ERROR: {str(e)}")
            results.append((test_case['name'], False, str(e)))
    
    # Summary
    print("\n" + "="*70)
    print("TEST RESULTS SUMMARY")
    print("="*70)
    
    emotion_label_results = []
    emotion_vector_results = []
    
    for name, success, message in results:
        if "emotion_label:" in name:
            emotion_label_results.append((name, success, message))
        else:
            emotion_vector_results.append((name, success, message))
    
    print("emotion_label tests:")
    for name, success, message in emotion_label_results:
        status = "✓" if success else "✗"
        print(f"  {status} {name}")
        if not success:
            print(f"    Error: {message}")
    
    print("\nemotion_vector_id tests:")
    for name, success, message in emotion_vector_results:
        status = "✓" if success else "✗"
        print(f"  {status} {name}")
        if not success:
            print(f"    Error: {message}")
    
    # Conclusion
    emotion_label_works = any(success for name, success, _ in emotion_label_results)
    emotion_vector_works = any(success for name, success, _ in emotion_vector_results)
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    
    if emotion_label_works:
        print("✅ emotion_label is supported by the API")
        working_labels = [name.split(": ")[1] for name, success, _ in emotion_label_results if success]
        print(f"   Working emotion_labels: {working_labels}")
    else:
        print("❌ emotion_label is NOT supported by the API")
    
    if emotion_vector_works:
        print("✅ emotion_vector_id is supported by the API")
        working_vectors = [name.split(": ")[1] for name, success, _ in emotion_vector_results if success]
        print(f"   Working emotion_vector_ids: {working_vectors}")
    else:
        print("❌ emotion_vector_id is NOT supported by the API")
    
    if emotion_label_works or emotion_vector_works:
        print("\n🎉 We can proceed with generating emotional TTS samples!")
        return True
    else:
        print("\n😞 Only basic 'normal-1' style is available")
        return False

if __name__ == "__main__":
    test_emotion_labels_and_vectors()