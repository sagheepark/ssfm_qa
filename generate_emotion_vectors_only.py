#!/usr/bin/env python3
"""
Generate Missing Emotion Vector Sample Files for expressivity_0.6
"""

import requests
import json
import time
import os
from pathlib import Path

# API Configuration with fresh token
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODgxNjQwLCJleHAiOjE3NTY4ODUyNDAsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.SsivGl7-2rHtcHKKxMKW3d-EsstGmO_H5IAgkGQH4GGrXaU6tGdcXMYN5NEJQdwP7dl_EHbcslIMnY_XYMXN74muHzNq2Rynze9Lfg9fl0gzGMpgZIHJAfCWFie9lwOYDPnMP7MNQi1CVOoDYsdstkOQmRpTHOLlClxJCctP2GDEFxMvpFr2Aqdv0OeTtfCHoQCYfJzjn1FDN23AL86NhSDI-GrjwdzyEFEHWUFxdgbvzx-_azJTfj8tb4qhnQJ8ZYBEOlgLV1tt14v2jZa6TaULoomSHvATotz5d87R5es_dVAhs-fWvO9ahDWX8CYZNUD56HmZQZdfyPsVKHWmxg"

BASE_URL = "https://dev.icepeak.ai/api"

# Voice configurations
VOICES = {
    "v001": "68ad0ca7e68cb082a1c46fd6",  # male
    "v002": "68ad0cb625c2800730ac5b48"   # female
}

# Emotion vectors
EMOTION_VECTORS = {
    "excited": "68a6b0ca2edfc11a25045538",
    "furious": "68a6b0d9b436060efdc6bc82", 
    "terrified": "68a6b0d2b436060efdc6bc80",
    "fear": "68a6b0f7b436060efdc6bc83",
    "surprise": "68a6b10255e3b2836e609969",
    "excitement": "68a6b1062edfc11a2504553b"
}

# Emotion texts
EMOTION_TEXTS = {
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
TEXT_TYPES = ["match", "neutral", "opposite"]

def create_tts_request(text, voice_id, vector_id, scale):
    """Create TTS request for emotion vector sample"""
    return {
        "text": text + "|0.6",  # Add expressivity suffix
        "actor_id": voice_id,
        "style_label": "normal-1",
        "emotion_vector_id": vector_id,
        "emotion_scale": scale,
        "tempo": 1,
        "pitch": 0,
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "bp_c_l": True,
        "adjust_lastword": 0,
        "style_label_version": "v1"
    }

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

def poll_for_completion(speak_urls, max_attempts=30):
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
        
        time.sleep(3)
    
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

def main():
    """Generate all emotion vector samples for expressivity_0.6"""
    print("Generating EMOTION VECTOR samples for expressivity_0.6")
    print("=" * 60)
    
    output_dir = "public/voices_2/expressivity_0.6/"
    all_requests = []
    all_file_mappings = []
    
    # Generate emotion_vector samples
    for voice_name, voice_id in VOICES.items():
        for emotion, vector_id in EMOTION_VECTORS.items():
            for text_type in TEXT_TYPES:
                for scale in SCALES:
                    text = EMOTION_TEXTS[emotion][text_type]
                    request = create_tts_request(text, voice_id, vector_id, scale)
                    all_requests.append(request)
                    
                    filename = f"{voice_name}_{emotion}_{text_type}_scale_{scale}.wav"
                    all_file_mappings.append({
                        "filename": filename,
                        "output_path": os.path.join(output_dir, filename)
                    })
    
    print(f"Total emotion vector samples to generate: {len(all_requests)}")
    print(f"Expected: 2 voices × 6 emotions × 3 text_types × 6 scales = 216")
    
    # Process in batches of 4
    batch_size = 4
    success_count = 0
    failed_count = 0
    
    for batch_idx in range(0, len(all_requests), batch_size):
        batch_requests = all_requests[batch_idx:batch_idx + batch_size]
        batch_file_mappings = all_file_mappings[batch_idx:batch_idx + batch_size]
        
        print(f"\nProcessing batch {batch_idx//batch_size + 1}/{(len(all_requests) + batch_size - 1)//batch_size}")
        
        try:
            speak_urls = batch_request_tts(batch_requests)
            results = poll_for_completion(speak_urls)
            
            # Download results
            for i, result in enumerate(results):
                file_info = batch_file_mappings[i]
                if result.get("status") == "done":
                    audio_url = result.get("audio", {}).get("url")
                    if audio_url:
                        download_url = get_download_url(audio_url)
                        download_audio(download_url, file_info["output_path"])
                        print(f"✓ Generated: {file_info['filename']}")
                        success_count += 1
                    else:
                        print(f"✗ No audio URL: {file_info['filename']}")
                        failed_count += 1
                else:
                    print(f"✗ Failed: {file_info['filename']}")
                    failed_count += 1
                    
        except Exception as e:
            print(f"Error processing batch: {e}")
            failed_count += len(batch_requests)
    
    print(f"\n{'='*60}")
    print("EMOTION VECTOR GENERATION COMPLETE!")
    print(f"✓ Successfully generated: {success_count}/216")
    print(f"✗ Failed: {failed_count}")
    
    # Final status
    total_files_now = len(os.listdir("public/voices_2/expressivity_0.6/"))
    print(f"📊 Total files in expressivity_0.6: {total_files_now}")
    print(f"🎯 Target: 504 files (72 references + 216 emotion_label + 216 emotion_vector)")

if __name__ == "__main__":
    main()