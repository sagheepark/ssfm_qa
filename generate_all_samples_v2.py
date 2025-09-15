#!/usr/bin/env python3
"""
Generate ALL Sample Audio Files for TTS QA System - v2
Based on the working test script pattern
"""

import requests
import json
import time
import os
from pathlib import Path

# API Configuration - SAME FORMAT AS WORKING SCRIPT
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODc3NjM4LCJleHAiOjE3NTY4ODEyMzgsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.I05jIeTjYnhxbnHmTAacL-TrpBc_TnohmHtgIDN0tokIwxcxpKT5COvVNv3kYcfg33-Ola714ZeIjdmvYXU9sVXGlSViw36gZwWIBGUnKfKFubTau5KQdLRGNSB7qx9YGWrr4fdMSz-rCswlSSX8SEKuz7-uP37v91SHXOMR7IgGL-FjHl-FmZHeaotTu1zzJD3HwJONu2DlG8QrLPHLvIwnlYCg_plGq5vg3R0Je43P4AFbPCKe9ys0eN3dwOt85Q5Q7K3smlAvEWjQxBhppaeiYIoEOtImK20vVQg623iF2JWcF4T3YMLGHQV8nkdId5XinItfa1HCD3oY8ocrmg"

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
TEXT_TYPES = ["match", "neutral", "opposite"]
EXPRESSIVITIES = ["none", "0.6"]

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

def generate_samples_for_expressivity(expressivity_type):
    """Generate all sample files for one expressivity type"""
    print(f"\n{'='*60}")
    print(f"Generating samples for expressivity_{expressivity_type}")
    print(f"{'='*60}")
    
    all_requests = []
    all_file_mappings = []
    
    # Generate emotion_label samples
    for voice_name, voice_id in VOICES.items():
        for emotion in EMOTION_LABELS:
            for text_type in TEXT_TYPES:
                for scale in SCALES:
                    # Get text and add expressivity suffix if needed
                    text = EMOTION_TEXTS[emotion][text_type]
                    if expressivity_type == "0.6":
                        text = text + "|0.6"
                    
                    request = create_tts_request(text, voice_id, "label", emotion, scale)
                    all_requests.append(request)
                    
                    output_dir = f"public/voices_2/expressivity_{expressivity_type}/"
                    filename = f"{voice_name}_{emotion}_{text_type}_scale_{scale}.wav"
                    all_file_mappings.append({
                        "filename": filename,
                        "output_path": os.path.join(output_dir, filename)
                    })
    
    # Generate emotion_vector samples
    for voice_name, voice_id in VOICES.items():
        for emotion, vector_id in EMOTION_VECTORS.items():
            for text_type in TEXT_TYPES:
                for scale in SCALES:
                    # Get text and add expressivity suffix if needed
                    text = EMOTION_TEXTS[emotion][text_type]
                    if expressivity_type == "0.6":
                        text = text + "|0.6"
                    
                    request = create_tts_request(text, voice_id, "vector", vector_id, scale)
                    all_requests.append(request)
                    
                    output_dir = f"public/voices_2/expressivity_{expressivity_type}/"
                    filename = f"{voice_name}_{emotion}_{text_type}_scale_{scale}.wav"
                    all_file_mappings.append({
                        "filename": filename,
                        "output_path": os.path.join(output_dir, filename)
                    })
    
    total_expected = len(VOICES) * (len(EMOTION_LABELS) + len(EMOTION_VECTORS)) * len(TEXT_TYPES) * len(SCALES)
    print(f"Total requests: {len(all_requests)}")
    print(f"Expected: 2 voices × 12 emotions × 3 text_types × 6 scales = {total_expected}")
    
    # Process in batches of 4 (API limit)
    batch_size = 4
    all_results = []
    success_count = 0
    failed_count = 0
    
    for batch_idx in range(0, len(all_requests), batch_size):
        batch_requests = all_requests[batch_idx:batch_idx + batch_size]
        batch_file_mappings = all_file_mappings[batch_idx:batch_idx + batch_size]
        
        print(f"\nProcessing batch {batch_idx//batch_size + 1}/{(len(all_requests) + batch_size - 1)//batch_size}")
        
        try:
            speak_urls = batch_request_tts(batch_requests)
            results = poll_for_completion(speak_urls)
            
            # Download results for this batch
            for i, result in enumerate(results):
                if result.get("status") == "done":
                    audio_url = result.get("audio", {}).get("url")
                    if audio_url:
                        download_url = get_download_url(audio_url)
                        file_info = batch_file_mappings[i]
                        download_audio(download_url, file_info["output_path"])
                        print(f"✓ Generated: {file_info['filename']}")
                        success_count += 1
                else:
                    print(f"✗ Failed: {batch_file_mappings[i]['filename']}")
                    failed_count += 1
                    
        except Exception as e:
            print(f"Error processing batch: {e}")
            failed_count += len(batch_requests)
    
    print(f"\nCompleted expressivity_{expressivity_type}: {success_count}/{len(all_requests)} files")
    return success_count, failed_count

def main():
    """Generate all 864 sample files"""
    print("Starting FULL Sample Generation - All 864 files")
    print("="*60)
    
    total_success = 0
    total_failed = 0
    
    for expressivity in EXPRESSIVITIES:
        success, failed = generate_samples_for_expressivity(expressivity)
        total_success += success
        total_failed += failed
    
    print(f"\n{'='*60}")
    print("FULL SAMPLE GENERATION COMPLETE!")
    print(f"Total samples generated: {total_success}")
    print(f"Total failed: {total_failed}")
    print(f"Expected total: 864 sample files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()