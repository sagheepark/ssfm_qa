#!/usr/bin/env python3
"""
Generate complete TTS samples following updated plan.md requirements EXACTLY
- 12 emotions: 6 emotion_label + 6 emotion_vector_id
- 3 text types per emotion: match, neutral, opposite  
- 2 voices × 3 text_types × 12 emotions × 6 scales = 432 samples
"""

import time
import requests
from pathlib import Path
import json

def generate_full_compliant_samples():
    """Generate samples exactly as specified in updated plan.md"""
    
    print("=" * 80)
    print("GENERATING FULL PLAN.MD COMPLIANT TTS SAMPLES")
    print("=" * 80)
    
    # Working token
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1NzY1ODMxLCJleHAiOjE3NTU3Njk0MzEsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.jDp9zGN45uZCmNI5UVfW7sdHksNVeDkw0D1KQSH7hS_7ShbmfvMnAx_vMgU5b6fqHTdzN6qA9Ftt-0-d9-2oi-O_oKcBbGvOx6yvr6Fee2HzQMMX3qQVq2xOJUBuTzgH4TgoLpUR4VD-9PIvjP4sjtJymdrD30zbIyB3Zi9woslUhB7dSxn7XO1IhCepPdGPMFOK3DBc8wOVWk_j5ox8FeSJP0jxZf0YQgpMGFP3qd127-sT23I3Zb3wRqJZM0DaNqxzlnrLsaA4Ey6h65C2HhQOi9WFn3KS2HGmaeFdCLCSE1MYmVe1LqJTCulO4vTgUPKxKfCcsYqOASSy87rKFg"
    
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
    
    # 6 emotion_labels
    emotion_labels = {
        "angry": {
            "match": "I can't believe you broke your promise again after everything we discussed!",
            "neutral": "The meeting is scheduled for three o'clock in the conference room.",
            "opposite": "Your thoughtfulness and kindness truly made my day so much better."
        },
        "sad": {
            "match": "I really miss the old days when everyone was still here together.",
            "neutral": "The report needs to be submitted by Friday afternoon without fail.",
            "opposite": "This is absolutely the best news I've heard all year long!"
        },
        "happy": {
            "match": "I'm so thrilled about the wonderful surprise party you organized for me!",
            "neutral": "Please remember to turn off the lights when you leave the office.",
            "opposite": "Everything seems to be going wrong and nothing works out anymore."
        },
        "whisper": {
            "match": "Don't make any noise, everyone is sleeping in the next room.",
            "neutral": "The quarterly financial report shows steady growth in all departments.",
            "opposite": "Everyone needs to hear this important announcement right now!"
        },
        "toneup": {
            "match": "Did you really win the grand prize in the competition?",
            "neutral": "The train arrives at platform seven every hour on weekdays.",
            "opposite": "Everything is perfectly calm and there's nothing to worry about here."
        },
        "tonedown": {
            "match": "Let me explain this matter in a very serious and professional manner.",
            "neutral": "The document contains information about the new policy changes.",
            "opposite": "This is so incredibly exciting and I can barely contain myself!"
        }
    }
    
    # 6 emotion_vector_ids
    emotion_vectors = {
        "excited": {
            "id": "68a6b0ca2edfc11a25045538",
            "match": "We're going on the adventure of a lifetime starting tomorrow morning!",
            "neutral": "The temperature today is expected to reach seventy-two degrees.",
            "opposite": "I'm too exhausted and drained to do anything at all today."
        },
        "furious": {
            "id": "68a6b0d2b436060efdc6bc80",
            "match": "This is absolutely unacceptable and I demand an explanation immediately!",
            "neutral": "The library closes at eight o'clock on weekday evenings.",
            "opposite": "I completely understand your position and I'm not upset at all."
        },
        "terrified": {
            "id": "68a6b0d9b436060efdc6bc82",
            "match": "Something is moving in the shadows and I don't know what it is!",
            "neutral": "The coffee machine is located on the third floor break room.",
            "opposite": "I feel completely safe and protected in this wonderful place."
        },
        "fear": {
            "id": "68a6b0f7b436060efdc6bc83",
            "match": "I'm really scared about what might happen if this goes wrong.",
            "neutral": "The new software update will be installed next Tuesday morning.",
            "opposite": "I have complete confidence that everything will work out perfectly."
        },
        "surprise": {
            "id": "68a6b10255e3b2836e609969",
            "match": "Oh my goodness, I never expected to see you here today!",
            "neutral": "The parking lot is located behind the main building entrance.",
            "opposite": "This is exactly what I predicted would happen all along."
        },
        "excitement": {
            "id": "68a6b1062edfc11a2504553b",
            "match": "I can hardly wait to share this amazing news with everyone!",
            "neutral": "Please fill out the form and return it to the front desk.",
            "opposite": "This is rather boring and I'm not interested in it at all."
        }
    }
    
    # 6 emotion scales
    scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    
    # Generate all samples following plan.md structure
    all_samples = []
    
    print("\n=== SAMPLE STRUCTURE ===")
    print("Format: {voice_id}_{text_type}_{emotion_type}_{emotion_value}_{scale}.wav")
    print("Total: 2 voices × 3 text_types × 12 emotions × 6 scales = 432 samples")
    print()
    
    # Emotional samples with emotion_label: 2 voices × 3 text_types × 6 emotions × 6 scales = 216 samples  
    print("emotion_label samples (216):")
    for voice_id, actor_id in voices.items():
        for emotion_name, emotion_texts in emotion_labels.items():
            for text_type, text_content in emotion_texts.items():
                for scale in scales:
                    filename = f"{voice_id}_{text_type}_emo_{emotion_name}_scale_{scale}.wav"
                    print(f"  {filename}")
                    all_samples.append({
                        "filename": filename,
                        "text": text_content,
                        "actor_id": actor_id,
                        "voice_id": voice_id,
                        "text_type": text_type,
                        "emotion_label": emotion_name,
                        "emotion_vector_id": None,
                        "emotion_scale": scale,
                        "category": "emotion_label"
                    })
    
    # Emotional samples with emotion_vector_id: 2 voices × 3 text_types × 6 vectors × 6 scales = 216 samples
    print(f"\nemotion_vector_id samples (216):")
    for voice_id, actor_id in voices.items():
        for vector_name, vector_data in emotion_vectors.items():
            for text_type in ["match", "neutral", "opposite"]:
                text_content = vector_data[text_type]
                for scale in scales:
                    filename = f"{voice_id}_{text_type}_vec_{vector_name}_scale_{scale}.wav"
                    print(f"  {filename}")
                    all_samples.append({
                        "filename": filename,
                        "text": text_content,
                        "actor_id": actor_id,
                        "voice_id": voice_id,
                        "text_type": text_type,
                        "emotion_label": None,
                        "emotion_vector_id": vector_data["id"],
                        "emotion_scale": scale,
                        "category": "emotion_vector_id"
                    })
    
    total_samples = len(all_samples)
    emotion_label_count = sum(1 for s in all_samples if s['category'] == 'emotion_label')
    emotion_vector_count = sum(1 for s in all_samples if s['category'] == 'emotion_vector_id')
    
    print(f"\n=== GENERATION PLAN ===")
    print(f"Total samples: {total_samples}")
    print(f"emotion_label samples: {emotion_label_count} (2 voices × 3 text_types × 6 emotions × 6 scales)")
    print(f"emotion_vector_id samples: {emotion_vector_count} (2 voices × 3 text_types × 6 vectors × 6 scales)")
    print(f"Estimated time: {total_samples * 6 / 60:.1f} minutes")
    print(f"\nVariables included in naming:")
    print(f"✅ Voice: {list(voices.keys())}")
    print(f"✅ Text_type: ['match', 'neutral', 'opposite']")  
    print(f"✅ Emotions: {list(emotion_labels.keys())} + {list(emotion_vectors.keys())}")
    print(f"✅ Scale: {scales}")
    
    # Generate samples
    success_count = 0
    failed_samples = []
    
    for i, sample in enumerate(all_samples, 1):
        print(f"\n[{i:3d}/{total_samples}] {sample['filename']}")
        print(f"   Voice: {sample['voice_id']} | Text_type: {sample['text_type']} | Category: {sample['category']}")
        print(f"   Emotion: {sample['emotion_label'] or 'vector_id'} | Scale: {sample['emotion_scale']}")
        
        if process_sample(sample, headers, host, output_dir):
            success_count += 1
            print(f"   ✅ SUCCESS ({success_count}/{i})")
        else:
            print(f"   ❌ FAILED")
            failed_samples.append(sample['filename'])
        
        # Progress update every 25 samples
        if i % 25 == 0:
            progress_pct = i/total_samples*100
            success_rate = success_count/i*100
            print(f"\n   📊 Progress: {i}/{total_samples} ({progress_pct:.1f}%) - Success rate: {success_rate:.1f}%")
        
        # Rate limiting
        if i < total_samples:
            time.sleep(3)
    
    # Final results
    print(f"\n{'='*80}")
    print("FULL PLAN.MD COMPLIANT GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Total samples: {total_samples}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(failed_samples)}")
    print(f"Success rate: {(success_count/total_samples)*100:.1f}%")
    
    if failed_samples:
        print(f"\nFailed samples ({len(failed_samples)}):")
        for filename in failed_samples[:10]:  # Show first 10
            print(f"  {filename}")
        if len(failed_samples) > 10:
            print(f"  ... and {len(failed_samples) - 10} more")
    
    # Generate statistics
    wav_files = list(output_dir.glob("*.wav"))
    print(f"\nGenerated files: {len(wav_files)}")
    
    # Group by category
    emo_label_files = [f for f in wav_files if "_emo_" in f.name]
    emo_vector_files = [f for f in wav_files if "_vec_" in f.name]
    
    print(f"\nemotion_label files ({len(emo_label_files)}) - showing first 10:")
    for file in sorted(emo_label_files)[:10]:
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")
    if len(emo_label_files) > 10:
        print(f"  ... and {len(emo_label_files) - 10} more emotion_label samples")
        
    print(f"\nemotion_vector_id files ({len(emo_vector_files)}) - showing first 10:")
    for file in sorted(emo_vector_files)[:10]:
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")
    if len(emo_vector_files) > 10:
        print(f"  ... and {len(emo_vector_files) - 10} more emotion_vector_id samples")
    
    # Save metadata
    metadata = {
        "generation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "plan_compliance": True,
        "total_samples": total_samples,
        "emotion_label_samples": emotion_label_count,
        "emotion_vector_samples": emotion_vector_count,
        "successful_samples": success_count,
        "failed_samples": failed_samples,
        "configuration": {
            "voices": voices,
            "emotion_labels": {k: "3 text types per emotion" for k in emotion_labels.keys()},
            "emotion_vectors": {k: v["id"] for k, v in emotion_vectors.items()},
            "scales": scales,
            "text_types": ["match", "neutral", "opposite"]
        },
        "naming_structure": "{voice_id}_{text_type}_{emotion_type}_{emotion_value}_{scale}.wav"
    }
    
    metadata_file = output_dir.parent / 'full_compliant_metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n📄 Metadata saved: {metadata_file}")
    
    if success_count > 0:
        print(f"\n🎉 Generated {success_count} full plan.md compliant samples!")
        if success_count == total_samples:
            print("\n🏆 PERFECT - ALL 432 SAMPLES GENERATED WITH FULL PLAN.MD COMPLIANCE!")
        return True
    else:
        print(f"\n😞 No samples generated")
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
        "emotion_vector_id": sample["emotion_vector_id"],
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
    generate_full_compliant_samples()