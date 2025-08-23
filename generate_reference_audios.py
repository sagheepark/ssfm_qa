#!/usr/bin/env python3
"""
Generate Reference Audio Files for TTS QA System
These are neutral baseline audios with style_label="normal-1" only (no emotion)
"""

import requests
import json
import time
import os
from pathlib import Path

# API Configuration
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1OTIxMDM0LCJleHAiOjE3NTU5MjQ2MzQsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.e0s4o6VDxd2MxEA8ZPzglKb7TGV7J6wzvvRWvT1sb-ttrwQpneGid5Pt0B0jyQ2bm9j1O8tajkDKCZITwF0Usf5kcp02f5Qdbume-ISfx7HWLxs15qmXEl3xapwtGDU-_SRzAg-9i5ueMKy1TrqfMALi-Ut6zUNvYeZtHBULQ9slTkzKym47AxGWVoCdfSoqgI6yGBRhNgNgCBKKCj4A1CrUk2wGUl5A2Akd3qv5LvSL0S4Zv7vwFClqpJ3G1yRr0DRbMLFRovwu87V83KuDllWgU3QsMVSFQT4pdjWWS3FUiLBbSLO6wSzgiLDQ1gFguw_Tg4zERrllq-6EFFingQ"

BASE_URL = "https://dev.icepeak.ai/api"

# Voice configurations
VOICES = {
    "v001": "688b02990486383d463c9d1a",  # male
    "v002": "689c69984c7990a1ddca2327"   # female
}

# Text configurations - using the actual texts from the test
TEXTS = {
    "match": {
        "angry": "I can't believe you broke your promise again after everything we discussed!",
        "sad": "I really miss the old days when everyone was still here together.",
        "happy": "I'm so thrilled about the wonderful surprise party you organized for me!",
        "whisper": "Don't make any noise, everyone is sleeping in the next room.",
        "toneup": "Did you really win the grand prize in the competition?",
        "tonedown": "Let me explain this matter in a very serious and professional manner.",
        "excited": "We're going on the adventure of a lifetime starting tomorrow morning!",
        "furious": "This is absolutely unacceptable and I demand an explanation immediately!",
        "terrified": "Something is moving in the shadows and I don't know what it is!",
        "fear": "I'm really scared about what might happen if this goes wrong.",
        "surprise": "Oh my goodness, I never expected to see you here today!",
        "excitement": "I can hardly wait to share this amazing news with everyone!"
    },
    "neutral": {
        "angry": "The meeting is scheduled for three o'clock in the conference room.",
        "sad": "The report needs to be submitted by Friday afternoon without fail.",
        "happy": "Please remember to turn off the lights when you leave the office.",
        "whisper": "The quarterly financial report shows steady growth in all departments.",
        "toneup": "The train arrives at platform seven every hour on weekdays.",
        "tonedown": "The document contains information about the new policy changes.",
        "excited": "The temperature today is expected to reach seventy-two degrees.",
        "furious": "The library closes at eight o'clock on weekday evenings.",
        "terrified": "The coffee machine is located on the third floor break room.",
        "fear": "The new software update will be installed next Tuesday morning.",
        "surprise": "The parking lot is located behind the main building entrance.",
        "excitement": "Please fill out the form and return it to the front desk."
    },
    "opposite": {
        "angry": "Your thoughtfulness and kindness truly made my day so much better.",
        "sad": "This is absolutely the best news I've heard all year long!",
        "happy": "Everything seems to be going wrong and nothing works out anymore.",
        "whisper": "Everyone needs to hear this important announcement right now!",
        "toneup": "Everything is perfectly calm and there's nothing to worry about here.",
        "tonedown": "This is so incredibly exciting and I can barely contain myself!",
        "excited": "I'm too exhausted and drained to do anything at all today.",
        "furious": "I completely understand your position and I'm not upset at all.",
        "terrified": "I feel completely safe and protected in this wonderful place.",
        "fear": "I have complete confidence that everything will work out perfectly.",
        "surprise": "This is exactly what I predicted would happen all along.",
        "excitement": "This is rather boring and I'm not interested in it at all."
    }
}

def get_unique_text_for_reference(text_type):
    """Get a single representative text for each text_type for reference audio"""
    # Use the 'happy' emotion text as the representative for each text type
    # This ensures each reference has unique text content
    return TEXTS[text_type]["happy"]

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
        print(f"Request data: {json.dumps(requests_data, indent=2)}")
    
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
    
    # Prepare batch requests
    all_requests = []
    all_file_mappings = []
    
    for voice_name, voice_id in VOICES.items():
        for text_type in ["match", "neutral", "opposite"]:
            # Get the representative text for this text_type
            text = get_unique_text_for_reference(text_type)
            
            # Add expressivity suffix if needed
            if expressivity_type == "0.6":
                text = text + "|0.6"
            
            request = create_tts_request(text, voice_id)
            all_requests.append(request)
            
            # Store mapping for filename
            output_dir = f"public/voices/expressivity_{expressivity_type}/"
            filename = f"{voice_name}_{text_type}_reference.wav"
            all_file_mappings.append({
                "voice": voice_name,
                "text_type": text_type,
                "filename": filename,
                "output_path": os.path.join(output_dir, filename)
            })
    
    print(f"\n{'='*60}")
    print(f"Generating references for expressivity_{expressivity_type}")
    print(f"Total requests: {len(all_requests)}")
    print(f"{'='*60}")
    
    # Process in batches of 4 (API limit)
    batch_size = 4
    for batch_idx in range(0, len(all_requests), batch_size):
        batch_requests = all_requests[batch_idx:batch_idx + batch_size]
        batch_file_mappings = all_file_mappings[batch_idx:batch_idx + batch_size]
        
        print(f"\nProcessing batch {batch_idx//batch_size + 1}/{(len(all_requests) + batch_size - 1)//batch_size}")
        
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
            else:
                print(f"✗ Failed: {batch_file_mappings[i]['filename']}")

def main():
    """Main function to generate all reference audios"""
    print("Starting Reference Audio Generation")
    print("="*60)
    print("Reference audios are neutral baselines:")
    print("- style_label: 'normal-1'")
    print("- No emotion_label")
    print("- No emotion_vector_id")
    print("- Each voice_id × text_type combination")
    print("="*60)
    
    # Generate for expressivity_none (no suffix)
    generate_references_for_expressivity("none")
    
    # Generate for expressivity_0.6 (with |0.6 suffix)
    generate_references_for_expressivity("0.6")
    
    print("\n" + "="*60)
    print("Reference Audio Generation Complete!")
    print("Total files generated: 12 (6 per expressivity type)")
    print("="*60)

if __name__ == "__main__":
    main()