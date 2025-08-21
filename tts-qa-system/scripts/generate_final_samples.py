#!/usr/bin/env python3
"""
Generate final comprehensive TTS sample set with proper naming
"""

import time
import requests
from pathlib import Path

def generate_final_samples():
    """Generate comprehensive TTS samples with working configurations"""
    
    print("=" * 70)
    print("GENERATING FINAL TTS SAMPLE SET")
    print("=" * 70)
    
    # Fresh token
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NDMzMCwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5MVU0bUo5M2QyIiwiaWF0IjoxNzU1NzY0MzMwLCJleHAiOjE3NTU3Njc5MzAsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.Nw49Oc7M0IVXRlr0qgRoVbvplrOVr9XGRAi58EcPpogjPQi_03ATaQzt_QuTLtGtyea-CeLeepaBBCcrBIYdVoaf5_nuSPCs4zwoETvB3sAbuN_vlA5FBsH_xSW2q8WdtfoTbKkyrsetXe95IgLmM2Dwg5i0hMr3kwvFZaMFKlAR91NQ_J-3mYJG3b-TsvSMFvUx5e_QA5DfxzOXial-QPAgeke8DAESqxVrTjtiBE-wilxO0nAtSamZV-02jaJpA-jXSEOdRW9esBwyX5mGsLGW0il4G-f1sb7bqVfWnS7My7Ulx72tvxgK5NqOnhZFn0CD7X4MzhD7-5LbyDL05A"
    
    headers = {"Authorization": f"Bearer {token}"}
    host = "https://dev.icepeak.ai"
    
    # Output directory
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Working configuration
    actor_id = "688b02990486383d463c9d1a"  
    voice_name = "voice_001"
    
    # Comprehensive text variations for quality evaluation
    text_variations = [
        {
            "name": "reference",
            "text": "This is a reference sample with normal voice and no emotion."
        },
        {
            "name": "neutral", 
            "text": "The weather seems quite pleasant today with clear skies ahead."
        },
        {
            "name": "greeting",
            "text": "Hello and welcome to our text-to-speech demonstration system."
        },
        {
            "name": "instruction",
            "text": "Please listen carefully to the following audio sample for quality evaluation."
        },
        {
            "name": "question",
            "text": "Can you hear the difference in voice quality between these samples?"
        },
        {
            "name": "statement",
            "text": "The quick brown fox jumps over the lazy dog in the garden."
        }
    ]
    
    # Voice parameter variations
    quality_params = [
        {"tempo": 1.0, "pitch": 0, "suffix": "normal"},
        {"tempo": 0.8, "pitch": 0, "suffix": "slow"},
        {"tempo": 1.2, "pitch": 0, "suffix": "fast"},
        {"tempo": 1.0, "pitch": -2, "suffix": "low_pitch"},
        {"tempo": 1.0, "pitch": 2, "suffix": "high_pitch"}
    ]
    
    # Generate sample set
    all_samples = []
    for text_var in text_variations:
        for params in quality_params:
            sample = {
                "filename": f"{text_var['name']}_{voice_name}_{params['suffix']}.wav",
                "text": text_var["text"],
                "actor_id": actor_id,
                "tempo": params["tempo"],
                "pitch": params["pitch"]
            }
            all_samples.append(sample)
    
    total_samples = len(all_samples)
    print(f"\\nGenerating {total_samples} TTS samples...")
    print(f"Text variations: {len(text_variations)}")
    print(f"Voice parameters: {len(quality_params)}")
    print(f"Using actor: {voice_name}")
    print(f"Estimated time: {total_samples * 4 / 60:.1f} minutes")
    
    success_count = 0
    
    for i, sample in enumerate(all_samples, 1):
        print(f"\\n[{i:2d}/{total_samples}] {sample['filename']}")
        print(f"   Text: {sample['text'][:50]}...")
        print(f"   Tempo: {sample['tempo']}, Pitch: {sample['pitch']}")
        
        if process_sample(sample, headers, host, output_dir):
            success_count += 1
            print(f"   ✅ SUCCESS ({success_count}/{i})")
        else:
            print(f"   ❌ FAILED")
        
        if i < total_samples:
            time.sleep(3)
    
    # Results
    print(f"\\n{'='*70}")
    print("FINAL GENERATION RESULTS")
    print(f"{'='*70}")
    print(f"Total samples: {total_samples}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_samples - success_count}")
    print(f"Success rate: {(success_count/total_samples)*100:.1f}%")
    
    # List files
    wav_files = list(output_dir.glob("*.wav"))
    print(f"\\nGenerated files ({len(wav_files)}):")
    for file in sorted(wav_files):
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")
    
    if success_count > 0:
        print(f"\\n🎉 Generated {success_count} TTS samples successfully!")
        return True
    else:
        print(f"\\n😞 No samples generated")
        return False

def process_sample(sample, headers, host, output_dir):
    """Process a single TTS sample"""
    
    speak_data = [{
        "text": sample["text"],
        "actor_id": sample["actor_id"],
        "tempo": sample["tempo"],
        "pitch": sample["pitch"],
        "style_label": "normal-1",
        "style_label_version": "v1",
        "emotion_label": None,
        "emotion_scale": 1.0,
        "previous_text": "",
        "next_text": "",
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "adjust_lastword": 0,
    }]
    
    try:
        # Request generation
        speak_response = requests.post(f"{host}/api/speak/batch/post", headers=headers, json=speak_data, timeout=15)
        
        if speak_response.status_code != 200:
            return False
        
        r = speak_response.json()
        speak_urls = r.get("result", {}).get("speak_urls")
        
        if not speak_urls:
            return False
        
        # Poll for completion
        for attempt in range(25):
            poll_response = requests.post(f"{host}/api/speak/batch/get", headers=headers, json=speak_urls, timeout=15)
            
            if poll_response.status_code != 200:
                return False
                
            poll_result = poll_response.json()["result"][0]
            status = poll_result["status"]
            
            if status == "done":
                # Get download URL
                audio_url = poll_result["audio"]["url"]
                audio_response = requests.get(audio_url + "/cloudfront", headers=headers, timeout=15)
                
                if audio_response.status_code != 200:
                    return False
                
                audio_response_json = audio_response.json()
                real_audio_url = audio_response_json["result"]
                
                # Download audio
                real_audio_response = requests.get(real_audio_url, timeout=30)
                
                if real_audio_response.status_code != 200:
                    return False
                
                # Save file
                file_path = output_dir / sample["filename"]
                with open(file_path, "wb") as audio_file:
                    audio_file.write(real_audio_response.content)
                
                file_size_kb = len(real_audio_response.content) / 1024
                print(f"   Saved: {file_size_kb:.1f} KB")
                return True
                
            elif status in ["failed", "error"]:
                return False
            
            time.sleep(0.6)
        
        return False
        
    except Exception as e:
        print(f"   Exception: {str(e)}")
        return False

if __name__ == "__main__":
    generate_final_samples()