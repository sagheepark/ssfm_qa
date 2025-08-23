#!/usr/bin/env python3
"""
Comprehensive Expressivity Comparison Script
Generates complete datasets for both expressivity_none and expressivity_0.6
"""

import time
import requests
import json
from pathlib import Path
from typing import Dict, List

# Configuration - Fresh token provided
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1ODM4OTI3LCJleHAiOjE3NTU4NDI1MjcsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.rKoWTYnVq-5xg0T4feUvkjamKpxu3DuWWAxDW4fWOMUCRauYPPLt0i9lT7lBL4KtGHnRwNoHNyKShBRrS7_V3UiZEb85b06-uqsO_AjC2ZBvHAo1Pgf7kYaMS1Bdem4R9GYZWCwgGLYm1hNqLcL5nLacmxS7CUJrOkUKABYIS6i-s_R4Rhk0QlS1dyc7I4iqq2iiRQvRSUjHDuXcOoQwg7eqk_0ScBp--EsQjhHC7xmSlFIagNWuIhyiCQz0ao-YzA_ea9JHiaFEK43bu_gK9IumsFckDAKFiivHJIuCx6MxdcgSHMWNngoTWy_XTC3zXW4q2RAHzhZpqL-VPYBHXQ"

HOST = "https://dev.icepeak.ai"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Voice actors
ACTORS = {
    "v001": "688b02990486383d463c9d1a",  # male
    "v002": "689c69984c7990a1ddca2327"   # female
}

# Emotion Labels (use emotion_label field)
EMOTION_LABELS = {
    "angry": {
        "texts": {
            "match": "I can't believe you broke your promise again after everything we discussed!",
            "neutral": "The meeting is scheduled for three o'clock in the conference room.",
            "opposite": "Your thoughtfulness and kindness truly made my day so much better."
        }
    },
    "sad": {
        "texts": {
            "match": "I really miss the old days when everyone was still here together.",
            "neutral": "The report needs to be submitted by Friday afternoon without fail.",
            "opposite": "This is absolutely the best news I've heard all year long!"
        }
    },
    "happy": {
        "texts": {
            "match": "I'm so thrilled about the wonderful surprise party you organized for me!",
            "neutral": "Please remember to turn off the lights when you leave the office.",
            "opposite": "Everything seems to be going wrong and nothing works out anymore."
        }
    },
    "whisper": {
        "texts": {
            "match": "Don't make any noise, everyone is sleeping in the next room.",
            "neutral": "The quarterly financial report shows steady growth in all departments.",
            "opposite": "Everyone needs to hear this important announcement right now!"
        }
    },
    "toneup": {
        "texts": {
            "match": "Did you really win the grand prize in the competition?",
            "neutral": "The train arrives at platform seven every hour on weekdays.",
            "opposite": "Everything is perfectly calm and there's nothing to worry about here."
        }
    },
    "tonedown": {
        "texts": {
            "match": "Let me explain this matter in a very serious and professional manner.",
            "neutral": "The document contains information about the new policy changes.",
            "opposite": "This is so incredibly exciting and I can barely contain myself!"
        }
    }
}

# Emotion Vectors (use emotion_vector_id field)
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

def generate_audio(voice_id: str, text: str, emotion_type: str, emotion_value: str,
                  emotion_scale: float, output_filename: str, expressivity: str) -> bool:
    """Generate single audio using emotion_label or emotion_vector_id"""
    
    # Add expressivity suffix if needed
    if expressivity == "0.6":
        text = f"{text} |0.6"
    
    # Build payload based on emotion type
    if emotion_type == "label":
        payload = [{
            "text": text,
            "actor_id": ACTORS[voice_id],
            "tempo": 1,
            "pitch": 0,
            "style_label": "normal-1",
            "style_label_version": "v1",
            "emotion_label": emotion_value,
            "emotion_scale": emotion_scale,
            "lang": "auto",
            "mode": "one-vocoder",
            "retake": True,
            "adjust_lastword": 0
        }]
    else:  # emotion_vector
        payload = [{
            "text": text,
            "actor_id": ACTORS[voice_id],
            "tempo": 1,
            "pitch": 0,
            "style_label": "normal-1",
            "style_label_version": "v1",
            "emotion_vector_id": emotion_value,
            "emotion_scale": emotion_scale,
            "bp_c_l": True,  # Critical for emotion_vector
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
                folder = f"expressivity_{expressivity}" if expressivity != "none" else "expressivity_none"
                output_path = Path(f"public/voices/{folder}/{output_filename}")
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

def generate_complete_dataset(expressivity: str, skip_existing: bool = True):
    """Generate complete dataset for given expressivity version"""
    
    print(f"\n{'='*60}")
    print(f"GENERATING EXPRESSIVITY_{expressivity.upper()} DATASET")
    print(f"{'='*60}")
    
    # Calculate totals
    total_emotion_labels = len(EMOTION_LABELS) * len(ACTORS) * 3 * len(EMOTION_SCALES)  # 6*2*3*6 = 216
    total_emotion_vectors = len(EMOTION_VECTORS) * len(ACTORS) * 3 * len(EMOTION_SCALES)  # 6*2*3*6 = 216
    total_samples = total_emotion_labels + total_emotion_vectors  # 432
    
    print(f"Total samples to generate: {total_samples}")
    print(f"- Emotion Labels: {total_emotion_labels}")
    print(f"- Emotion Vectors: {total_emotion_vectors}")
    
    generated = 0
    failed = 0
    skipped = 0
    
    # Generate Emotion Label samples
    print(f"\n📢 Processing EMOTION LABELS...")
    for emotion_name, emotion_data in EMOTION_LABELS.items():
        print(f"\n  Processing emotion_label: {emotion_name}")
        
        for voice_name in ACTORS.keys():
            for text_type, text in emotion_data["texts"].items():
                for scale in EMOTION_SCALES:
                    scale_str = str(scale).replace(".", "_")
                    filename = f"{voice_name}_{text_type}_emo_{emotion_name}_scale_{scale}.wav"
                    
                    # Check if file exists
                    folder = f"expressivity_{expressivity}" if expressivity != "none" else "expressivity_none"
                    output_path = Path(f"public/voices/{folder}/{filename}")
                    
                    if skip_existing and output_path.exists():
                        skipped += 1
                        print(f"    ⏭️  Skipping existing: {filename}")
                        continue
                    
                    print(f"\n    Generating: {filename}")
                    
                    success = generate_audio(
                        voice_name, text, "label", emotion_name,
                        scale, filename, expressivity
                    )
                    
                    if success:
                        generated += 1
                    else:
                        failed += 1
                    
                    total_processed = generated + failed + skipped
                    print(f"    Progress: {total_processed}/{total_samples} ({generated} success, {failed} failed, {skipped} skipped)")
                    
                    time.sleep(1)  # Rate limiting
    
    # Generate Emotion Vector samples
    print(f"\n📢 Processing EMOTION VECTORS...")
    for emotion_name, emotion_data in EMOTION_VECTORS.items():
        print(f"\n  Processing emotion_vector: {emotion_name}")
        
        for voice_name in ACTORS.keys():
            for text_type, text in emotion_data["texts"].items():
                for scale in EMOTION_SCALES:
                    scale_str = str(scale).replace(".", "_")
                    filename = f"{voice_name}_{text_type}_vec_{emotion_name}_scale_{scale}.wav"
                    
                    # Check if file exists
                    folder = f"expressivity_{expressivity}" if expressivity != "none" else "expressivity_none"
                    output_path = Path(f"public/voices/{folder}/{filename}")
                    
                    if skip_existing and output_path.exists():
                        skipped += 1
                        print(f"    ⏭️  Skipping existing: {filename}")
                        continue
                    
                    print(f"\n    Generating: {filename}")
                    
                    success = generate_audio(
                        voice_name, text, "vector", emotion_data["id"],
                        scale, filename, expressivity
                    )
                    
                    if success:
                        generated += 1
                    else:
                        failed += 1
                    
                    total_processed = generated + failed + skipped
                    print(f"    Progress: {total_processed}/{total_samples} ({generated} success, {failed} failed, {skipped} skipped)")
                    
                    time.sleep(1)  # Rate limiting
    
    print(f"\n{'='*60}")
    print(f"EXPRESSIVITY_{expressivity.upper()} GENERATION COMPLETE")
    print(f"✅ Successfully generated: {generated}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️  Skipped existing: {skipped}")
    print(f"📊 Total processed: {generated + failed + skipped}/{total_samples}")
    
    return generated, failed, skipped

def main():
    """Main execution function"""
    
    print("="*60)
    print("EXPRESSIVITY COMPARISON DATASET GENERATION")
    print("="*60)
    
    # First, complete expressivity_none dataset
    print("\n🎯 PHASE 1: Complete expressivity_none dataset")
    generated_none, failed_none, skipped_none = generate_complete_dataset("none", skip_existing=True)
    
    if failed_none > 0:
        print(f"\n⚠️  Warning: {failed_none} files failed in expressivity_none")
        print("Consider getting fresh token before proceeding to expressivity_0.6")
        return
    
    # Then generate expressivity_0.6 dataset
    print("\n🎯 PHASE 2: Generate expressivity_0.6 dataset")
    generated_06, failed_06, skipped_06 = generate_complete_dataset("0.6", skip_existing=True)
    
    # Final summary
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    print(f"expressivity_none: {generated_none + skipped_none} files ({generated_none} new, {skipped_none} existing)")
    print(f"expressivity_0.6:  {generated_06} files ({failed_06} failed)")
    print(f"Total dataset size: {generated_none + skipped_none + generated_06} files")
    
    if failed_none == 0 and failed_06 == 0:
        print("\n🎉 COMPLETE SUCCESS: Both expressivity datasets generated!")
    else:
        print(f"\n⚠️  Some files failed. Check token expiration and retry.")

if __name__ == "__main__":
    main()