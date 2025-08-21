#!/usr/bin/env python3
"""
Generate TTS samples with only working configurations
"""

import time
import requests
import json
from pathlib import Path

def generate_working_samples():
    """Generate TTS samples using only confirmed working parameters"""
    
    print("=" * 70)
    print("GENERATING WORKING TTS SAMPLES")
    print("=" * 70)
    
    # Token that works
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2MzM2OSwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU1NzYzMzY5LCJleHAiOjE3NTU3NjY5NjksImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.EScBGAzSA87MnXRAPsnvwq6Ejbpf3xgfZQvmmM9kf32X49WNKyp4LoLjxmmTXmcY0C66AV4cXkyTdlS89IoD5cgrTw3KdkAPFhLbEnkj5iR18qQuELtND3XV5bFVvgbVLrRD18lrQTd-G09CmU23qmBnNEzAQ6CcEVphTe-8JEqPAGRrepMjP3heWV3UgMDpXe3SmYT5dNHAL_mCpUNFLG7-j8zezu8U8QGqGti_v7agCI-q3Y5dZvxTG3-tIT293wlsVZ_diJMS9sCw5e-Y4pwoyzeeXobgxl2TfyuacF0QIk2eN8L7KsPWWInzDzMUj6ms4IWhIIKS4BnGyGdWgA"
    
    headers = {"Authorization": f"Bearer {token}"}
    host = "https://dev.icepeak.ai"
    
    # Output directory
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Only working configurations
    # Actor: Only voice_001 works
    actor_id = "688b02990486383d463c9d1a"
    voice_name = "voice_001"
    
    # Test sentences from tts-test-sentences.md (subset)
    test_sentences = {
        "Normal": {
            "neutral": "This is a reference sample with normal voice and no emotion.",
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
    
    # Emotion scales to test
    scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    
    # Generate samples
    sample_count = 0
    success_count = 0
    
    print(f"\\nUsing actor: {voice_name} ({actor_id})")
    print(f"Emotions to test: {list(test_sentences.keys())}")
    print(f"Scales to test: {scales}")
    
    # Calculate total samples
    total_samples = 0
    for emotion, texts in test_sentences.items():
        if emotion == "Normal":
            total_samples += 1  # Just one reference sample
        else:
            total_samples += len(texts) * len(scales)  # text_types * scales
    
    print(f"Total samples to generate: {total_samples}")
    print(f"Estimated time: {total_samples * 5 / 60:.1f} minutes")
    
    # Generate samples
    for emotion, texts in test_sentences.items():
        print(f"\\n--- {emotion.upper()} SAMPLES ---")
        
        if emotion == "Normal":
            # Reference sample
            filename = f"reference_{voice_name}.wav"
            text_content = texts["neutral"]
            
            print(f"\\nGenerating: {filename}")
            
            if process_sample(
                text_content, actor_id, None, 1.0,
                headers, host, output_dir, filename
            ):
                success_count += 1
            sample_count += 1
            time.sleep(2)  # Rate limiting
            
        else:
            # Emotional samples
            for text_type, text_content in texts.items():
                for scale in scales:
                    filename = f"{emotion.lower()}_{text_type}_{voice_name}_scale{scale}.wav"
                    
                    print(f"\\nGenerating: {filename}")
                    print(f"   Text: {text_content[:50]}...")
                    print(f"   Emotion: {emotion}, Scale: {scale}")
                    
                    if process_sample(
                        text_content, actor_id, emotion, scale,
                        headers, host, output_dir, filename
                    ):
                        success_count += 1
                    sample_count += 1
                    
                    # Rate limiting
                    time.sleep(2)
    
    print(f"\\n{'='*70}")
    print("GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"Total samples attempted: {sample_count}")
    print(f"Successful generations: {success_count}")
    print(f"Failed generations: {sample_count - success_count}")
    print(f"Success rate: {(success_count/sample_count)*100:.1f}%")
    
    # List all generated files
    wav_files = list(output_dir.glob("*.wav"))
    print(f"\\nAll generated files ({len(wav_files)}):")
    for file in sorted(wav_files):
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")

def process_sample(text, actor_id, emotion_label, emotion_scale, headers, host, output_dir, filename):
    """Process a single TTS sample"""
    
    speak_data = [{
        "text": text,
        "actor_id": actor_id,
        "tempo": 1,
        "pitch": 0,
        "style_label": "normal-1",
        "style_label_version": "v1",
        "emotion_label": emotion_label,
        "emotion_scale": emotion_scale,
        "previous_text": "",
        "next_text": "",
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "adjust_lastword": 0,
    }]
    
    try:
        # Step 1: Request generation
        speak_response = requests.post(f"{host}/api/speak/batch/post", headers=headers, json=speak_data, timeout=15)
        
        if speak_response.status_code != 200:
            print(f"   ❌ Request failed: {speak_response.status_code}")
            try:
                error_info = speak_response.json()
                print(f"   Error: {error_info}")
            except:
                print(f"   Error text: {speak_response.text}")
            return False
        
        r = speak_response.json()
        speak_urls = r.get("result", {}).get("speak_urls")
        
        if not speak_urls:
            print("   ❌ No speak URLs received")
            return False
        
        # Step 2: Poll for completion
        for attempt in range(40):  # Increased timeout for emotional samples
            poll_response = requests.post(f"{host}/api/speak/batch/get", headers=headers, json=speak_urls, timeout=15)
            
            if poll_response.status_code != 200:
                print(f"   ❌ Poll failed: {poll_response.status_code}")
                return False
                
            poll_result = poll_response.json()["result"][0]
            status = poll_result["status"]
            
            if attempt % 5 == 0 or status in ["done", "failed", "error"]:
                print(f"   Poll #{attempt+1}: Status = {status}")
            
            if status == "done":
                # Step 3: Get download URL
                audio_url = poll_result["audio"]["url"]
                audio_response = requests.get(audio_url + "/cloudfront", headers=headers, timeout=15)
                
                if audio_response.status_code != 200:
                    print(f"   ❌ CloudFront URL failed: {audio_response.status_code}")
                    return False
                
                audio_response_json = audio_response.json()
                real_audio_url = audio_response_json["result"]
                
                # Step 4: Download audio
                real_audio_response = requests.get(real_audio_url, timeout=30)
                
                if real_audio_response.status_code != 200:
                    print(f"   ❌ Audio download failed: {real_audio_response.status_code}")
                    return False
                
                # Save file
                file_path = output_dir / filename
                with open(file_path, "wb") as audio_file:
                    audio_file.write(real_audio_response.content)
                
                file_size_kb = len(real_audio_response.content) / 1024
                print(f"   ✅ Saved: {file_path.name} ({file_size_kb:.1f} KB)")
                return True
                
            elif status in ["failed", "error"]:
                print(f"   ❌ Generation failed: {status}")
                error_msg = poll_result.get('error', 'no error details')
                print(f"   Error details: {error_msg}")
                return False
            
            # Still processing
            time.sleep(0.5)
        
        print("   ❌ Timeout waiting for completion")
        return False
        
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    generate_working_samples()