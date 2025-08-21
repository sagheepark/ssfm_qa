#!/usr/bin/env python3
"""
Simple TTS sample generation based on working notebook pattern
"""

import time
import requests
import json
from pathlib import Path

def create_all_samples():
    """Generate all 218 TTS samples using the notebook approach"""
    
    print("=" * 70)
    print("GENERATING ALL TTS SAMPLES - NOTEBOOK APPROACH")
    print("=" * 70)
    
    # Token that works
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2MzM2OSwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU1NzYzMzY5LCJleHAiOjE3NTU3NjY5NjksImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.EScBGAzSA87MnXRAPsnvwq6Ejbpf3xgfZQvmmM9kf32X49WNKyp4LoLjxmmTXmcY0C66AV4cXkyTdlS89IoD5cgrTw3KdkAPFhLbEnkj5iR18qQuELtND3XV5bFVvgbVLrRD18lrQTd-G09CmU23qmBnNEzAQ6CcEVphTe-8JEqPAGRrepMjP3heWV3UgMDpXe3SmYT5dNHAL_mCpUNFLG7-j8zezu8U8QGqGti_v7agCI-q3Y5dZvxTG3-tIT293wlsVZ_diJMS9sCw5e-Y4pwoyzeeXobgxl2TfyuacF0QIk2eN8L7KsPWWInzDzMUj6ms4IWhIIKS4BnGyGdWgA"
    
    headers = {"Authorization": f"Bearer {token}"}
    host = "https://dev.icepeak.ai"
    
    # Output directory
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test sentences mapping (subset for testing)
    test_sentences = {
        "Happy": {
            "match": "I'm so thrilled about the wonderful surprise party you organized for me!",
            "neutral": "The weather seems quite pleasant today with clear skies ahead.",
            "opposite": "I really miss the old days when everyone was still here together."
        },
        "Angry": {
            "match": "I can't believe you broke your promise again after everything we discussed!",
            "neutral": "The weather seems quite pleasant today with clear skies ahead.",
            "opposite": "I'm so thrilled about the wonderful surprise party you organized for me!"
        },
        "Sad": {
            "match": "I really miss the old days when everyone was still here together.",
            "neutral": "The weather seems quite pleasant today with clear skies ahead.",
            "opposite": "I'm so thrilled about the wonderful surprise party you organized for me!"
        }
    }
    
    # Voice actors
    actors = {
        "voice_001": "688b02990486383d463c9d1a",
        "voice_002": "689c693264acbc0a5b9fb0e5"
    }
    
    # Emotion scales
    scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    
    # Generate samples
    sample_count = 0
    success_count = 0
    
    # Reference samples first
    print("\\nGenerating reference samples...")
    for voice_name, actor_id in actors.items():
        filename = f"reference_{voice_name}.wav"
        print(f"\\nGenerating: {filename}")
        
        speak_data = [{
            "text": "This is a reference sample with normal voice and no emotion.",
            "actor_id": actor_id,
            "tempo": 1,
            "pitch": 0,
            "style_label": "normal-1",
            "style_label_version": "v1",
            "emotion_label": None,
            "emotion_scale": 1,
            "previous_text": "",
            "next_text": "",
            "lang": "auto",
            "mode": "one-vocoder",
            "retake": True,
            "adjust_lastword": 0,
        }]
        
        if process_sample(speak_data, headers, host, output_dir, filename):
            success_count += 1
        sample_count += 1
        
        # Rate limiting
        time.sleep(1)
    
    # Emotional samples
    print("\\nGenerating emotional samples...")
    for emotion, texts in test_sentences.items():
        for text_type, text_content in texts.items():
            for scale in scales:
                for voice_name, actor_id in actors.items():
                    filename = f"{emotion.lower()}_{text_type}_{voice_name}_scale{scale}.wav"
                    print(f"\\nGenerating: {filename}")
                    
                    speak_data = [{
                        "text": text_content,
                        "actor_id": actor_id,
                        "tempo": 1,
                        "pitch": 0,
                        "style_label": "normal-1",
                        "style_label_version": "v1",
                        "emotion_label": emotion,
                        "emotion_scale": scale,
                        "previous_text": "",
                        "next_text": "",
                        "lang": "auto",
                        "mode": "one-vocoder",
                        "retake": True,
                        "adjust_lastword": 0,
                    }]
                    
                    if process_sample(speak_data, headers, host, output_dir, filename):
                        success_count += 1
                    sample_count += 1
                    
                    # Rate limiting
                    time.sleep(1)
    
    print(f"\\n{'='*70}")
    print("GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"Total samples attempted: {sample_count}")
    print(f"Successful generations: {success_count}")
    print(f"Failed generations: {sample_count - success_count}")
    print(f"Success rate: {(success_count/sample_count)*100:.1f}%")

def process_sample(speak_data, headers, host, output_dir, filename):
    """Process a single TTS sample using the notebook approach"""
    
    try:
        # Step 1: Request generation
        speak_response = requests.post(f"{host}/api/speak/batch/post", headers=headers, json=speak_data)
        
        if speak_response.status_code != 200:
            print(f"   ❌ Request failed: {speak_response.status_code}")
            return False
        
        r = speak_response.json()
        speak_urls = r.get("result", {}).get("speak_urls")
        
        if not speak_urls:
            print("   ❌ No speak URLs received")
            return False
        
        # Step 2: Poll for completion
        for attempt in range(20):
            poll_response = requests.post(f"{host}/api/speak/batch/get", headers=headers, json=speak_urls)
            
            if poll_response.status_code != 200:
                print(f"   ❌ Poll failed: {poll_response.status_code}")
                return False
                
            poll_result = poll_response.json()["result"][0]
            status = poll_result["status"]
            
            if status == "done":
                # Step 3: Get download URL
                audio_url = poll_result["audio"]["url"]
                audio_response = requests.get(audio_url + "/cloudfront", headers=headers)
                
                if audio_response.status_code != 200:
                    print(f"   ❌ CloudFront URL failed: {audio_response.status_code}")
                    return False
                
                audio_response_json = audio_response.json()
                real_audio_url = audio_response_json["result"]
                
                # Step 4: Download audio
                real_audio_response = requests.get(real_audio_url)
                
                if real_audio_response.status_code != 200:
                    print(f"   ❌ Audio download failed: {real_audio_response.status_code}")
                    return False
                
                # Save file
                file_path = output_dir / filename
                with open(file_path, "wb") as audio_file:
                    audio_file.write(real_audio_response.content)
                
                print(f"   ✅ Saved: {file_path}")
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
    create_all_samples()