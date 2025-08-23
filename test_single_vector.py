#!/usr/bin/env python3
"""Test single emotion_vector generation using notebook blueprint"""

import time
import requests

# Fresh token
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1ODIxMzIzLCJleHAiOjE3NTU4MjQ5MjMsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.P751wYbfr_LPdS3nw8CHO2-o0Bs2Zds59Gtu4G4tIVU7jvPlyJgyvZJCc27hEWVm2HyTv9-Lh-niUdTnohyR0ELmoazs8VXJWkwmeRDb3R370SgA2OvNWe8XN_S7AGcRDVkOmTPY6klBfsdsX13XS49fr7MXGsAA-W-yjjxrsFHhrHTTauYzCAGumNmfoYwWq-ymzIojtkKZ5hoOEc0ADRfI4eUvUIZtQmrXviSNp_4xTMEkBMDqIw7XBA7t25gLQEnxzQE6bAnPOult5XL7mumHYwbRaC2MEewxNHorxjNrSnwmbrRSdL2PzIvegn30mryDuApjtF2BirSFolzswg"

HEADERS = {"Authorization": f"Bearer {TOKEN}"}
host = "https://dev.icepeak.ai"  # This is the correct host that worked before

# Test data with emotion_vector_id
speak_data = [
    {
        "text": "We're going on the adventure of a lifetime!",
        "actor_id": "688b02990486383d463c9d1a",  # ssfm_v30_emotion_test - correct for this token
        "tempo": 1,
        "pitch": 0,
        "style_label": "normal-1",  # MUST be normal-1 for emotion_vector
        "style_label_version": "v1",
        "emotion_vector_id": "68a6b0ca2edfc11a25045538",  # Excited - from tts-test-sentences.md
        "emotion_scale": 1.5,
        "bp_c_l": True,  # Important parameter from working example
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "adjust_lastword": 0,
    }
]

print("Testing TTS generation with emotion_vector_id...")
print(f"emotion_vector_id: {speak_data[0]['emotion_vector_id']}")
print(f"emotion_scale: {speak_data[0]['emotion_scale']}")
print(f"bp_c_l: {speak_data[0]['bp_c_l']}")

# Step 1: Request generation
print("\n1. Requesting generation...")
speak_response = requests.post(
    f"{host}/api/speak/batch/post", headers=HEADERS, json=speak_data
)

print(f"Response status: {speak_response.status_code}")

if speak_response.status_code == 200:
    r = speak_response.json()
    print(f"Response: {r}")
    
    speak_urls = r.get("result", {}).get("speak_urls", [])
    
    if speak_urls:
        print(f"\n2. Got speak URLs: {speak_urls}")
        print("Polling for completion...")
        
        # Poll for completion
        for i in range(20):
            poll_response = requests.post(
                f"{host}/api/speak/batch/get", headers=HEADERS, json=speak_urls
            )
            
            poll_result = poll_response.json()["result"][0]
            print(f"  Attempt {i+1}: {poll_result['status']}")
            
            if poll_result["status"] == "done":
                print("\n3. Generation complete!")
                print(f"Audio URL: {poll_result['audio']['url']}")
                
                # Get cloudfront URL
                audio_response = requests.get(
                    poll_result["audio"]["url"] + "/cloudfront", headers=HEADERS
                )
                audio_response_json = audio_response.json()
                real_audio_url = audio_response_json["result"]
                
                # Download audio
                real_audio_response = requests.get(real_audio_url)
                
                # Save test file
                output_file = "public/voices/test_v001_vec_excited_1.5.wav"
                with open(output_file, "wb") as audio_file:
                    audio_file.write(real_audio_response.content)
                
                print(f"\n✅ Success! Audio saved to: {output_file}")
                print(f"   File size: {len(real_audio_response.content)} bytes")
                break
            
            time.sleep(2)
else:
    print(f"Error: {speak_response.text}")