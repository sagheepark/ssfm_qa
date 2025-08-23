#!/usr/bin/env python3
"""
Generate emotion_vector_id TTS samples based on plan.md requirements
Using dev_ssfm30.ipynb as blueprint for API calls
"""

import time
import requests
import json
from pathlib import Path
from typing import Dict, List, Optional

# Configuration from plan.md
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1NzkwNTI3LCJleHAiOjE3NTU3OTQxMjcsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.fFBDZnhMgpnMXwy0kDyCLasjY95I1b_PCHVptjznUI4fPI1eUBrR7caHQ3o_Uj6YQIE_5Uji6O-KsEwXZuJmtrfuQH1XeJjOcQdpNpjkyZfUY1_Y687SlDO9Sk0BqSMAAsEg8B5keCQg8F7nO4btk-XYKm_UGn1ANtbKMMMMd6aToJPMkEdJsmMUwW8UxNfMhL16JUZzWS6TvBCTSeiGt9FwejTKyAlmVx38s6rq_g4JMitbMCfH4eXHF2iMTLLffS43-REgp99rExHS5tBZKaB3eYg8n7kkU0wfRWp81bHjA67jy4tVMZL5pm6aeBe_GDi9sOQF868VyjgUNPFINw"

HOST = "https://dev.icepeak.ai"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Voice IDs - using working actor_ids for this token
VOICE_IDS = {
    "v001": "688b02990486383d463c9d1a",  # ssfm_v30_emotion_test (male)
    "v002": "689c69984c7990a1ddca2327"   # ssfm_v30_emotion_test_female (female)
}

# Emotion vectors from updated tts-test-sentences.md
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
            "match": "Something is moving in the shadows and I don't know what it is!",
            "neutral": "The coffee machine is located on the third floor break room.",
            "opposite": "I feel completely safe and protected in this wonderful place."
        }
    },
    "fear": {
        "id": "68a7b5beb4a6c41c56a161ea",
        "texts": {
            "match": "I'm really scared about what might happen if this goes wrong.",
            "neutral": "The new software update will be installed next Tuesday morning.",
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
            "neutral": "Please submit your report by the end of business today.",
            "opposite": "Nothing particularly interesting happened during the entire meeting."
        }
    }
}

# Emotion scales from plan.md
EMOTION_SCALES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

def generate_single_audio(voice_id: str, text: str, emotion_vector_id: str, 
                         emotion_scale: float, output_filename: str) -> bool:
    """Generate a single audio file using the speak API (following notebook blueprint)"""
    
    speak_data = [
        {
            "text": text,
            "actor_id": VOICE_IDS[voice_id],
            "tempo": 1,
            "pitch": 0,
            "style_label": "normal-1",  # MUST be normal-1 for emotion_vector
            "style_label_version": "v1",
            "emotion_vector_id": emotion_vector_id,  # The emotion vector ID
            "emotion_scale": emotion_scale,
            "bp_c_l": True,  # Important parameter
            "lang": "auto",
            "mode": "one-vocoder",
            "retake": True,
            "adjust_lastword": 0,
        }
    ]
    
    try:
        # Step 1: Request generation (using speak/batch/post like notebook)
        speak_response = requests.post(
            f"{HOST}/api/speak/batch/post", 
            headers=HEADERS, 
            json=speak_data
        )
        
        if speak_response.status_code != 200:
            print(f"  ❌ Request failed: {speak_response.status_code}")
            return False
            
        r = speak_response.json()
        speak_urls = r.get("result", {}).get("speak_urls", [])
        
        if not speak_urls:
            print(f"  ❌ No speak URLs returned")
            return False
        
        # Step 2: Poll for completion (using speak/batch/get)
        for attempt in range(30):
            time.sleep(2)
            
            poll_response = requests.post(
                f"{HOST}/api/speak/batch/get", 
                headers=HEADERS, 
                json=speak_urls
            )
            
            if poll_response.status_code != 200:
                continue
                
            poll_result = poll_response.json()["result"][0]
            
            if poll_result["status"] == "done":
                # Step 3: Get cloudfront URL
                audio_url = poll_result["audio"]["url"]
                audio_response = requests.get(
                    f"{audio_url}/cloudfront", 
                    headers=HEADERS
                )
                
                if audio_response.status_code != 200:
                    print(f"  ❌ Failed to get cloudfront URL")
                    return False
                    
                audio_response_json = audio_response.json()
                real_audio_url = audio_response_json["result"]
                
                # Step 4: Download actual audio
                real_audio_response = requests.get(real_audio_url)
                
                if real_audio_response.status_code != 200:
                    print(f"  ❌ Failed to download audio")
                    return False
                
                # Save audio file
                output_path = Path(f"public/voices/{output_filename}")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, "wb") as audio_file:
                    audio_file.write(real_audio_response.content)
                
                print(f"  ✅ Saved: {output_filename} ({len(real_audio_response.content)} bytes)")
                return True
                
            elif poll_result["status"] == "failed":
                print(f"  ❌ Generation failed")
                return False
        
        print(f"  ❌ Timeout waiting for generation")
        return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def generate_all_emotion_vectors():
    """Generate all emotion_vector samples according to plan.md"""
    
    total_samples = len(EMOTION_VECTORS) * len(VOICE_IDS) * 3 * len(EMOTION_SCALES)  # 6*2*3*6 = 216
    generated = 0
    failed = 0
    
    print(f"Starting generation of {total_samples} emotion_vector samples")
    print("=" * 60)
    
    for emotion_name, emotion_data in EMOTION_VECTORS.items():
        emotion_id = emotion_data["id"]
        
        for voice_name, voice_id in VOICE_IDS.items():
            for text_type, text in emotion_data["texts"].items():
                for scale in EMOTION_SCALES:
                    # Generate filename according to plan.md format
                    # Format: {voice_id}_{text_type}_vec_{emotion}_{scale}.wav
                    scale_str = str(scale).replace(".", "_")
                    filename = f"{voice_name}_{text_type}_vec_{emotion_name}_scale_{scale}.wav"
                    
                    print(f"\nGenerating: {filename}")
                    print(f"  Voice: {voice_name}, Emotion: {emotion_name}, Text: {text_type}, Scale: {scale}")
                    
                    success = generate_single_audio(
                        voice_name, 
                        text, 
                        emotion_id, 
                        scale, 
                        filename
                    )
                    
                    if success:
                        generated += 1
                    else:
                        failed += 1
                    
                    # Progress update
                    total_processed = generated + failed
                    print(f"  Progress: {total_processed}/{total_samples} ({generated} success, {failed} failed)")
                    
                    # Small delay to avoid rate limiting
                    time.sleep(1)
    
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print(f"✅ Successfully generated: {generated}/{total_samples}")
    print(f"❌ Failed: {failed}/{total_samples}")
    
    return generated, failed

if __name__ == "__main__":
    print("=" * 60)
    print("EMOTION VECTOR TTS GENERATION")
    print("Based on plan.md requirements")
    print("=" * 60)
    
    generated, failed = generate_all_emotion_vectors()
    
    if failed == 0:
        print("\n🎉 All emotion_vector samples generated successfully!")
    else:
        print(f"\n⚠️  Some samples failed. Please check and retry.")