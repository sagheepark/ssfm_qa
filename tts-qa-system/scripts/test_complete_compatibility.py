#!/usr/bin/env python3
"""
Test complete compatibility matrix for TTS API
- Two actors: voice_001, voice_002
- All 6 emotions: happy, sad, angry, whisper, tonedown, toneup
- Multiple scales: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0
"""

import requests
import time
import json
from pathlib import Path

def test_complete_compatibility():
    """Test all combinations of actors, emotions, and scales"""
    
    print("=" * 80)
    print("TESTING COMPLETE TTS API COMPATIBILITY")
    print("=" * 80)
    
    # Fresh token provided by user
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTQ3NiwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU1NzY1NDc2LCJleHAiOjE3NTU3NjkwNzYsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.H8oYaEzoA5rYIDbwCi2wQrzqRLobX4GmsuG46gnhb27gjYeDjvnJ4aVVSAk3CYjbQjTIsOIEX7Kyq91QktKz92jdnBNLJ7B39piJDq9OpjQXVPzTttmV1Ai__PwIxl-2thDdRpp9FHdmS3mjeOiWeRoU9QE359GqE6oOVLcXLp9lXjajsPvjr-_nY4JE7pFkK-uYPPVsKmUMCDJIf5eqq8i2YPdzhJuRmnA56BNP_x1EGMh3OWn91k03YxcQBppoEUFOLoupMSgwaUQK8wL4Pi9eawdWxZccwFxkjrW46I8vz1sizFvhBbaSqhEztkvrXacY4IkGQzpqyqieRSCD0Q"
    
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://dev.icepeak.ai"
    
    # Test configurations
    actors = {
        "voice_001": "688b02990486383d463c9d1a",
        "voice_002": "689c693264acbc0a5b9fb0e5"  # Updated accessibility
    }
    
    emotions = ["happy", "sad", "angry", "whisper", "tonedown", "toneup"]
    scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    
    # Test texts for each emotion
    test_texts = {
        "happy": "I'm so thrilled about the wonderful surprise party you organized for me!",
        "sad": "I really miss the old days when everyone was still here together.",
        "angry": "I can't believe you broke your promise again after everything we discussed!",
        "whisper": "Let me tell you a secret in a very quiet voice.",
        "tonedown": "Please speak more softly and calmly about this sensitive topic.", 
        "toneup": "We need to be more enthusiastic and energetic about this project!"
    }
    
    results = {}
    
    # First, test basic actor accessibility
    print("\\n" + "="*50)
    print("STEP 1: TESTING ACTOR ACCESSIBILITY")
    print("="*50)
    
    for voice_name, actor_id in actors.items():
        print(f"\\nTesting {voice_name} ({actor_id})...")
        
        test_request = [{
            "text": "This is a basic connectivity test.",
            "actor_id": actor_id,
            "style_label": "normal-1",
            "style_label_version": "v1",
            "emotion_label": None,
            "emotion_scale": 1.0,
            "tempo": 1,
            "pitch": 0,
            "lang": "auto",
            "mode": "one-vocoder", 
            "retake": True,
            "adjust_lastword": 0
        }]
        
        try:
            response = requests.post(f"{base_url}/api/speak/batch/post", 
                                   headers=headers, json=test_request, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ {voice_name} ACCESSIBLE")
                results[voice_name] = {"accessible": True, "emotions": {}}
            else:
                error_msg = response.json().get('message', {}).get('msg', 'unknown error')
                print(f"   ❌ {voice_name} NOT ACCESSIBLE: {error_msg}")
                results[voice_name] = {"accessible": False, "emotions": {}, "error": error_msg}
                
        except Exception as e:
            print(f"   ❌ {voice_name} ERROR: {str(e)}")
            results[voice_name] = {"accessible": False, "emotions": {}, "error": str(e)}
    
    # Test emotions only for accessible actors
    accessible_actors = {k: v for k, v in actors.items() if results.get(k, {}).get("accessible", False)}
    
    if not accessible_actors:
        print("\\n❌ No actors are accessible! Cannot proceed with emotion testing.")
        return False
        
    print(f"\\n✅ Found {len(accessible_actors)} accessible actor(s): {list(accessible_actors.keys())}")
    
    # Step 2: Test emotions
    print("\\n" + "="*50) 
    print("STEP 2: TESTING EMOTIONS")
    print("="*50)
    
    total_tests = len(accessible_actors) * len(emotions) * len(scales)
    test_count = 0
    
    print(f"\\nTesting {len(emotions)} emotions with {len(scales)} scales each")
    print(f"Total emotion tests: {total_tests}")
    print(f"Emotions to test: {emotions}")
    print(f"Scales to test: {scales}")
    
    for voice_name, actor_id in accessible_actors.items():
        print(f"\\n--- TESTING {voice_name.upper()} ---")
        results[voice_name]["emotions"] = {}
        
        for emotion in emotions:
            print(f"\\n  Testing emotion: {emotion}")
            results[voice_name]["emotions"][emotion] = {}
            
            emotion_text = test_texts.get(emotion, "This is a test sentence.")
            
            for scale in scales:
                test_count += 1
                print(f"    [{test_count:2d}/{total_tests}] Scale {scale}...", end=" ")
                
                test_request = [{
                    "text": emotion_text,
                    "actor_id": actor_id,
                    "style_label": "normal-1",
                    "style_label_version": "v1", 
                    "emotion_label": emotion,
                    "emotion_scale": scale,
                    "tempo": 1,
                    "pitch": 0,
                    "lang": "auto",
                    "mode": "one-vocoder",
                    "retake": True,
                    "adjust_lastword": 0
                }]
                
                try:
                    # Test request phase
                    response = requests.post(f"{base_url}/api/speak/batch/post",
                                           headers=headers, json=test_request, timeout=10)
                    
                    if response.status_code == 200:
                        r = response.json()
                        speak_urls = r.get("result", {}).get("speak_urls")
                        
                        if speak_urls:
                            # Test generation phase (quick check)
                            for attempt in range(5):  # Quick test, don't wait long
                                poll_response = requests.post(f"{base_url}/api/speak/batch/get",
                                                            headers=headers, json=speak_urls, timeout=10)
                                
                                if poll_response.status_code == 200:
                                    poll_result = poll_response.json()["result"][0]
                                    status = poll_result["status"]
                                    
                                    if status == "done":
                                        print("✅ SUCCESS")
                                        results[voice_name]["emotions"][emotion][scale] = "success"
                                        break
                                    elif status in ["failed", "error"]:
                                        print("❌ GENERATION FAILED")
                                        results[voice_name]["emotions"][emotion][scale] = "generation_failed"
                                        break
                                else:
                                    print("❌ POLL FAILED")
                                    results[voice_name]["emotions"][emotion][scale] = "poll_failed"
                                    break
                                    
                                time.sleep(0.5)
                            else:
                                print("⏳ TIMEOUT (still processing)")
                                results[voice_name]["emotions"][emotion][scale] = "timeout"
                        else:
                            print("❌ NO SPEAK URLS")
                            results[voice_name]["emotions"][emotion][scale] = "no_speak_urls"
                    else:
                        error_msg = response.json().get('message', {}).get('msg', 'unknown')
                        print(f"❌ REQUEST FAILED: {error_msg}")
                        results[voice_name]["emotions"][emotion][scale] = f"request_failed: {error_msg}"
                        
                except Exception as e:
                    print(f"❌ ERROR: {str(e)}")
                    results[voice_name]["emotions"][emotion][scale] = f"error: {str(e)}"
                
                # Rate limiting
                if test_count < total_tests:
                    time.sleep(1)
    
    # Generate comprehensive report
    print("\\n" + "="*80)
    print("COMPREHENSIVE COMPATIBILITY REPORT")
    print("="*80)
    
    # Actor accessibility summary
    print("\\nACTOR ACCESSIBILITY:")
    for voice_name, voice_data in results.items():
        accessible = voice_data.get("accessible", False)
        status = "✅ ACCESSIBLE" if accessible else f"❌ NOT ACCESSIBLE ({voice_data.get('error', 'unknown')})"
        print(f"  {voice_name}: {status}")
    
    # Emotion compatibility matrix
    for voice_name, voice_data in results.items():
        if not voice_data.get("accessible", False):
            continue
            
        print(f"\\n{voice_name.upper()} EMOTION COMPATIBILITY MATRIX:")
        print(f"{'Emotion':<12} " + " ".join([f"Scale {s:3}" for s in scales]))
        print("-" * (12 + len(scales) * 10))
        
        for emotion in emotions:
            emotion_data = voice_data["emotions"].get(emotion, {})
            row = f"{emotion:<12} "
            
            for scale in scales:
                result = emotion_data.get(scale, "not_tested")
                if result == "success":
                    symbol = "✅    "
                elif "failed" in result:
                    symbol = "❌    " 
                elif result == "timeout":
                    symbol = "⏳    "
                else:
                    symbol = "?     "
                row += symbol
            print(row)
    
    # Working combinations summary
    print("\\nWORKING COMBINATIONS SUMMARY:")
    working_combinations = []
    
    for voice_name, voice_data in results.items():
        if not voice_data.get("accessible", False):
            continue
            
        for emotion, emotion_data in voice_data["emotions"].items():
            working_scales = [scale for scale, result in emotion_data.items() if result == "success"]
            if working_scales:
                working_combinations.append({
                    "voice": voice_name,
                    "emotion": emotion,
                    "scales": working_scales
                })
                print(f"  ✅ {voice_name} + {emotion}: scales {working_scales}")
    
    if not working_combinations:
        print("  ❌ No working emotion combinations found!")
    
    # Save detailed results
    output_dir = Path(__file__).parent.parent / 'data'
    output_dir.mkdir(parents=True, exist_ok=True)
    results_file = output_dir / 'compatibility_test_results.json'
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\\n📄 Detailed results saved to: {results_file}")
    
    # Return summary
    accessible_count = sum(1 for v in results.values() if v.get("accessible", False))
    working_emotion_count = len(working_combinations)
    
    print(f"\\n🎯 FINAL SUMMARY:")
    print(f"   Accessible actors: {accessible_count}/2")
    print(f"   Working emotion combinations: {working_emotion_count}")
    
    return accessible_count > 0 and working_emotion_count > 0

if __name__ == "__main__":
    test_complete_compatibility()