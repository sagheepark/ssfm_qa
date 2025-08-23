#!/usr/bin/env python3
"""Test all emotion_vector_ids from tts-test-sentences.md"""

import requests
import time

TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1ODIxMzIzLCJleHAiOjE3NTU4MjQ5MjMsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.P751wYbfr_LPdS3nw8CHO2-o0Bs2Zds59Gtu4G4tIVU7jvPlyJgyvZJCc27hEWVm2HyTv9-Lh-niUdTnohyR0ELmoazs8VXJWkwmeRDb3R370SgA2OvNWe8XN_S7AGcRDVkOmTPY6klBfsdsX13XS49fr7MXGsAA-W-yjjxrsFHhrHTTauYzCAGumNmfoYwWq-ymzIojtkKZ5hoOEc0ADRfI4eUvUIZtQmrXviSNp_4xTMEkBMDqIw7XBA7t25gLQEnxzQE6bAnPOult5XL7mumHYwbRaC2MEewxNHorxjNrSnwmbrRSdL2PzIvegn30mryDuApjtF2BirSFolzswg"

HEADERS = {"Authorization": f"Bearer {TOKEN}"}
host = "https://dev.icepeak.ai"

# All 6 emotion_vector_ids from tts-test-sentences.md
EMOTION_VECTORS = {
    "Excited": "68a6b0ca2edfc11a25045538",
    "Furious": "68a6b0d2b436060efdc6bc80", 
    "Terrified": "68a6b0d9b436060efdc6bc82",
    "Fear (두려움)": "68a6b0f7b436060efdc6bc83",
    "Surprise (놀람)": "68a6b10255e3b2836e609969",
    "Excitement (흥분)": "68a6b1062edfc11a2504553b"
}

# Also test the working one from the example
EMOTION_VECTORS["Working Example"] = "68a7b5c5b4a6c41c56a161eb"

print("Testing all emotion_vector_ids...")
print("=" * 60)

for name, vector_id in EMOTION_VECTORS.items():
    print(f"\nTesting {name}: {vector_id}")
    
    speak_data = [{
        "text": "Testing emotion vector",
        "actor_id": "688b02990486383d463c9d1a",
        "tempo": 1,
        "pitch": 0,
        "style_label": "normal-1",
        "style_label_version": "v1",
        "emotion_vector_id": vector_id,
        "emotion_scale": 1.0,
        "bp_c_l": True,
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "adjust_lastword": 0,
    }]
    
    try:
        response = requests.post(
            f"{host}/api/speak/batch/post",
            headers=HEADERS,
            json=speak_data
        )
        
        if response.status_code == 200:
            print(f"  ✅ SUCCESS - Vector exists and works!")
        elif response.status_code == 404:
            error = response.json()
            if "not-found/emotion_vector" in str(error):
                print(f"  ❌ NOT FOUND - Vector doesn't exist")
            else:
                print(f"  ❌ Error 404: {error}")
        else:
            print(f"  ❌ Error {response.status_code}: {response.text[:100]}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")
    
    time.sleep(0.5)  # Small delay between requests

print("\n" + "=" * 60)
print("Test complete!")