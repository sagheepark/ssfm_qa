#!/usr/bin/env python3
"""
Test script for emotion_vector_id TTS generation
Tests the correct parameter configuration for emotion vectors
"""

import requests
import json
import time
from pathlib import Path

# Fresh token
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1NzkwNTI3LCJleHAiOjE3NTU3OTQxMjcsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.fFBDZnhMgpnMXwy0kDyCLasjY95I1b_PCHVptjznUI4fPI1eUBrR7caHQ3o_Uj6YQIE_5Uji6O-KsEwXZuJmtrfuQH1XeJjOcQdpNpjkyZfUY1_Y687SlDO9Sk0BqSMAAsEg8B5keCQg8F7nO4btk-XYKm_UGn1ANtbKMMMMd6aToJPMkEdJsmMUwW8UxNfMhL16JUZzWS6TvBCTSeiGt9FwejTKyAlmVx38s6rq_g4JMitbMCfH4eXHF2iMTLLffS43-REgp99rExHS5tBZKaB3eYg8n7kkU0wfRWp81bHjA67jy4tVMZL5pm6aeBe_GDi9sOQF868VyjgUNPFINw"

BASE_URL = "https://dev.icepeak.ai"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_single_emotion_vector():
    """Test a single emotion_vector_id generation"""
    
    # Test configuration - Excited emotion vector
    test_config = {
        "text": "We're going on the adventure of a lifetime!",
        "actor_id": "667cce64b2524e2fc47eb6e8",  # v001
        "tempo": 1,
        "pitch": 0,
        "style_label": "normal-1",  # MUST be normal-1 for emotion_vector
        "style_label_version": "v1",
        "emotion_label": "",  # MUST be empty string for emotion_vector
        "emotion_vector_id": "68a6b0ca2edfc11a25045538",  # Excited
        "emotion_scale": 1.5,
        "previous_text": None,
        "next_text": None,
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "adjust_lastword": 0
    }
    
    print("Testing emotion_vector_id generation with configuration:")
    print(f"  emotion_label: '{test_config['emotion_label']}' (empty)")
    print(f"  style_label: {test_config['style_label']}")
    print(f"  emotion_vector_id: {test_config['emotion_vector_id']}")
    print(f"  emotion_scale: {test_config['emotion_scale']}")
    
    # Step 1: Request generation
    print("\n1. Requesting TTS generation...")
    response = requests.post(
        f"{BASE_URL}/api/tts/add-queue",
        headers=HEADERS,
        json=test_config
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False
    
    result = response.json()
    request_id = result.get("id")
    print(f"Request ID: {request_id}")
    
    # Step 2: Poll for completion
    print("\n2. Polling for completion...")
    max_attempts = 30
    for attempt in range(max_attempts):
        time.sleep(2)
        
        status_response = requests.get(
            f"{BASE_URL}/api/tts/{request_id}",
            headers=HEADERS
        )
        
        if status_response.status_code != 200:
            print(f"Status check error: {status_response.status_code}")
            continue
            
        status_data = status_response.json()
        status = status_data.get("status")
        print(f"  Attempt {attempt + 1}: {status}")
        
        if status == "completed":
            audio_url = status_data.get("url")
            print(f"\n3. Audio URL received: {audio_url}")
            
            # Step 3: Download audio
            if audio_url:
                print("\n4. Downloading audio...")
                audio_response = requests.get(audio_url)
                
                if audio_response.status_code == 200:
                    # Save test file
                    output_path = Path("public/voices/test_v001_vec_excited_scale_1.5.wav")
                    output_path.write_bytes(audio_response.content)
                    print(f"✅ Audio saved to: {output_path}")
                    print(f"   File size: {len(audio_response.content)} bytes")
                    return True
                else:
                    print(f"❌ Failed to download audio: {audio_response.status_code}")
                    return False
            break
        elif status == "failed":
            print(f"❌ Generation failed: {status_data.get('error', 'Unknown error')}")
            return False
    
    print("❌ Timeout waiting for generation")
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Emotion Vector ID Generation")
    print("=" * 60)
    
    success = test_single_emotion_vector()
    
    if success:
        print("\n✅ Test PASSED - emotion_vector_id generation works!")
        print("\nYou can now proceed with full generation.")
    else:
        print("\n❌ Test FAILED - Check configuration and try again")