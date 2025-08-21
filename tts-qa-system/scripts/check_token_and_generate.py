#!/usr/bin/env python3
"""
Check token validity and generate samples with two different actors
"""

import requests
import json
import time
from pathlib import Path

def check_token_validity():
    """Check if the current token is still valid"""
    
    print("="*70)
    print("CHECKING TOKEN VALIDITY")
    print("="*70)
    
    # Fresh token provided by user
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2MzM2OSwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU1NzYzMzY5LCJleHAiOjE3NTU3NjY5NjksImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.EScBGAzSA87MnXRAPsnvwq6Ejbpf3xgfZQvmmM9kf32X49WNKyp4LoLjxmmTXmcY0C66AV4cXkyTdlS89IoD5cgrTw3KdkAPFhLbEnkj5iR18qQuELtND3XV5bFVvgbVLrRD18lrQTd-G09CmU23qmBnNEzAQ6CcEVphTe-8JEqPAGRrepMjP3heWV3UgMDpXe3SmYT5dNHAL_mCpUNFLG7-j8zezu8U8QGqGti_v7agCI-q3Y5dZvxTG3-tIT293wlsVZ_diJMS9sCw5e-Y4pwoyzeeXobgxl2TfyuacF0QIk2eN8L7KsPWWInzDzMUj6ms4IWhIIKS4BnGyGdWgA"
    
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://dev.icepeak.ai"
    
    # Simple test request
    test_request = [{
        "text": "Token validity test.",
        "actor_id": "688b02990486383d463c9d1a",
        "style_label": "normal-1",
        "emotion_label": None,
        "emotion_scale": 1.0,
        "tempo": 1,
        "pitch": 0,
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "adjust_lastword": 0,
        "style_label_version": "v1"
    }]
    
    try:
        response = requests.post(f"{base_url}/api/speak/batch/post", 
                               headers=headers, json=test_request, timeout=10)
        
        if response.status_code == 200:
            print("✅ TOKEN IS VALID!")
            return True, token
        elif response.status_code == 401:
            error_msg = response.json().get('message', {}).get('msg', 'unknown')
            print(f"❌ TOKEN INVALID: {error_msg}")
            return False, None
        else:
            print(f"❓ UNEXPECTED RESPONSE: {response.status_code}")
            print(response.text[:200])
            return False, None
            
    except Exception as e:
        print(f"❌ ERROR CHECKING TOKEN: {str(e)}")
        return False, None

def create_samples_with_two_actors():
    """Create samples using both actor IDs"""
    
    # Actor mapping as specified
    actor_mapping = {
        "voice_001": "688b02990486383d463c9d1a",
        "voice_002": "689c693264acbc0a5b9fb0e5"
    }
    
    # Emotion data from tts-test-sentences.md
    emotions_data = {
        "Angry": {
            "match": "I can't believe you broke your promise again after everything we discussed!",
            "neutral": "The meeting is scheduled for three o'clock in the conference room.",
            "opposite": "Your thoughtfulness and kindness truly made my day so much better."
        },
        "Sad": {
            "match": "I really miss the old days when everyone was still here together.",
            "neutral": "The report needs to be submitted by Friday afternoon without fail.",
            "opposite": "This is absolutely the best news I've heard all year long!"
        },
        "Happy": {
            "match": "I'm so thrilled about the wonderful surprise party you organized for me!",
            "neutral": "Please remember to turn off the lights when you leave the office.",
            "opposite": "Everything seems to be going wrong and nothing works out anymore."
        },
        "Whisper": {
            "match": "Don't make any noise, everyone is sleeping in the next room.",
            "neutral": "The quarterly financial report shows steady growth in all departments.",
            "opposite": "Everyone needs to hear this important announcement right now!"
        },
        "Toneup": {
            "match": "Did you really win the grand prize in the competition?",
            "neutral": "The train arrives at platform seven every hour on weekdays.",
            "opposite": "Everything is perfectly calm and there's nothing to worry about here."
        },
        "Tonedown": {
            "match": "Let me explain this matter in a very serious and professional manner.",
            "neutral": "The document contains information about the new policy changes.",
            "opposite": "This is so incredibly exciting and I can barely contain myself!"
        }
    }
    
    emotion_scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    match_types = ["match", "neutral", "opposite"]
    
    samples = []
    
    # Generate samples for both voices
    for voice_id, actor_id in actor_mapping.items():
        
        # Reference sample (no emotion)
        samples.append({
            'text': "This is a reference sample for voice calibration and testing.",
            'actor_id': actor_id,
            'voice_id': voice_id,
            'style_label': "normal-1",
            'emotion_label': None,
            'emotion_scale': 1.0,
            'filename': f'{voice_id}_ref.wav',
            'category': 'reference'
        })
        
        # Emotional samples
        for emotion_name, sentences in emotions_data.items():
            for match_type in match_types:
                text = sentences[match_type]
                
                for scale in emotion_scales:
                    samples.append({
                        'text': text,
                        'actor_id': actor_id,
                        'voice_id': voice_id,
                        'style_label': "normal-1",
                        'emotion_label': emotion_name,
                        'emotion_scale': scale,
                        'filename': f'{voice_id}_{emotion_name.lower()}_{match_type}_scale{scale}.wav',
                        'category': f'{emotion_name}_{match_type}_{scale}'
                    })
    
    return samples

def generate_all_samples(token: str, batch_size: int = 4):
    """Generate all samples with progress tracking"""
    
    print("\n" + "="*70)
    print("GENERATING ALL TTS SAMPLES WITH TWO ACTORS")
    print("="*70)
    
    # Create sample list
    all_samples = create_samples_with_two_actors()
    
    print(f"Total samples to generate: {len(all_samples)}")
    print(f"Batch size: {batch_size}")
    
    # Show distribution
    voice_counts = {}
    emotion_counts = {}
    
    for sample in all_samples:
        voice = sample['voice_id']
        emotion = sample.get('emotion_label') or 'Reference'
        voice_counts[voice] = voice_counts.get(voice, 0) + 1
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    print(f"\nVoice distribution:")
    for voice, count in sorted(voice_counts.items()):
        print(f"  {voice}: {count} samples")
    
    print(f"\nEmotion distribution:")
    for emotion, count in sorted(emotion_counts.items()):
        print(f"  {emotion}: {count} samples")
    
    estimated_time = (len(all_samples) / batch_size) * 12  # ~12 seconds per batch
    print(f"\nEstimated time: {estimated_time/60:.1f} minutes")
    
    # Auto-proceed with generation
    print(f"\nProceeding with generating {len(all_samples)} samples...")
    response = 'y'
    
    # Start generation
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://dev.icepeak.ai"
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear old files
    print(f"\nCleaning old files...")
    old_files = list(output_dir.glob('*.wav'))
    for f in old_files:
        f.unlink()
        print(f"  Removed: {f.name}")
    
    # Process in batches
    total_success = 0
    total_failed = 0
    
    start_time = time.time()
    
    for batch_idx in range(0, len(all_samples), batch_size):
        batch_samples = all_samples[batch_idx:batch_idx + batch_size]
        batch_num = (batch_idx // batch_size) + 1
        
        print(f"\n{'='*50}")
        print(f"BATCH {batch_num}: Samples {batch_idx + 1}-{min(batch_idx + batch_size, len(all_samples))}")
        print(f"{'='*50}")
        
        # Prepare batch request
        batch_requests = []
        for sample in batch_samples:
            request = {
                "text": sample['text'],
                "actor_id": sample['actor_id'],
                "style_label": sample['style_label'],
                "emotion_label": sample['emotion_label'],
                "emotion_scale": sample['emotion_scale'],
                "tempo": 1,
                "pitch": 0,
                "lang": "auto",
                "mode": "one-vocoder",
                "retake": True,
                "adjust_lastword": 0,
                "style_label_version": "v1"
            }
            batch_requests.append(request)
        
        # Show batch info
        for i, sample in enumerate(batch_samples):
            emotion = sample.get('emotion_label') or 'Reference'
            print(f"  {i+1}. {sample['filename']} ({sample['voice_id']})")
            print(f"      Emotion: {emotion}, Scale: {sample['emotion_scale']}")
        
        try:
            # Step 1: Request generation
            print(f"\nStep 1: Requesting generation...")
            response = requests.post(f"{base_url}/api/speak/batch/post", 
                                   headers=headers, json=batch_requests, timeout=30)
            
            if response.status_code != 200:
                print(f"✗ Request failed: {response.status_code}")
                print(response.text[:200])
                total_failed += len(batch_samples)
                continue
            
            speak_urls = response.json()["result"]["speak_urls"]
            print(f"✓ Got {len(speak_urls)} speak URLs")
            
            # Step 2: Poll for completion
            print(f"Step 2: Polling for completion...")
            completed_results = None
            
            for attempt in range(25):  # Max 25 attempts (~12.5 seconds)
                poll_response = requests.post(f"{base_url}/api/speak/batch/get",
                                            headers=headers, json=speak_urls, timeout=30)
                
                if poll_response.status_code == 200:
                    results = poll_response.json()["result"]
                    done_count = sum(1 for r in results if r.get("status") == "done")
                    print(f"  Attempt {attempt + 1}: {done_count}/{len(results)} done")
                    
                    if done_count == len(results):
                        completed_results = results
                        break
                
                time.sleep(0.5)
            
            if not completed_results:
                print("✗ Polling timed out")
                total_failed += len(batch_samples)
                continue
            
            # Step 3 & 4: Download each file
            print(f"Step 3 & 4: Downloading audio files...")
            batch_success = 0
            
            for result, sample in zip(completed_results, batch_samples):
                if result.get("status") != "done":
                    print(f"  ✗ {sample['filename']}: Not completed")
                    continue
                
                try:
                    # Get audio URL (try hd1 first, fallback to url)
                    audio_info = result.get("audio", {})
                    audio_url = audio_info.get("hd1", {}).get("url") or audio_info.get("url")
                    
                    if not audio_url:
                        print(f"  ✗ {sample['filename']}: No audio URL")
                        continue
                    
                    # Get download URL
                    cloudfront_response = requests.get(f"{audio_url}/cloudfront", 
                                                     headers=headers, timeout=30)
                    if cloudfront_response.status_code != 200:
                        print(f"  ✗ {sample['filename']}: CloudFront failed")
                        continue
                    
                    download_url = cloudfront_response.json()["result"]
                    
                    # Download audio
                    audio_response = requests.get(download_url, timeout=30)
                    if audio_response.status_code != 200:
                        print(f"  ✗ {sample['filename']}: Download failed")
                        continue
                    
                    # Save file
                    file_path = output_dir / sample['filename']
                    with open(file_path, 'wb') as f:
                        f.write(audio_response.content)
                    
                    size_kb = file_path.stat().st_size / 1024
                    print(f"  ✓ {sample['filename']}: {size_kb:.1f} KB")
                    batch_success += 1
                    
                except Exception as e:
                    print(f"  ✗ {sample['filename']}: {str(e)}")
            
            total_success += batch_success
            total_failed += len(batch_samples) - batch_success
            
            print(f"\nBatch {batch_num} result: {batch_success}/{len(batch_samples)} successful")
            print(f"Running total: {total_success}/{total_success + total_failed}")
            
        except Exception as e:
            print(f"✗ Batch {batch_num} failed: {str(e)}")
            total_failed += len(batch_samples)
        
        # Pause between batches
        if batch_idx + batch_size < len(all_samples):
            print(f"Pausing 3 seconds before next batch...")
            time.sleep(3)
    
    # Final summary
    elapsed = time.time() - start_time
    
    print("\n" + "="*70)
    print("GENERATION COMPLETE!")
    print("="*70)
    print(f"Total successful: {total_success}/{len(all_samples)}")
    print(f"Total failed: {total_failed}")
    print(f"Success rate: {total_success/len(all_samples)*100:.1f}%")
    print(f"Total time: {elapsed/60:.1f} minutes")
    
    # Check generated files
    generated_files = list(output_dir.glob('*.wav'))
    
    print(f"\nGenerated files: {len(generated_files)}")
    
    if generated_files:
        # Analyze by voice
        voice_files = {}
        for f in generated_files:
            voice = f.name.split('_')[0]
            voice_files[voice] = voice_files.get(voice, 0) + 1
        
        print(f"Files by voice:")
        for voice, count in sorted(voice_files.items()):
            print(f"  {voice}: {count} files")
        
        # Show sample file sizes
        avg_size = sum(f.stat().st_size for f in generated_files) / len(generated_files)
        print(f"Average file size: {avg_size/1024:.1f} KB")
    
    success_rate = total_success / len(all_samples)
    return success_rate > 0.8

def main():
    """Main execution"""
    
    # Check token validity first
    is_valid, token = check_token_validity()
    
    if not is_valid:
        print("\n❌ Cannot proceed - token is invalid or expired")
        print("Please get a fresh token from the API provider")
        return False
    
    print(f"\n✅ Token is valid - proceeding with generation")
    
    # Generate all samples
    success = generate_all_samples(token, batch_size=4)
    
    if success:
        print("\n🎉 SUCCESS: All TTS samples generated successfully!")
        print("✅ Ready for QA evaluation!")
    else:
        print("\n⚠ Some issues occurred during generation")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)