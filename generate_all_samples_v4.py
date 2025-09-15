#!/usr/bin/env python3
"""
Generate ALL Sample Audio Files for TTS QA System - v4
VERSION 4: REVISED PLAN - Only expressivity_0.6, New Voice IDs, Fresh Token, HD1 Quality
"""

import requests
import json
import time
import os
from pathlib import Path

# Fresh API token from user
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImUzZWU3ZTAyOGUzODg1YTM0NWNlMDcwNTVmODQ2ODYyMjU1YTcwNDYiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NjY4OTI4OCwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU3ODk4OTYzLCJleHAiOjE3NTc5MDI1NjMsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.oMn2KZ15_vrlT_Sqw0XuAWTxwcwdzWmVbOF3UIPLZiB1LDv3JWkmbuUqWa3_D_Piu-Awekg9gjlwr3Hfih8Jr8SFjAw-W9CubEaBj3e_sIeaJBMvCH1BJDh3FiL4a6_fbcg6nMBkX4SNYJPs7S3-gT-HaYuIffJsE_Kuuwlo9uP1sqyMFsEr5skFdsv7zId6kbXftRqtJaF2XCD_19N92eyNprO9FXoiWgAzv2FysUFl5tLc5Aykyx5MZXHtKi1VzRj1JlTHqoA65r13U8gsn6BiSjTyL3bOG-BUcpJmY_wvsjtU9v9-splclgQ6Bgo_zfh0vfO6lTq8l8_uw8_-xA"

BASE_URL = "https://dev.icepeak.ai/api"

# Voice configurations - REVISED VOICE IDs from user
VOICES = {
    "v001": "68c3cbbc39de69ffd6baad5f",  # male
    "v002": "68c3cbc04b464b622eb32355"   # female
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

# ALL emotion texts from docs/tts-test-sentences.md
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

# Scale values from plan.md - updated to match existing pattern
SCALES = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
TEXT_TYPES = ["match", "neutral", "opposite"]

def get_high_quality_audio_url(result):
    """Extract highest quality audio URL from TTS result"""
    audio_section = result.get("audio", {})
    
    # Priority: hd1 is TRUE high quality, not 'high'
    # Based on API testing: 'high' = standard quality, 'hd1' = actual high quality
    if "hd1" in audio_section and audio_section["hd1"].get("url"):
        return audio_section["hd1"]["url"], "hd1" 
    if "high" in audio_section and audio_section["high"].get("url"):
        return audio_section["high"]["url"], "high"
    if audio_section.get("url"):
        return audio_section["url"], "standard"
    if "low" in audio_section and audio_section["low"].get("url"):
        return audio_section["low"]["url"], "low"
        
    return None, None

def get_cloudfront_download_url(audio_url):
    """Get CloudFront optimized download URL (backend method)"""
    headers = {"Authorization": API_TOKEN}
    response = requests.get(f"{audio_url}/cloudfront", headers=headers)
    response.raise_for_status()
    return response.json().get("result")

def download_high_quality_audio(result, output_path):
    """Download highest quality audio using backend approach"""
    audio_url, quality_type = get_high_quality_audio_url(result)
    
    if not audio_url:
        return False, "none", 0
    
    try:
        download_url = get_cloudfront_download_url(audio_url)
        response = requests.get(download_url)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        return True, quality_type, len(response.content)
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False, quality_type, 0

def create_tts_request(text, voice_id, emotion_type, emotion_value, scale):
    """Create a TTS request for sample audio with emotion"""
    request = {
        "text": text,
        "actor_id": voice_id,
        "style_label": "normal-1",
        "emotion_scale": scale,
        "lang": "auto",
        "mode": "one-vocoder",
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
    headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}
    
    response = requests.post(url, json=requests_data, headers=headers)
    response.raise_for_status()
    
    result = response.json()
    return result.get("result", {}).get("speak_urls", [])

def poll_for_completion(speak_urls, max_attempts=30):
    """Poll for TTS completion"""
    url = f"{BASE_URL}/speak/batch/get"
    headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}
    
    for attempt in range(max_attempts):
        response = requests.post(url, json=speak_urls, headers=headers)
        response.raise_for_status()
        
        results = response.json().get("result", [])
        all_done = all(r.get("status") == "done" for r in results)
        
        if all_done:
            return results
        
        time.sleep(3)
    
    raise TimeoutError("TTS generation timed out")

def main():
    """Generate all sample files for voices_3 with HD1 QUALITY"""
    print("🎵 HD1-QUALITY Sample Generation for voices_3")
    print("📋 REVISED PLAN: Only expressivity_0.6, New Voice IDs")
    print("=" * 60)
    
    # Only generate expressivity_0.6 (no expressivity_none needed)
    expressivity_type = "0.6"
    print(f"\n🎵 HD1-QUALITY Sample Generation: expressivity_{expressivity_type}")
    
    all_requests = []
    all_file_mappings = []
    
    # Generate emotion_label samples
    for voice_name, voice_id in VOICES.items():
        for emotion in EMOTION_LABELS:
            for text_type in TEXT_TYPES:
                for scale in SCALES:
                    text_base = EMOTION_TEXTS[emotion][text_type]
                    
                    # Add |0.6 suffix for expressivity_0.6
                    text = f"{text_base}|0.6"
                    
                    request = create_tts_request(text, voice_id, "label", emotion, scale)
                    all_requests.append(request)
                    
                    output_dir = f"public/voices_3/expressivity_{expressivity_type}/"
                    filename = f"{voice_name}_{emotion}_{text_type}_scale_{scale}.wav"
                    all_file_mappings.append({
                        "filename": filename,
                        "output_path": output_dir + filename
                    })
    
    # Generate emotion_vector samples
    for voice_name, voice_id in VOICES.items():
        for emotion, vector_id in EMOTION_VECTORS.items():
            for text_type in TEXT_TYPES:
                for scale in SCALES:
                    text_base = EMOTION_TEXTS[emotion][text_type]
                    
                    text = f"{text_base}|0.6"
                    
                    request = create_tts_request(text, voice_id, "vector", vector_id, scale)
                    all_requests.append(request)
                    
                    output_dir = f"public/voices_3/expressivity_{expressivity_type}/"
                    filename = f"{voice_name}_{emotion}_{text_type}_scale_{scale}.wav"
                    all_file_mappings.append({
                        "filename": filename,
                        "output_path": output_dir + filename
                    })
    
    total_expected = len(VOICES) * (len(EMOTION_LABELS) + len(EMOTION_VECTORS)) * len(TEXT_TYPES) * len(SCALES)
    print(f"📊 Total {expressivity_type} samples to generate: {len(all_requests)}")
    print(f"🎯 Expected: 2 voices × 12 emotions × 3 text_types × 6 scales = {total_expected}")
    
    # Process in batches of 4 (API limit)
    success_count = 0
    quality_stats = {}
    
    for i in range(0, len(all_requests), 4):
        batch = all_requests[i:i+4]
        batch_mappings = all_file_mappings[i:i+4]
        
        print(f"\n🔄 Processing batch {i//4 + 1}/{(len(all_requests) + 3)//4} ({len(batch)} files)...")
        
        try:
            # Send batch request
            speak_urls = batch_request_tts(batch)
            
            # Wait for completion
            results = poll_for_completion(speak_urls)
            
            # Download with HD1 QUALITY
            for j, result in enumerate(results):
                file_info = batch_mappings[j]
                
                if result.get("status") == "done":
                    success, quality, file_size = download_high_quality_audio(result, file_info["output_path"])
                    
                    if success:
                        print(f"✅ {quality.upper()}: {file_info['filename']} ({file_size:,} bytes)")
                        success_count += 1
                        quality_stats[quality] = quality_stats.get(quality, 0) + 1
                    else:
                        print(f"❌ Failed: {file_info['filename']}")
                else:
                    print(f"❌ Generation failed: {file_info['filename']}")
            
        except Exception as e:
            print(f"❌ Batch failed: {e}")
            for file_info in batch_mappings:
                print(f"❌ Failed: {file_info['filename']}")
    
    print(f"\n📈 {expressivity_type} Results:")
    print(f"✅ Success: {success_count}/{len(all_requests)}")
    print(f"🎵 Quality Distribution: {quality_stats}")
    
    # Final verification
    total_files = len(os.listdir(f"public/voices_3/expressivity_{expressivity_type}/"))
    print(f"\n🎯 TOTAL HD1-QUALITY SAMPLES GENERATED: {total_files}")
    print(f"🎵 Expected: 432 sample files")
    print("✅ HD1-QUALITY Sample Generation Complete!")

if __name__ == "__main__":
    main()
