#!/usr/bin/env python3
"""
Generate TTS samples following plan.md requirements EXACTLY
- 2 voices × 3 texts × 6 emotions × 6 scales = 216 emotional samples
- 2 voices × 3 texts × 1 reference = 6 reference samples  
- Total: 222 samples
"""

import time
import requests
from pathlib import Path
import json

def generate_plan_compliant_samples():
    """Generate samples exactly as specified in plan.md"""
    
    print("=" * 80)
    print("GENERATING PLAN.MD COMPLIANT TTS SAMPLES")
    print("=" * 80)
    
    # Working token
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1NzY1ODMxLCJleHAiOjE3NTU3NjkwNzYsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.jDp9zGN45uZCmNI5UVfW7sdHksNVeDkw0D1KQSH7hS_7ShbmfvMnAx_vMgU5b6fqHTdzN6qA9Ftt-0-d9-2oi-O_oKcBbGvOx6yvr6Fee2HzQMMX3qQVq2xOJUBuTzgH4TgoLpUR4VD-9PIvjP4sjtJymdrD30zbIyB3Zi9woslUhB7dSxn7XO1IhCepPdGPMFOK3DBc8wOVWk_j5ox8FeSJP0jxZf0YQgpMGFP3qd127-sT23I3Zb3wRqJZM0DaNqxzlnrLsaA4Ey6h65C2HhQOi9WFn3KS2HGmaeFdCLCSE1MYmVe1LqJTCulO4vTgUPKxKfCcsYqOASSy87rKFg"
    
    headers = {"Authorization": f"Bearer {token}"}
    host = "https://dev.icepeak.ai"
    
    # Output directory
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear old files
    print("Clearing old files...")
    old_count = 0
    for old_file in output_dir.glob("*.wav"):
        old_file.unlink()
        old_count += 1
    print(f"Removed {old_count} old files")
    
    # Configuration as per plan.md
    voices = {
        "v001": "688b02990486383d463c9d1a",  # voice_001
        "v002": "689c693264acbc0a5b9fb0e5"   # voice_002
    }
    
    # 3 different texts as specified in plan.md
    texts = {
        "t001": "I am so thrilled about the wonderful surprise party you organized for me!",
        "t002": "Please listen carefully to the following audio sample for quality evaluation.",
        "t003": "The quick brown fox jumps over the lazy dog in the garden today."
    }
    
    # 6 emotions that work (from our testing)
    emotions = ["happy", "sad", "angry", "whisper", "tonedown", "toneup"]
    
    # 6 emotion scales as per plan.md
    scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    
    # Generate all samples following plan.md structure
    all_samples = []
    
    print("\\n=== SAMPLE STRUCTURE ===")
    print("Format: {voice_id}_{text_idx}_{variant_type}_{variant_value}_{scale}.wav")
    print()
    
    # Reference samples: 2 voices × 3 texts = 6 samples
    print("Reference samples (6):")
    for voice_id, actor_id in voices.items():
        for text_id, text_content in texts.items():
            filename = f"{voice_id}_{text_id}_ref.wav"
            print(f"  {filename}")
            all_samples.append({
                "filename": filename,
                "text": text_content,
                "actor_id": actor_id,
                "voice_id": voice_id,
                "text_id": text_id,
                "emotion_label": None,
                "emotion_scale": 1.0,
                "category": "reference"
            })
    
    # Emotional samples: 2 voices × 3 texts × 6 emotions × 6 scales = 216 samples  
    print(f"\\nEmotional samples (216):")
    print("Sample structure: v001_t001_emo_happy_scale_1.5.wav")
    
    for voice_id, actor_id in voices.items():
        for text_id, text_content in texts.items():
            for emotion in emotions:
                for scale in scales:
                    filename = f"{voice_id}_{text_id}_emo_{emotion}_scale_{scale}.wav"
                    all_samples.append({
                        "filename": filename,
                        "text": text_content,
                        "actor_id": actor_id,
                        "voice_id": voice_id,
                        "text_id": text_id,
                        "emotion_label": emotion,
                        "emotion_scale": scale,
                        "category": "emotional"
                    })
    
    total_samples = len(all_samples)
    reference_count = sum(1 for s in all_samples if s['category'] == 'reference')
    emotional_count = sum(1 for s in all_samples if s['category'] == 'emotional')
    
    print(f"\\n=== GENERATION PLAN ===")
    print(f"Total samples: {total_samples}")
    print(f"Reference samples: {reference_count} (2 voices × 3 texts)")
    print(f"Emotional samples: {emotional_count} (2 voices × 3 texts × 6 emotions × 6 scales)")
    print(f"Estimated time: {total_samples * 6 / 60:.1f} minutes")
    print(f"\\nVariables included in naming:")
    print(f"✅ Voice: {list(voices.keys())}")
    print(f"✅ Text: {list(texts.keys())}")  
    print(f"✅ Emotion: {emotions}")
    print(f"✅ Scale: {scales}")
    
    # Generate samples
    success_count = 0
    failed_samples = []
    
    for i, sample in enumerate(all_samples, 1):
        print(f"\\n[{i:3d}/{total_samples}] {sample['filename']}")
        print(f"   Voice: {sample['voice_id']} | Text: {sample['text_id']} | Emotion: {sample['emotion_label'] or 'None'} | Scale: {sample['emotion_scale']}")
        
        if process_sample(sample, headers, host, output_dir):
            success_count += 1
            print(f"   ✅ SUCCESS ({success_count}/{i})")
        else:
            print(f"   ❌ FAILED")
            failed_samples.append(sample['filename'])
        
        # Progress update every 20 samples
        if i % 20 == 0:
            progress_pct = i/total_samples*100
            success_rate = success_count/i*100
            print(f"\\n   📊 Progress: {i}/{total_samples} ({progress_pct:.1f}%) - Success rate: {success_rate:.1f}%")
        
        # Rate limiting
        if i < total_samples:
            time.sleep(3)
    
    # Final results
    print(f"\\n{'='*80}")
    print("PLAN.MD COMPLIANT GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Total samples: {total_samples}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(failed_samples)}")
    print(f"Success rate: {(success_count/total_samples)*100:.1f}%")
    
    if failed_samples:
        print(f"\\nFailed samples ({len(failed_samples)}):")
        for filename in failed_samples[:10]:  # Show first 10
            print(f"  {filename}")
        if len(failed_samples) > 10:
            print(f"  ... and {len(failed_samples) - 10} more")
    
    # Generate statistics
    wav_files = list(output_dir.glob("*.wav"))
    print(f"\\nGenerated files: {len(wav_files)}")
    
    # Group by category
    ref_files = [f for f in wav_files if "_ref.wav" in f.name]
    emo_files = [f for f in wav_files if "_emo_" in f.name]
    
    print(f"\\nReference files ({len(ref_files)}):")
    for file in sorted(ref_files):
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")
    
    print(f"\\nEmotional files ({len(emo_files)}) - showing first 10:")
    for file in sorted(emo_files)[:10]:
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")
    if len(emo_files) > 10:
        print(f"  ... and {len(emo_files) - 10} more emotional samples")
    
    # Save metadata
    metadata = {
        "generation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "plan_compliance": True,
        "total_samples": total_samples,
        "reference_samples": reference_count,
        "emotional_samples": emotional_count,
        "successful_samples": success_count,
        "failed_samples": failed_samples,
        "configuration": {
            "voices": voices,
            "texts": {k: v[:50] + "..." if len(v) > 50 else v for k, v in texts.items()},
            "emotions": emotions,
            "scales": scales
        },
        "naming_structure": "{voice_id}_{text_idx}_{variant_type}_{variant_value}_{scale}.wav"
    }
    
    metadata_file = output_dir.parent / 'plan_compliant_metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\\n📄 Metadata saved: {metadata_file}")
    
    if success_count > 0:
        print(f"\\n🎉 Generated {success_count} plan.md compliant samples!")
        if success_count == total_samples:
            print("\\n🏆 PERFECT - ALL SAMPLES GENERATED WITH FULL PLAN.MD COMPLIANCE!")
        return True
    else:
        print(f"\\n😞 No samples generated")
        return False

def process_sample(sample, headers, host, output_dir):
    """Process single sample with 4-step TTS workflow"""
    
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
        # Step 1: Request
        speak_response = requests.post(f"{host}/api/speak/batch/post", headers=headers, json=speak_data, timeout=15)
        
        if speak_response.status_code != 200:
            return False
        
        r = speak_response.json()
        speak_urls = r.get("result", {}).get("speak_urls")
        
        if not speak_urls:
            return False
        
        # Step 2: Poll
        for attempt in range(25):
            poll_response = requests.post(f"{host}/api/speak/batch/get", headers=headers, json=speak_urls, timeout=15)
            
            if poll_response.status_code != 200:
                return False
                
            poll_result = poll_response.json()["result"][0]
            status = poll_result["status"]
            
            if status == "done":
                # Step 3: Get URL
                audio_url = poll_result["audio"]["url"]
                audio_response = requests.get(audio_url + "/cloudfront", headers=headers, timeout=15)
                
                if audio_response.status_code != 200:
                    return False
                
                audio_response_json = audio_response.json()
                real_audio_url = audio_response_json["result"]
                
                # Step 4: Download
                real_audio_response = requests.get(real_audio_url, timeout=30)
                
                if real_audio_response.status_code != 200:
                    return False
                
                # Save
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
    generate_plan_compliant_samples()