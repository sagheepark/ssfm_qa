#!/usr/bin/env python3
"""
Generate the 4 missing voice files for expressivity_0.6 - Fixed version
"""

import requests
import json
import time
import os
from pathlib import Path

# API Configuration - using newer token from working script
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODgxNjQxLCJleHAiOjE3NTY4ODUyNDEsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.ehcAR-G8fqbf8G3hIluk-Ry7QDzauBolZI94Q6fSmuHFG62nZNou8ZdSRBvQvZaRk8MfCo95dOCvD3nOls9C7XoOt6u7igrewwNbT-SjBqRXpFlBRI8bSu7sAUq03JrE2sI5XjtxUkf30YUVzD3G7yXczAMyh-BGBJV9PfGCrzG4uKWaPheEnsyB01xAtaPYdPCvLDx1SzWz_KZzEYqRXB8KW1_xPYShZ6ffb3c2xRROw7e_XrV6ewmE8EcgLlBjBkhRxf-ywOx8RaaVFEemfuBQtJ6_GCeqBfq4Dm4w4TQj9ZYgY-3I_ijyU_5cO4JK8xlF03z9boAaLp0mJudniA"

BASE_URL = "https://dev.icepeak.ai/api"

# Voice and text configuration
VOICES = {"v002": "68ad0cb625c2800730ac5b48"}

def create_tts_request(text, voice_id, emotion_label, scale):
    """Create TTS request matching working script format"""
    return {
        "text": text,
        "actor_id": voice_id,
        "emotion_label": emotion_label,
        "emotion_scale": float(scale),
        "style_label": "normal-1",
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "bp_c_l": True,
        "adjust_lastword": 0,
        "style_label_version": "v1"
    }

def batch_request_tts(requests_data):
    """Send batch TTS request using correct endpoint"""
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
    headers = {"Authorization": API_TOKEN}
    response = requests.get(download_url, headers=headers)
    response.raise_for_status()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)

def main():
    print("Generating 4 missing voice files...")
    
    # Create output directory
    output_dir = Path("public/voices_2/expressivity_0.6")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Missing files configuration
    missing_files = [
        {"scale": 1.5, "filename": "v002_tonedown_opposite_scale_1.5.wav"},
        {"scale": 2.0, "filename": "v002_tonedown_opposite_scale_2.0.wav"},
        {"scale": 2.5, "filename": "v002_tonedown_opposite_scale_2.5.wav"},
        {"scale": 3.0, "filename": "v002_tonedown_opposite_scale_3.0.wav"}
    ]
    
    voice_id = VOICES["v002"]
    text = "This is so incredibly exciting and I can barely contain myself!|0.6"
    
    # Create batch requests
    batch_requests = []
    for file_info in missing_files:
        request_data = create_tts_request(text, voice_id, "tonedown", file_info["scale"])
        batch_requests.append(request_data)
    
    try:
        # Step 1: Send batch request
        speak_urls = batch_request_tts(batch_requests)
        
        # Step 2: Poll for completion
        results = poll_for_completion(speak_urls)
        
        # Step 3: Download files
        for i, (file_info, result) in enumerate(zip(missing_files, results)):
            filename = file_info["filename"]
            file_path = output_dir / filename
            
            if result.get("status") == "done" and "audio" in result:
                print(f"Downloading {filename}...")
                # Try direct download with authorization
                audio_url = result["audio"]["url"]
                download_audio(audio_url, str(file_path))
                print(f"✓ Successfully generated: {filename}")
            else:
                print(f"✗ Failed to generate {filename}")
                print(f"Status: {result.get('status', 'unknown')}")
                if "audio" not in result:
                    print("No audio data in result")
                
    except Exception as e:
        print(f"✗ Generation failed: {e}")
    
    print("\nGeneration complete!")
    
    # Verify final count
    total_files = len(list(output_dir.glob("*.wav")))
    print(f"Total files in expressivity_0.6: {total_files}")

if __name__ == "__main__":
    main()