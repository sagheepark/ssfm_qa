#!/usr/bin/env python3
"""
Generate complete TTS sample set with all working configurations
74 total samples: 2 reference + 72 emotional (2 actors × 6 emotions × 6 scales)
"""

import time
import requests
from pathlib import Path
import json

def generate_complete_samples():
    """Generate the complete 74-sample TTS set"""
    
    print("=" * 70)
    print("GENERATING COMPLETE TTS SAMPLE SET")
    print("=" * 70)
    
    # Working token
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1NzY1ODMxLCJleHAiOjE3NTU3Njk0MzEsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.jDp9zGN45uZCmNI5UVfW7sdHksNVeDkw0D1KQSH7hS_7ShbmfvMnAx_vMgU5b6fqHTdzN6qA9Ftt-0-d9-2oi-O_oKcBbGvOx6yvr6Fee2HzQMMX3qQVq2xOJUBuTzgH4TgoLpUR4VD-9PIvjP4sjtJymdrD30zbIyB3Zi9woslUhB7dSxn7XO1IhCepPdGPMFOK3DBc8wOVWk_j5ox8FeSJP0jxZf0YQgpMGFP3qd127-sT23I3Zb3wRqJZM0DaNqxzlnrLsaA4Ey6h65C2HhQOi9WFn3KS2HGmaeFdCLCSE1MYmVe1LqJTCulO4vTgUPKxKfCcsYqOASSy87rKFg"
    
    headers = {"Authorization": f"Bearer {token}"}
    host = "https://dev.icepeak.ai"
    
    # Output directory
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear old files first
    print("Clearing old files...")
    old_count = 0
    for old_file in output_dir.glob("*.wav"):
        old_file.unlink()
        old_count += 1
    print(f"Removed {old_count} old files")
    
    # Configuration
    actors = {
        "voice_001": "688b02990486383d463c9d1a",
        "voice_002": "689c693264acbc0a5b9fb0e5"
    }
    
    emotions = ["happy", "sad", "angry", "whisper", "tonedown", "toneup"]
    scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    
    # Emotion-specific texts
    emotion_texts = {
        "happy": "I am so thrilled about the wonderful surprise party you organized for me!",
        "sad": "I really miss the old days when everyone was still here together.",
        "angry": "I cannot believe you broke your promise again after everything we discussed!",
        "whisper": "Let me tell you a secret in a very quiet voice.",
        "tonedown": "Please speak more softly and calmly about this sensitive topic.",
        "toneup": "We need to be more enthusiastic and energetic about this project!"
    }
    
    # Generate sample list
    all_samples = []
    
    # Reference samples (2)
    for voice_name, actor_id in actors.items():
        all_samples.append({
            "filename": f"reference_{voice_name}.wav",
            "text": "This is a reference sample with normal voice and no emotion.",
            "actor_id": actor_id,
            "emotion_label": None,
            "emotion_scale": 1.0,
            "category": "reference"
        })
    
    # Emotional samples (72)
    for voice_name, actor_id in actors.items():
        for emotion in emotions:
            for scale in scales:
                all_samples.append({
                    "filename": f"{emotion}_{voice_name}_scale{scale}.wav",
                    "text": emotion_texts[emotion],
                    "actor_id": actor_id,
                    "emotion_label": emotion,
                    "emotion_scale": scale,
                    "category": "emotional"
                })
    
    total_samples = len(all_samples)
    print(f"\\nTotal samples to generate: {total_samples}")
    print(f"Reference samples: {sum(1 for s in all_samples if s['category'] == 'reference')}")
    print(f"Emotional samples: {sum(1 for s in all_samples if s['category'] == 'emotional')}")
    print(f"Estimated time: {total_samples * 6 / 60:.1f} minutes")
    
    # Generate samples
    success_count = 0
    failed_samples = []
    
    for i, sample in enumerate(all_samples, 1):
        print(f"\\n[{i:2d}/{total_samples}] {sample['filename']}")
        print(f"   Actor: {sample['actor_id'][-8:]}")
        print(f"   Emotion: {sample['emotion_label'] or 'None'}")
        print(f"   Scale: {sample['emotion_scale']}")
        print(f"   Text: {sample['text'][:50]}...")
        
        if process_sample(sample, headers, host, output_dir):
            success_count += 1
            print(f"   ✅ SUCCESS ({success_count}/{i})")
        else:
            print(f"   ❌ FAILED")
            failed_samples.append(sample['filename'])
        
        # Progress update every 10 samples
        if i % 10 == 0:
            print(f"\\n   📊 Progress: {i}/{total_samples} ({i/total_samples*100:.1f}%) - Success rate: {success_count/i*100:.1f}%")
        
        # Rate limiting
        if i < total_samples:
            time.sleep(3)
    
    # Final results
    print(f"\\n{'='*70}")
    print("FINAL GENERATION RESULTS")
    print(f"{'='*70}")
    print(f"Total samples attempted: {total_samples}")
    print(f"Successful generations: {success_count}")
    print(f"Failed generations: {total_samples - success_count}")
    print(f"Success rate: {(success_count/total_samples)*100:.1f}%")
    
    if failed_samples:
        print(f"\\n❌ Failed samples ({len(failed_samples)}):")
        for filename in failed_samples:
            print(f"  - {filename}")
    
    # List generated files by category
    wav_files = list(output_dir.glob("*.wav"))
    print(f"\\nGenerated files ({len(wav_files)}):")
    
    # Group by category
    reference_files = [f for f in wav_files if f.name.startswith("reference_")]
    emotion_files = [f for f in wav_files if not f.name.startswith("reference_")]
    
    print(f"\\nREFERENCE SAMPLES ({len(reference_files)}):")
    for file in sorted(reference_files):
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")
    
    print(f"\\nEMOTIONAL SAMPLES ({len(emotion_files)}):")
    # Group by emotion
    emotion_groups = {}
    for file in emotion_files:
        emotion = file.name.split('_')[0]
        if emotion not in emotion_groups:
            emotion_groups[emotion] = []
        size_kb = file.stat().st_size / 1024
        emotion_groups[emotion].append((file.name, size_kb))
    
    for emotion in sorted(emotion_groups.keys()):
        files_in_emotion = emotion_groups[emotion]
        print(f"\\n  {emotion.upper()} ({len(files_in_emotion)} files):")
        for filename, size_kb in sorted(files_in_emotion):
            print(f"    {filename} ({size_kb:.1f} KB)")
    
    # Save generation metadata
    metadata = {
        "generation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_samples": total_samples,
        "successful_samples": success_count,
        "failed_samples": failed_samples,
        "configuration": {
            "actors": actors,
            "emotions": emotions,
            "scales": scales
        }
    }
    
    metadata_file = output_dir.parent / 'generation_metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\\n📄 Generation metadata saved to: {metadata_file}")
    
    if success_count > 0:
        print(f"\\n🎉 Generated {success_count} TTS samples successfully!")
        print(f"📁 Files saved in: {output_dir}")
        
        if success_count == total_samples:
            print("\\n🏆 PERFECT SCORE - ALL SAMPLES GENERATED!")
        
        return True
    else:
        print(f"\\n😞 No samples were generated successfully")
        return False

def process_sample(sample, headers, host, output_dir):
    """Process a single TTS sample using the 4-step workflow"""
    
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
    
    try:
        # Step 1: Request generation
        speak_response = requests.post(f"{host}/api/speak/batch/post", headers=headers, json=speak_data, timeout=15)
        
        if speak_response.status_code != 200:
            return False
        
        r = speak_response.json()
        speak_urls = r.get("result", {}).get("speak_urls")
        
        if not speak_urls:
            return False
        
        # Step 2: Poll for completion
        for attempt in range(30):  # 15 seconds max wait
            poll_response = requests.post(f"{host}/api/speak/batch/get", headers=headers, json=speak_urls, timeout=15)
            
            if poll_response.status_code != 200:
                return False
                
            poll_result = poll_response.json()["result"][0]
            status = poll_result["status"]
            
            if status == "done":
                # Step 3: Get download URL  
                audio_url = poll_result["audio"]["url"]
                audio_response = requests.get(audio_url + "/cloudfront", headers=headers, timeout=15)
                
                if audio_response.status_code != 200:
                    return False
                
                audio_response_json = audio_response.json()
                real_audio_url = audio_response_json["result"]
                
                # Step 4: Download audio
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
            
            time.sleep(0.5)
        
        return False
        
    except Exception as e:
        return False

if __name__ == "__main__":
    generate_complete_samples()