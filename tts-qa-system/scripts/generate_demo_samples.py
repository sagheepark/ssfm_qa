#!/usr/bin/env python3
"""
Generate a small set of demo TTS samples that work reliably
"""

import time
import requests
from pathlib import Path

def generate_demo_samples():
    """Generate a reliable demo set of TTS samples"""
    
    print("=" * 70)
    print("GENERATING DEMO TTS SAMPLES")
    print("=" * 70)
    
    # Token that works
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NDMzMCwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5MVU0bUo5M2QyIiwiaWF0IjoxNzU1NzY0MzMwLCJleHAiOjE3NTU3Njc5MzAsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.Nw49Oc7M0IVXRlr0qgRoVbvplrOVr9XGRAi58EcPpogjPQi_03ATaQzt_QuTLtGtyea-CeLeepaBBCcrBIYdVoaf5_nuSPCs4zwoETvB3sAbuN_vlA5FBsH_xSW2q8WdtfoTbKkyrsetXe95IgLmM2Dwg5i0hMr3kwvFZaMFKlAR91NQ_J-3mYJG3b-TsvSMFvUx5e_QA5DfxzOXial-QPAgeke8DAESqxVrTjtiBE-wilxO0nAtSamZV-02jaJpA-jXSEOdRW9esBwyX5mGsLGW0il4G-f1sb7bqVfWnS7My7Ulx72tvxgK5NqOnhZFn0CD7X4MzhD7-5LbyDL05A"
    
    headers = {"Authorization": f"Bearer {token}"}
    host = "https://dev.icepeak.ai"
    
    # Output directory
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Demo samples - only use configurations that work reliably
    demo_samples = [
        {
            "filename": "demo_normal_reference.wav",
            "text": "This is a reference sample with normal voice and no emotion.",
            "actor_id": "688b02990486383d463c9d1a",
            "emotion_label": None,
            "emotion_scale": 1.0
        },
        {
            "filename": "demo_normal_neutral.wav",
            "text": "The weather seems quite pleasant today with clear skies ahead.",
            "actor_id": "688b02990486383d463c9d1a", 
            "emotion_label": None,
            "emotion_scale": 1.0
        },
        {
            "filename": "demo_angry_match_scale1.wav",
            "text": "I can't believe you broke your promise again after everything we discussed!",
            "actor_id": "688b02990486383d463c9d1a",
            "emotion_label": "Angry",
            "emotion_scale": 1.0
        },
        {
            "filename": "demo_angry_match_scale2.wav",
            "text": "I can't believe you broke your promise again after everything we discussed!",
            "actor_id": "688b02990486383d463c9d1a",
            "emotion_label": "Angry", 
            "emotion_scale": 2.0
        },
        {
            "filename": "demo_sad_match_scale1.wav",
            "text": "I really miss the old days when everyone was still here together.",
            "actor_id": "688b02990486383d463c9d1a",
            "emotion_label": "Sad",
            "emotion_scale": 1.0
        },
        {
            "filename": "demo_sad_match_scale2.wav", 
            "text": "I really miss the old days when everyone was still here together.",
            "actor_id": "688b02990486383d463c9d1a",
            "emotion_label": "Sad",
            "emotion_scale": 2.0
        }
    ]
    
    print(f"Generating {len(demo_samples)} demo samples...")
    print(f"Using actor ID: 688b02990486383d463c9d1a (voice_001)")
    print(f"Output directory: {output_dir}")
    
    success_count = 0
    
    for i, sample in enumerate(demo_samples, 1):
        print(f"\\n{i}/{len(demo_samples)}: {sample['filename']}")
        print(f"   Text: {sample['text'][:60]}...")
        print(f"   Emotion: {sample['emotion_label'] or 'None'}, Scale: {sample['emotion_scale']}")
        
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
        
        # Process the sample
        if process_sample(speak_data, headers, host, output_dir, sample["filename"]):
            success_count += 1
            print(f"   ✅ SUCCESS")
        else:
            print(f"   ❌ FAILED")
        
        # Rate limiting between requests
        if i < len(demo_samples):
            print(f"   Waiting 3 seconds before next request...")
            time.sleep(3)
    
    # Final results
    print(f"\\n{'='*70}")
    print("DEMO GENERATION RESULTS")
    print(f"{'='*70}")
    print(f"Total samples: {len(demo_samples)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(demo_samples) - success_count}")
    print(f"Success rate: {(success_count/len(demo_samples))*100:.1f}%")
    
    # List all generated files
    wav_files = list(output_dir.glob("*.wav"))
    print(f"\\nAll generated files ({len(wav_files)}):")
    for file in sorted(wav_files):
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")
    
    if success_count > 0:
        print(f"\\n🎉 TTS generation pipeline is working!")
        print(f"Generated files are saved in: {output_dir}")
        return True
    else:
        print(f"\\n😞 No samples were generated successfully")
        return False

def process_sample(speak_data, headers, host, output_dir, filename):
    """Process a single TTS sample with the notebook approach"""
    
    try:
        # Step 1: Request generation
        speak_response = requests.post(f"{host}/api/speak/batch/post", headers=headers, json=speak_data, timeout=15)
        
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
            poll_response = requests.post(f"{host}/api/speak/batch/get", headers=headers, json=speak_urls, timeout=15)
            
            if poll_response.status_code != 200:
                print(f"   ❌ Poll failed: {poll_response.status_code}")
                return False
                
            poll_result = poll_response.json()["result"][0]
            status = poll_result["status"]
            
            if status == "done":
                # Step 3: Get download URL  
                audio_url = poll_result["audio"]["url"]
                audio_response = requests.get(audio_url + "/cloudfront", headers=headers, timeout=15)
                
                if audio_response.status_code != 200:
                    print(f"   ❌ CloudFront failed: {audio_response.status_code}")
                    return False
                
                audio_response_json = audio_response.json()
                real_audio_url = audio_response_json["result"]
                
                # Step 4: Download audio
                real_audio_response = requests.get(real_audio_url, timeout=30)
                
                if real_audio_response.status_code != 200:
                    print(f"   ❌ Download failed: {real_audio_response.status_code}")
                    return False
                
                # Save file
                file_path = output_dir / filename
                with open(file_path, "wb") as audio_file:
                    audio_file.write(real_audio_response.content)
                
                file_size_kb = len(real_audio_response.content) / 1024
                print(f"   Saved: {file_size_kb:.1f} KB")
                return True
                
            elif status in ["failed", "error"]:
                print(f"   ❌ Generation failed: {status}")
                return False
            
            # Still processing
            time.sleep(0.5)
        
        print("   ❌ Timeout")
        return False
        
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    generate_demo_samples()