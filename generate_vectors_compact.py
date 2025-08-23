#!/usr/bin/env python3
"""
Compact emotion_vector generation script - Optimized version
Based on successful test configuration
"""

import time
import requests
import json
from pathlib import Path
from typing import Dict, List

# Configuration - NEED FRESH TOKEN
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1ODIxMzIzLCJleHAiOjE3NTU4MjQ5MjMsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.P751wYbfr_LPdS3nw8CHO2-o0Bs2Zds59Gtu4G4tIVU7jvPlyJgyvZJCc27hEWVm2HyTv9-Lh-niUdTnohyR0ELmoazs8VXJWkwmeRDb3R370SgA2OvNWe8XN_S7AGcRDVkOmTPY6klBfsdsX13XS49fr7MXGsAA-W-yjjxrsFHhrHTTauYzCAGumNmfoYwWq-ymzIojtkKZ5hoOEc0ADRfI4eUvUIZtQmrXviSNp_4xTMEkBMDqIw7XBA7t25gLQEnxzQE6bAnPOult5XL7mumHYwbRaC2MEewxNHorxjNrSnwmbrRSdL2PzIvegn30mryDuApjtF2BirSFolzswg"
HOST = "https://dev.icepeak.ai"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Working actor_ids for this account
ACTORS = {
    "v001": "688b02990486383d463c9d1a",  # male
    "v002": "689c69984c7990a1ddca2327"   # female
}

# Verified emotion_vector_ids from tts-test-sentences.md
EMOTION_VECTORS = {
    "excited": {
        "id": "68a7b5995b2b44d11cede93c",
        "texts": {
            "match": "We're going on the adventure of a lifetime!",
            "neutral": "The temperature today is expected to reach seventy-two degrees.",
            "opposite": "I'm too exhausted and drained to do anything at all today."
        }
    },
    "furious": {
        "id": "68a7b5a418fc7f54efec5b2f",
        "texts": {
            "match": "This is absolutely unacceptable and I demand an explanation!",
            "neutral": "The library closes at eight o'clock on weekday evenings.",
            "opposite": "I completely understand your position and I'm not upset at all."
        }
    },
    "terrified": {
        "id": "68a7b5acb4a6c41c56a161e9",
        "texts": {
            "match": "Something is moving in the shadows and I don't know what!",
            "neutral": "The coffee machine is located on the third floor break room.",
            "opposite": "I feel completely safe and protected in this wonderful place."
        }
    },
    "fear": {
        "id": "68a7b5beb4a6c41c56a161ea",
        "texts": {
            "match": "I'm really scared about what might happen if this goes wrong.",
            "neutral": "The new software update will be installed next Tuesday.",
            "opposite": "I have complete confidence that everything will work out perfectly."
        }
    },
    "surprise": {
        "id": "68a7b5c218fc7f54efec5b31",
        "texts": {
            "match": "Oh my goodness, I never expected to see you here today!",
            "neutral": "The parking lot is located behind the main building entrance.",
            "opposite": "This is exactly what I predicted would happen all along."
        }
    },
    "excitement": {
        "id": "68a7b5c5b4a6c41c56a161eb",
        "texts": {
            "match": "I can hardly wait to share this amazing news with everyone!",
            "neutral": "Please fill out the form and return it to the front desk.",
            "opposite": "This is rather boring and I'm not interested in it at all."
        }
    }
}

EMOTION_SCALES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

def generate_audio(voice_id: str, text: str, emotion_vector_id: str, 
                  emotion_scale: float, output_filename: str) -> bool:
    """Generate single audio using working configuration"""
    
    payload = [{
        "text": text,
        "actor_id": ACTORS[voice_id],
        "tempo": 1,
        "pitch": 0,
        "style_label": "normal-1",
        "style_label_version": "v1",
        "emotion_vector_id": emotion_vector_id,
        "emotion_scale": emotion_scale,
        "bp_c_l": True,  # Critical parameter
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "adjust_lastword": 0
    }]
    
    try:
        # Request generation
        response = requests.post(f"{HOST}/api/speak/batch/post", 
                                headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            print(f"  ❌ Request failed: {response.status_code}")
            return False
            
        speak_urls = response.json().get("result", {}).get("speak_urls", [])
        if not speak_urls:
            return False
        
        # Poll for completion
        for _ in range(30):
            time.sleep(2)
            poll_response = requests.post(f"{HOST}/api/speak/batch/get",
                                         headers=HEADERS, json=speak_urls)
            
            if poll_response.status_code != 200:
                continue
                
            result = poll_response.json()["result"][0]
            
            if result["status"] == "done":
                # Get audio URL
                audio_url = result["audio"]["url"]
                cf_response = requests.get(f"{audio_url}/cloudfront", headers=HEADERS)
                real_url = cf_response.json()["result"]
                
                # Download audio
                audio_data = requests.get(real_url).content
                
                # Save file
                output_path = Path(f"public/voices/{output_filename}")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(audio_data)
                
                print(f"  ✅ {output_filename} ({len(audio_data)} bytes)")
                return True
                
            elif result["status"] == "failed":
                print(f"  ❌ Generation failed")
                return False
        
        print(f"  ❌ Timeout")
        return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Generate all emotion_vector samples"""
    
    print("=" * 60)
    print("EMOTION VECTOR TTS GENERATION")
    print("=" * 60)
    print(f"\nTotal samples to generate: 216")
    print(f"(6 emotions × 3 texts × 6 scales × 2 voices)")
    
    if TOKEN == "YOUR_FRESH_TOKEN_HERE":
        print("\n❌ ERROR: Please update TOKEN with fresh token!")
        return
    
    generated = 0
    failed = 0
    
    for emotion_name, emotion_data in EMOTION_VECTORS.items():
        print(f"\n📢 Processing {emotion_name}...")
        
        for voice_name in ACTORS.keys():
            for text_type, text in emotion_data["texts"].items():
                for scale in EMOTION_SCALES:
                    # Generate filename: v001_match_vec_excited_scale_1.5.wav
                    scale_str = str(scale).replace(".", "_")
                    filename = f"{voice_name}_{text_type}_vec_{emotion_name}_scale_{scale}.wav"
                    
                    print(f"\n  Generating: {filename}")
                    
                    success = generate_audio(
                        voice_name,
                        text,
                        emotion_data["id"],
                        scale,
                        filename
                    )
                    
                    if success:
                        generated += 1
                    else:
                        failed += 1
                    
                    # Progress
                    total = generated + failed
                    print(f"  Progress: {total}/216 ({generated} success, {failed} failed)")
                    
                    # Small delay to avoid rate limiting
                    time.sleep(1)
    
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print(f"✅ Successfully generated: {generated}/216")
    if failed > 0:
        print(f"❌ Failed: {failed}/216")

if __name__ == "__main__":
    main()