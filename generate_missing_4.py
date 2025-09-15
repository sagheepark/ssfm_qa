#!/usr/bin/env python3
"""
Generate the 4 missing voice files for expressivity_0.6
"""

import requests
import json
import os
from pathlib import Path

# API Configuration - using newer token from working script
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODgxNjQwLCJleHAiOjE3NTY4ODUyNDAsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.SsivGl7-2rHtcHKKxMKW3d-EsstGmO_H5IAgkGQH4GGrXaU6tGdcXMYN5NEJQdwP7dl_EHbcslIMnY_XYMXN74muHzNq2Rynze9Lfg9fl0gzGMpgZIHJAfCWFie9lwOYDPnMP7MNQi1CVOoDYsdstkOQmRpTHOLlClxJCctP2GDEFxMvpFr2Aqdv0OeTtfCHoQCYfJzjn1FDN23AL86NhSDI-GrjwdzyEFEHWUFxdgbvzx-_azJTfj8tb4qhnQJ8ZYBEOlgLV1tt14v2jZa6TaULoomSHvATotz5d87R5es_dVAhs-fWvO9ahDWX8CYZNUD56HmZQZdfyPsVKHWmxg"

BASE_URL = "https://dev.icepeak.ai/api"

# Voice and text configuration
VOICES = {"v002": "68ad0cb625c2800730ac5b48"}

# Text content for tonedown_opposite
TEXT_CONTENT = {
    "tonedown_opposite": "This is so incredibly exciting and I can barely contain myself!|0.6"
}

def create_tts_request(text, voice_id, emotion_type, emotion_value, scale):
    return {
        "text": text,
        "lang": "auto",
        "actor_id": voice_id,
        "emotion_label": emotion_value,
        "emotion_scale": float(scale),
        "style_label": "normal-1",
        "mode": "one-vocoder"
    }

def send_batch_request(requests_data):
    """Send batch TTS requests using dev.icepeak.ai API"""
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }
    
    batch_data = {"batch": requests_data}
    response = requests.post(f"{BASE_URL}/tts/batch", headers=headers, json=batch_data)
    return response

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
    text = TEXT_CONTENT["tonedown_opposite"]
    
    # Create batch request (all 4 files in one batch)
    batch_requests = []
    for file_info in missing_files:
        request_data = create_tts_request(text, voice_id, "emotion_label", "tonedown", file_info["scale"])
        batch_requests.append(request_data)
    
    print(f"Sending batch request for {len(batch_requests)} files...")
    
    # Send batch request
    response = send_batch_request(batch_requests)
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            
            # Save files
            for i, file_info in enumerate(missing_files):
                filename = file_info["filename"]
                file_path = output_dir / filename
                
                # Get audio data from batch response
                if i < len(response_data) and 'audio_url' in response_data[i]:
                    audio_response = requests.get(response_data[i]['audio_url'])
                    if audio_response.status_code == 200:
                        with open(file_path, 'wb') as f:
                            f.write(audio_response.content)
                        print(f"✓ Successfully generated: {filename}")
                    else:
                        print(f"✗ Failed to download audio for {filename}")
                else:
                    print(f"✗ No audio data for {filename}")
                    
        except Exception as e:
            print(f"✗ Error processing batch response: {e}")
            print(f"Response content: {response.text}")
    else:
        print(f"✗ Batch request failed: {response.status_code}")
        print(f"Response: {response.text}")
    
    print("\nGeneration complete!")
    
    # Verify final count
    total_files = len(list(output_dir.glob("*.wav")))
    print(f"Total files in expressivity_0.6: {total_files}")

if __name__ == "__main__":
    main()