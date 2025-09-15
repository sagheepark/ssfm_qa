#!/usr/bin/env python3
"""
Generate Sample Audio Files for TTS QA System - v2
Based on the working reference generation script pattern
"""

import requests
import json
import time
import os
from pathlib import Path

# API Configuration - SAME FORMAT AS WORKING REFERENCE SCRIPT
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODczMjkzLCJleHAiOjE3NTY4NzY4OTMsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.bcBxWngqX2Lx0Q01emmpGEaHa01pkUbidiruO7al8vLE9qj6N8aQWGC8La1sECUGDgCvEQG7--2Y0_mT7yATXxt1NoixkY0x4Yb28fsCG_AkfxOKw-gQhjtVPKLjY1W_qNy4EpIbB7c0cT-4hVhccrgFjONPhenqHeMh4aOFJ7f2A-wApwk8u7O5_ByAa2s1zU0Sf201gbYUQNbipnBvblig5_whUHbkEk7-rXz8wDBHT9EnkblI-Rpoc31HGelhO1ahHEMKsnfnHt7P7Th047FKulwefDDYmehpaiE9wNgKzSgs9_Xbc05rIM2qIA7wUSondO6A0Cm_17xiwUt9fQ"

BASE_URL = "https://dev.icepeak.ai/api"

# Voice configurations - NEW VOICE IDs
VOICES = {
    "v001": "68ad0ca7e68cb082a1c46fd6",  # male - NEW
    "v002": "68ad0cb625c2800730ac5b48"   # female - NEW
}

# Emotion configurations
EMOTION_LABELS = ["angry", "sad", "happy", "whisper", "toneup", "tonedown"]
EMOTION_VECTORS = {
    "excited": "68a6b0ca2edfc11a25045538",
    "furious": "68a6b0d9b436060efdc6bc82", 
    "terrified": "68a6b0d2b436060efdc6bc80",
    "fear": "68a6b0f7b436060efdc6bc83",
    "surprise": "68a6b10255e3b2836e609969",
    "excitement": "68a6b1062edfc11a2504553b"
}

# ALL emotion texts
EMOTION_TEXTS = {
    "angry": {
        "match": "I can't believe you broke your promise again after everything we discussed!",
        "neutral": "The meeting is scheduled for three o'clock in the conference room.",
        "opposite": "Your thoughtfulness and kindness truly made my day so much better."
    },
    "sad": {
        "match": "I really miss the old days when everyone was still here together.",
        "neutral": "The report needs to be submitted by Friday afternoon without fail.",
        "opposite": "This is absolutely the best news I've heard all year long!"
    },
    "happy": {
        "match": "I'm so thrilled about the wonderful surprise party you organized for me!",
        "neutral": "Please remember to turn off the lights when you leave the office.",
        "opposite": "Everything seems to be going wrong and nothing works out anymore."
    },
    "whisper": {
        "match": "Don't make any noise, everyone is sleeping in the next room.",
        "neutral": "The quarterly financial report shows steady growth in all departments.",
        "opposite": "Everyone needs to hear this important announcement right now!"
    },
    "toneup": {
        "match": "Did you really win the grand prize in the competition?",
        "neutral": "The train arrives at platform seven every hour on weekdays.",
        "opposite": "Everything is perfectly calm and there's nothing to worry about here."
    },
    "tonedown": {
        "match": "Let me explain this matter in a very serious and professional manner.",
        "neutral": "The document contains information about the new policy changes.",
        "opposite": "This is so incredibly exciting and I can barely contain myself!"
    },
    "excited": {
        "match": "We're going on the adventure of a lifetime starting tomorrow morning!",
        "neutral": "The temperature today is expected to reach seventy-two degrees.",
        "opposite": "I'm too exhausted and drained to do anything at all today."
    },
    "furious": {
        "match": "This is absolutely unacceptable and I demand an explanation immediately!",
        "neutral": "The library closes at eight o'clock on weekday evenings.",
        "opposite": "I completely understand your position and I'm not upset at all."
    },
    "terrified": {
        "match": "Something is moving in the shadows and I don't know what it is!",
        "neutral": "The coffee machine is located on the third floor break room.",
        "opposite": "I feel completely safe and protected in this wonderful place."
    },
    "fear": {
        "match": "I'm really scared about what might happen if this goes wrong.",
        "neutral": "The new software update will be installed next Tuesday morning.",
        "opposite": "I have complete confidence that everything will work out perfectly."
    },
    "surprise": {
        "match": "Oh my goodness, I never expected to see you here today!",
        "neutral": "The parking lot is located behind the main building entrance.",
        "opposite": "This is exactly what I predicted would happen all along."
    },
    "excitement": {
        "match": "I can hardly wait to share this amazing news with everyone!",
        "neutral": "Please fill out the form and return it to the front desk.",
        "opposite": "This is rather boring and I'm not interested in it at all."
    }
}

SCALES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

def create_tts_request(text, voice_id, emotion_type, emotion_value, scale):
    """Create a TTS request for sample audio with emotion"""
    request = {
        "text": text,
        "actor_id": voice_id,
        "style_label": "normal-1",
        "emotion_scale": scale,
        "tempo": 1,
        "pitch": 0,
        "lang": "auto",
        "mode": "one-vocoder",  # CRITICAL
        "retake": True,
        "bp_c_l": True,
        "adjust_lastword": 0,
        "style_label_version": "v1"
    }
    
    # Add emotion parameter based on type
    if emotion_type == "label":
        request["emotion_label"] = emotion_value
    else:  # emotion_type == "vector"
        request["emotion_vector_id"] = emotion_value
    
    return request

# Copy the exact working functions from reference script
def batch_request_tts(requests_data):
    """Send batch TTS request"""
    url = f"{BASE_URL}/speak/batch/post"
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }
    
    print(f"Sending batch request with {len(requests_data)} items...")
    response = requests.post(url, json=requests_data, headers=headers)
    
    if response.status_code != 200:
        print(f"Error response: {response.text}")
    
    response.raise_for_status()
    
    result = response.json()
    speak_urls = result.get("result", {}).get("speak_urls", [])
    print(f"Received {len(speak_urls)} speak URLs")
    return speak_urls

def poll_for_completion(speak_urls, max_attempts=40):
    """Poll for TTS completion"""
    url = f"{BASE_URL}/speak/batch/get"
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }
    
    for attempt in range(max_attempts):
        print(f"Polling attempt {attempt + 1}/{max_attempts}...")
        response = requests.post(url, json=speak_urls, headers=headers)
        response.raise_for_status()
        
        results = response.json().get("result", [])
        all_done = all(r.get("status") == "done" for r in results)
        
        if all_done:
            print("All audio generation completed!")
            return results
        
        time.sleep(5)
    
    raise TimeoutError("TTS generation timed out")

def get_download_url(audio_url):
    """Get CloudFront download URL"""
    url = f"{audio_url}/cloudfront"
    headers = {"Authorization": API_TOKEN}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json().get("result")

def download_audio(download_url, output_path):
    """Download audio file"""
    response = requests.get(download_url)
    response.raise_for_status()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded: {output_path}")

def main():
    """Generate first 10 samples as a test"""
    print("Testing Sample Generation - First 10 files")
    print("=" * 60)
    
    # Test with just 10 samples first
    all_requests = []
    all_file_mappings = []
    
    count = 0
    max_test = 10
    
    # Generate for expressivity_none first
    for voice_name, voice_id in VOICES.items():
        for emotion in EMOTION_LABELS[:2]:  # Just angry and sad for test
            for text_type in ["match"]:  # Just match for test 
                for scale in [1.0, 2.0]:  # Just 2 scales for test
                    if count >= max_test:
                        break
                        
                    text = EMOTION_TEXTS[emotion][text_type]
                    request = create_tts_request(text, voice_id, "label", emotion, scale)
                    all_requests.append(request)
                    
                    output_dir = f"public/voices_2/expressivity_none/"
                    filename = f"{voice_name}_{emotion}_{text_type}_scale_{scale}.wav"
                    all_file_mappings.append({
                        "filename": filename,
                        "output_path": os.path.join(output_dir, filename)
                    })
                    count += 1
                    
                if count >= max_test:
                    break
            if count >= max_test:
                break
        if count >= max_test:
            break
    
    print(f"Testing with {len(all_requests)} sample requests...")
    
    # Process in batches of 4 (API limit)
    batch_size = 4
    all_results = []
    
    for batch_idx in range(0, len(all_requests), batch_size):
        batch_requests = all_requests[batch_idx:batch_idx + batch_size]
        print(f"\nProcessing batch {batch_idx//batch_size + 1}/{(len(all_requests) + batch_size - 1)//batch_size}")
        
        speak_urls = batch_request_tts(batch_requests)
        results = poll_for_completion(speak_urls)
        all_results.extend(results)
    
    # Download all generated audios
    success_count = 0
    for i, result in enumerate(all_results):
        if result.get("status") == "done":
            audio_url = result.get("audio", {}).get("url")
            if audio_url:
                download_url = get_download_url(audio_url)
                file_info = all_file_mappings[i]
                download_audio(download_url, file_info["output_path"])
                success_count += 1
                print(f"✓ Generated: {file_info['filename']}")
        else:
            print(f"✗ Failed: {all_file_mappings[i]['filename']}")
    
    print(f"\nTest completed: {success_count}/{len(all_requests)} files generated")
    
    if success_count > 0:
        print("🎉 Sample generation is working! Ready for full generation.")
        return True
    else:
        print("❌ Sample generation failed.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)