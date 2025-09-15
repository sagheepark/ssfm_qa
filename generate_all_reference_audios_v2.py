#!/usr/bin/env python3
"""
Generate ALL Reference Audio Files for TTS QA System
These are neutral baseline audios with style_label="normal-1" only (no emotion)
One reference for each unique voice × text combination
"""

import requests
import json
import time
import os
from pathlib import Path

# API Configuration
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg2NTg3NCwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODY1ODg3LCJleHAiOjE3NTY4Njk0ODcsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.IKhDwBmzcwUPsXrJgIgPiz6mQTo2Ineq6u1kA4_jZpc41pJTDkfJF6mHyA6Ldkcj6y2vBkWIAO_ml_NzEidRetmx6SEnOWHDt9xMRAerTWSQ2bD24RS1y5W4l_SsEg5IeYuROzcfwmaWWqdGyHvCbBDoxPIEPqqwlzTJooMDDRhcd0i4MdISFH68gw4ZMMBLSsrj-NFJ4BeDvjWXyqZctEREN-_l6PxQs7fBpmqI7esjL634cFt7cK_5IMRoWVm0LMj7TJD4zuBMHkk3CzwSw0bKybygZWeJ8kxPKwlSiL7pANjeP5cw4T5uun2EPeIObFQ1E7h3Xoy-H4i4A9hvMA"

BASE_URL = "https://dev.icepeak.ai/api"

# Voice configurations
VOICES = {
    "v001": "68ad0ca7e68cb082a1c46fd6",  # male - NEW
    "v002": "68ad0cb625c2800730ac5b48"   # female - NEW
}

# ALL emotion texts - each emotion has unique texts for match/neutral/opposite
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

# Emotion lists for file naming
EMOTION_LABELS = ["angry", "sad", "happy", "whisper", "toneup", "tonedown"]
EMOTION_VECTORS = ["excited", "furious", "terrified", "fear", "surprise", "excitement"]

def create_tts_request(text, voice_id):
    """Create a TTS request for reference audio (neutral baseline)"""
    return {
        "text": text,
        "actor_id": voice_id,
        "style_label": "normal-1",  # Neutral baseline - no emotion
        # Don't include emotion_label or emotion_vector_id for neutral reference
        "emotion_scale": 1.0,        # Default scale
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

def generate_references_for_expressivity(expressivity_type):
    """Generate reference audios for a specific expressivity type"""
    
    # Prepare ALL requests - one for each unique text
    all_requests = []
    all_file_mappings = []
    
    for voice_name, voice_id in VOICES.items():
        # Process emotion_label texts
        for emotion in EMOTION_LABELS:
            for text_type in ["match", "neutral", "opposite"]:
                # Get the specific text for this emotion and text_type
                text = EMOTION_TEXTS[emotion][text_type]
                
                # Add expressivity suffix if needed
                if expressivity_type == "0.6":
                    text = text + "|0.6"
                
                request = create_tts_request(text, voice_id)
                all_requests.append(request)
                
                # Store mapping for filename
                # Reference filename format: {voice_id}_{text_type}_reference_{emotion}.wav
                output_dir = f"public/voices_2/expressivity_{expressivity_type}/"
                filename = f"{voice_name}_{emotion}_{text_type}_reference.wav"
                all_file_mappings.append({
                    "voice": voice_name,
                    "emotion": emotion,
                    "text_type": text_type,
                    "filename": filename,
                    "output_path": os.path.join(output_dir, filename)
                })
        
        # Process emotion_vector texts
        for emotion in EMOTION_VECTORS:
            for text_type in ["match", "neutral", "opposite"]:
                # Get the specific text for this emotion and text_type
                text = EMOTION_TEXTS[emotion][text_type]
                
                # Add expressivity suffix if needed
                if expressivity_type == "0.6":
                    text = text + "|0.6"
                
                request = create_tts_request(text, voice_id)
                all_requests.append(request)
                
                # Store mapping for filename
                output_dir = f"public/voices_2/expressivity_{expressivity_type}/"
                filename = f"{voice_name}_{emotion}_{text_type}_reference.wav"
                all_file_mappings.append({
                    "voice": voice_name,
                    "emotion": emotion,
                    "text_type": text_type,
                    "filename": filename,
                    "output_path": os.path.join(output_dir, filename)
                })
    
    print(f"\n{'='*60}")
    print(f"Generating references for expressivity_{expressivity_type}")
    print(f"Total requests: {len(all_requests)}")
    print(f"2 voices × 12 emotions × 3 text_types = 72 files")
    print(f"{'='*60}")
    
    # Process in batches of 4 (API limit)
    batch_size = 4
    successful_count = 0
    failed_files = []
    
    for batch_idx in range(0, len(all_requests), batch_size):
        batch_requests = all_requests[batch_idx:batch_idx + batch_size]
        batch_file_mappings = all_file_mappings[batch_idx:batch_idx + batch_size]
        
        print(f"\nProcessing batch {batch_idx//batch_size + 1}/{(len(all_requests) + batch_size - 1)//batch_size}")
        
        try:
            # Send batch request
            speak_urls = batch_request_tts(batch_requests)
            
            # Poll for completion
            results = poll_for_completion(speak_urls)
            
            # Download all generated audios
            for i, result in enumerate(results):
                if result.get("status") == "done":
                    audio_url = result.get("audio", {}).get("url")
                    if audio_url:
                        # Get download URL
                        download_url = get_download_url(audio_url)
                        
                        # Download file
                        file_info = batch_file_mappings[i]
                        download_audio(download_url, file_info["output_path"])
                        print(f"✓ Generated: {file_info['filename']}")
                        successful_count += 1
                else:
                    failed_files.append(batch_file_mappings[i]['filename'])
                    print(f"✗ Failed: {batch_file_mappings[i]['filename']}")
        except Exception as e:
            print(f"Error processing batch: {e}")
            for file_info in batch_file_mappings:
                failed_files.append(file_info['filename'])
    
    print(f"\nCompleted: {successful_count}/{len(all_requests)} files generated successfully")
    if failed_files:
        print(f"Failed files: {', '.join(failed_files)}")
    
    return successful_count, failed_files

def main():
    """Main function to generate all reference audios"""
    print("Starting Complete Reference Audio Generation")
    print("="*60)
    print("Reference audios are neutral baselines:")
    print("- style_label: 'normal-1'")
    print("- No emotion_label")
    print("- No emotion_vector_id")
    print("- One reference for each unique voice × text combination")
    print("="*60)
    
    total_success = 0
    all_failed = []
    
    # Generate for expressivity_none (no suffix)
    success, failed = generate_references_for_expressivity("none")
    total_success += success
    all_failed.extend([f"none/{f}" for f in failed])
    
    # Generate for expressivity_0.6 (with |0.6 suffix)
    success, failed = generate_references_for_expressivity("0.6")
    total_success += success
    all_failed.extend([f"0.6/{f}" for f in failed])
    
    print("\n" + "="*60)
    print("Reference Audio Generation Complete!")
    print(f"Total files generated: {total_success}/144")
    print(f"Expected: 72 files per expressivity type × 2 types = 144 total")
    if all_failed:
        print(f"Failed files: {len(all_failed)}")
        for f in all_failed:
            print(f"  - {f}")
    print("="*60)

if __name__ == "__main__":
    main()