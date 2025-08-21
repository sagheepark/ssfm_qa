#!/usr/bin/env python3
"""
Test the complete generation flow with a few samples
"""

import time
import requests
import json
from pathlib import Path

def test_generation_flow():
    """Test generating a few samples to debug the flow"""
    
    print("=" * 70)
    print("TESTING GENERATION FLOW")
    print("=" * 70)
    
    # Token that works
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2MzM2OSwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU1NzYzMzY5LCJleHAiOjE3NTU3NjY5NjksImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.EScBGAzSA87MnXRAPsnvwq6Ejbpf3xgfZQvmmM9kf32X49WNKyp4LoLjxmmTXmcY0C66AV4cXkyTdlS89IoD5cgrTw3KdkAPFhLbEnkj5iR18qQuELtND3XV5bFVvgbVLrRD18lrQTd-G09CmU23qmBnNEzAQ6CcEVphTe-8JEqPAGRrepMjP3heWV3UgMDpXe3SmYT5dNHAL_mCpUNFLG7-j8zezu8U8QGqGti_v7agCI-q3Y5dZvxTG3-tIT293wlsVZ_diJMS9sCw5e-Y4pwoyzeeXobgxl2TfyuacF0QIk2eN8L7KsPWWInzDzMUj6ms4IWhIIKS4BnGyGdWgA"
    
    headers = {"Authorization": f"Bearer {token}"}
    host = "https://dev.icepeak.ai"
    
    # Output directory
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test samples
    test_samples = [
        {
            "filename": "test_voice_001_normal.wav",
            "text": "This is a test with voice 001 and normal emotion.",
            "actor_id": "688b02990486383d463c9d1a",
            "emotion_label": None,
            "emotion_scale": 1.0
        },
        {
            "filename": "test_voice_002_normal.wav", 
            "text": "This is a test with voice 002 and normal emotion.",
            "actor_id": "689c693264acbc0a5b9fb0e5",
            "emotion_label": None,
            "emotion_scale": 1.0
        },
        {
            "filename": "test_voice_001_happy.wav",
            "text": "I'm so thrilled about the wonderful surprise party you organized for me!",
            "actor_id": "688b02990486383d463c9d1a", 
            "emotion_label": "Happy",
            "emotion_scale": 2.0
        },
        {
            "filename": "test_voice_002_sad.wav",
            "text": "I really miss the old days when everyone was still here together.",
            "actor_id": "689c693264acbc0a5b9fb0e5",
            "emotion_label": "Sad", 
            "emotion_scale": 1.5
        }
    ]
    
    success_count = 0
    
    for i, sample in enumerate(test_samples, 1):
        print(f"\\n{i}/{len(test_samples)}: Generating {sample['filename']}")
        print(f"   Text: {sample['text'][:50]}...")
        print(f"   Actor: {sample['actor_id']}")
        print(f"   Emotion: {sample['emotion_label']}")
        print(f"   Scale: {sample['emotion_scale']}")
        
        speak_data = [{
            "text": sample["text"],
            "actor_id": sample["actor_id"], 
            "tempo": 1,
            "pitch": 0,
            "style_label": "normal-1",
            "style_label_version": "v1",
            "emotion_label": sample["emotion_label"],
            "emotion_scale": sample["emotion_scale"],
            "previous_text": "",
            "next_text": "",
            "lang": "auto",
            "mode": "one-vocoder",
            "retake": True,
            "adjust_lastword": 0,
        }]
        
        if process_sample(speak_data, headers, host, output_dir, sample["filename"]):
            success_count += 1
        
        # Rate limiting between requests
        if i < len(test_samples):
            print(f"   Waiting 2 seconds...")
            time.sleep(2)
    
    print(f"\\n{'='*70}")
    print("TEST RESULTS")
    print(f"{'='*70}")
    print(f"Successful generations: {success_count}/{len(test_samples)}")
    print(f"Success rate: {(success_count/len(test_samples))*100:.1f}%")
    
    # List generated files
    wav_files = list(output_dir.glob("*.wav"))
    print(f"\\nGenerated files ({len(wav_files)}):")
    for file in sorted(wav_files):
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")

def process_sample(speak_data, headers, host, output_dir, filename):
    """Process a single TTS sample using the notebook approach"""
    
    try:
        # Step 1: Request generation
        print(f"   Step 1: Requesting TTS generation...")
        speak_response = requests.post(f"{host}/api/speak/batch/post", headers=headers, json=speak_data, timeout=10)
        
        if speak_response.status_code != 200:
            print(f"   ❌ Request failed: {speak_response.status_code}")
            try:
                error_info = speak_response.json()
                print(f"   Error details: {error_info}")
            except:
                print(f"   Error text: {speak_response.text}")
            return False
        
        r = speak_response.json()
        speak_urls = r.get("result", {}).get("speak_urls")
        
        if not speak_urls:
            print("   ❌ No speak URLs received")
            print(f"   Response: {r}")
            return False
        
        print(f"   Step 2: Got speak URLs: {speak_urls}")
        
        # Step 2: Poll for completion
        print(f"   Step 3: Polling for completion...")
        for attempt in range(30):  # Increased timeout
            poll_response = requests.post(f"{host}/api/speak/batch/get", headers=headers, json=speak_urls, timeout=10)
            
            if poll_response.status_code != 200:
                print(f"   ❌ Poll failed: {poll_response.status_code}")
                return False
                
            poll_result = poll_response.json()["result"][0]
            status = poll_result["status"]
            print(f"   Poll #{attempt+1}: Status = {status}")
            
            if status == "done":
                # Step 3: Get download URL
                print(f"   Step 4: Getting download URL...")
                audio_url = poll_result["audio"]["url"]
                audio_response = requests.get(audio_url + "/cloudfront", headers=headers, timeout=10)
                
                if audio_response.status_code != 200:
                    print(f"   ❌ CloudFront URL failed: {audio_response.status_code}")
                    return False
                
                audio_response_json = audio_response.json()
                real_audio_url = audio_response_json["result"]
                print(f"   Step 5: Real audio URL: {real_audio_url[:50]}...")
                
                # Step 4: Download audio
                print(f"   Step 6: Downloading audio...")
                real_audio_response = requests.get(real_audio_url, timeout=30)
                
                if real_audio_response.status_code != 200:
                    print(f"   ❌ Audio download failed: {real_audio_response.status_code}")
                    return False
                
                # Save file
                file_path = output_dir / filename
                with open(file_path, "wb") as audio_file:
                    audio_file.write(real_audio_response.content)
                
                file_size_kb = len(real_audio_response.content) / 1024
                print(f"   ✅ Saved: {file_path} ({file_size_kb:.1f} KB)")
                return True
                
            elif status == "error":
                print(f"   ❌ Generation failed: {poll_result.get('error', 'unknown error')}")
                return False
            
            # Still processing
            time.sleep(0.5)
        
        print("   ❌ Timeout waiting for completion")
        return False
        
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    test_generation_flow()