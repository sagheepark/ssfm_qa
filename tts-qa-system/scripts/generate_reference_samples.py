#!/usr/bin/env python3
"""
Generate reference TTS samples with style_label: normal-1 only (no emotions)
One reference for each voice-text combination used in emotional samples
"""

import time
import requests
from pathlib import Path
import json

def generate_reference_samples():
    """Generate reference samples with normal-1 style only"""
    
    print("=" * 80)
    print("GENERATING REFERENCE TTS SAMPLES (normal-1 style only)")
    print("=" * 80)
    
    # Working token
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1NzY5OTQzLCJleHAiOjE3NTU3NzM1NDMsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.C1lCBTJi40QI3-rCcc2XoLK4JBVkJocZVDDWuJoQgN-ejpqxd9IBO_8YZDIc7KSI5gOU-qu_1dgXADwaG1vWJkyv47hOHyKQ7v_ON0imx2CFTH_s7j353X-7MW8g1afHRZSFF9AeOQu_75TrG2HqzSAi-w_S3rJm7RwAEOrhIZiK1LSqdSyx03oBenW3pJri5wyoDrtu4u5xoNrXeFseI0Z89AkuziGg6_-2BkCeYJy6qOK5xskD8l_yTlR2WiOfihgLCjg72slnMyBu6In-5fMUufNigW1if7SYsu83iiF5KYcDXFSBRievB2ixWS8yoTe0daYfitVovlL7oiPUYw"
    
    headers = {"Authorization": f"Bearer {token}"}
    host = "https://dev.icepeak.ai"
    
    # Output directory for reference samples
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Configuration matching our emotional samples
    voices = {
        "v001": "688b02990486383d463c9d1a",  # voice_001
        "v002": "689c693264acbc0a5b9fb0e5"   # voice_002
    }
    
    # Reference texts matching the exact text used in emotional samples
    # Each emotion has different text for match/neutral/opposite combinations
    reference_texts = {
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
    
    # Generate reference samples
    all_samples = []
    
    print("\n=== REFERENCE SAMPLES TO GENERATE ===")
    print("Format: {voice_id}_{text_type}_reference_{emotion}.wav")
    print(f"Total: {len(voices)} voices × 3 text types × {len(reference_texts)} emotions = {len(voices) * 3 * len(reference_texts)} samples")
    print()
    
    for voice_id, actor_id in voices.items():
        for emotion, emotion_texts in reference_texts.items():
            for text_type, text_content in emotion_texts.items():
                filename = f"{voice_id}_{text_type}_reference_{emotion}.wav"
                all_samples.append({
                    "filename": filename,
                    "text": text_content,
                    "actor_id": actor_id,
                    "voice_id": voice_id,
                    "text_type": text_type,
                    "emotion": emotion,
                    "style_label": "normal-1",  # Only using style_label
                    "emotion_label": None,       # No emotion_label
                    "emotion_vector_id": None,   # No emotion_vector_id
                    "emotion_scale": 1.0,        # Fixed scale of 1.0
                    "category": "reference"
                })
    
    total_samples = len(all_samples)
    print(f"\n=== GENERATION PLAN ===")
    print(f"Total reference samples: {total_samples}")
    print(f"Voices: {list(voices.keys())}")
    print(f"Emotions: {len(reference_texts)}")
    print(f"Text types per emotion: 3 (match, neutral, opposite)")
    print(f"Style: normal-1 (no emotions)")
    print(f"Scale: 1.0 (fixed)")
    print(f"Estimated time: {total_samples * 6 / 60:.1f} minutes")
    
    # Show first few samples
    print("\nFirst 5 samples:")
    for sample in all_samples[:5]:
        print(f"  {sample['filename']}")
    print(f"  ... and {total_samples - 5} more")
    
    # Generate samples
    success_count = 0
    failed_samples = []
    
    for i, sample in enumerate(all_samples, 1):
        print(f"\n[{i:2d}/{total_samples}] {sample['filename']}")
        print(f"   Voice: {sample['voice_id']} | Text Type: {sample['text_type']}")
        print(f"   Style: {sample['style_label']} | Scale: {sample['emotion_scale']}")
        
        if process_sample(sample, headers, host, output_dir):
            success_count += 1
            print(f"   ✅ SUCCESS ({success_count}/{i})")
        else:
            print(f"   ❌ FAILED")
            failed_samples.append(sample['filename'])
        
        # Progress update every 10 samples
        if i % 10 == 0:
            progress_pct = i/total_samples*100
            success_rate = success_count/i*100
            print(f"\n   📊 Progress: {i}/{total_samples} ({progress_pct:.1f}%) - Success rate: {success_rate:.1f}%")
        
        # Rate limiting
        if i < total_samples:
            time.sleep(3)
    
    # Final results
    print(f"\n{'='*80}")
    print("REFERENCE GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Total samples: {total_samples}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(failed_samples)}")
    print(f"Success rate: {(success_count/total_samples)*100:.1f}%")
    
    if failed_samples:
        print(f"\nFailed samples ({len(failed_samples)}):")
        for filename in failed_samples[:10]:
            print(f"  {filename}")
        if len(failed_samples) > 10:
            print(f"  ... and {len(failed_samples) - 10} more")
    
    # List generated files
    wav_files = list(output_dir.glob("*_reference.wav"))
    print(f"\nGenerated reference files ({len(wav_files)}):")
    
    # Group by voice
    for voice in voices.keys():
        voice_files = [f for f in wav_files if f.name.startswith(voice)]
        print(f"\n  {voice} ({len(voice_files)} files):")
        for file in sorted(voice_files)[:3]:
            size_kb = file.stat().st_size / 1024
            print(f"    {file.name} ({size_kb:.1f} KB)")
        if len(voice_files) > 3:
            print(f"    ... and {len(voice_files) - 3} more")
    
    # Save metadata
    metadata = {
        "generation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": "reference_samples",
        "total_samples": total_samples,
        "successful_samples": success_count,
        "failed_samples": failed_samples,
        "configuration": {
            "voices": voices,
            "text_types": 3,
            "emotions": list(reference_texts.keys()),
            "style_label": "normal-1",
            "emotion_label": None,
            "emotion_vector_id": None,
            "emotion_scale": 1.0
        },
        "naming_structure": "{voice_id}_{text_type}_reference_{emotion}.wav",
        "purpose": "Baseline reference for similarity comparison"
    }
    
    metadata_file = output_dir.parent / 'reference_metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n📄 Metadata saved: {metadata_file}")
    
    if success_count > 0:
        print(f"\n🎉 Generated {success_count} reference samples!")
        print(f"📁 Files saved in: {output_dir}")
        return True
    else:
        print(f"\n😞 No reference samples generated")
        return False

def process_sample(sample, headers, host, output_dir):
    """Process single reference sample with 4-step TTS workflow"""
    
    speak_data = [{
        "text": sample["text"],
        "actor_id": sample["actor_id"],
        "tempo": 1,
        "pitch": 0,
        "style_label": "normal-1",  # Always normal-1 for reference
        "style_label_version": "v1",
        "emotion_label": None,       # No emotion
        "emotion_scale": 1.0,        # Fixed scale
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
    generate_reference_samples()