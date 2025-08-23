#!/usr/bin/env python3
"""Test with EXACT payload from working example"""

import requests
import json

TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjpmYWxzZSwiaXNfaXBfdmVyaWZpY2F0aW9uX25lZWRlZCI6dHJ1ZSwiZ3JvdXBfYWRtaW5faWQiOiI2NjdjY2U2NGIyNTI0ZTJmYzQ3ZWI2ZTciLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1NTc2NTgzMSwidXNlcl9pZCI6IjUxTmZudERBVDdiQXlRekZyYUpQd08wYjloRTIiLCJzdWIiOiI1MU5mbnREQVQ3YkF5UXpGcmFKUHdPMGI5aEUyIiwiaWF0IjoxNzU1ODIxMzIzLCJleHAiOjE3NTU4MjQ5MjMsImVtYWlsIjoic2FuZ2hlZSszQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrM0BuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.P751wYbfr_LPdS3nw8CHO2-o0Bs2Zds59Gtu4G4tIVU7jvPlyJgyvZJCc27hEWVm2HyTv9-Lh-niUdTnohyR0ELmoazs8VXJWkwmeRDb3R370SgA2OvNWe8XN_S7AGcRDVkOmTPY6klBfsdsX13XS49fr7MXGsAA-W-yjjxrsFHhrHTTauYzCAGumNmfoYwWq-ymzIojtkKZ5hoOEc0ADRfI4eUvUIZtQmrXviSNp_4xTMEkBMDqIw7XBA7t25gLQEnxzQE6bAnPOult5XL7mumHYwbRaC2MEewxNHorxjNrSnwmbrRSdL2PzIvegn30mryDuApjtF2BirSFolzswg"

HEADERS = {"Authorization": f"Bearer {TOKEN}"}
host = "https://dev.icepeak.ai"

print("Testing with EXACT working payload structure...")
print("=" * 60)

# Test 1: Your working example (should work)
print("\n1. Testing working emotion_vector_id: 68a7b5c5b4a6c41c56a161eb")
payload_working = [{
    "text": "안녕하세요",
    "actor_id": "688b02990486383d463c9d1a",
    "tempo": 1,
    "pitch": 0,
    "style_label": "normal-1",
    "style_label_version": "v1",
    "emotion_scale": 1,
    "emotion_vector_id": "68a7b5c5b4a6c41c56a161eb",
    "lang": "auto",
    "mode": "one-vocoder",
    "bp_c_l": True,
    "retake": True,
    "adjust_lastword": 0
}]

response = requests.post(f"{host}/api/speak/batch/post", headers=HEADERS, json=payload_working)
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    print(f"   Response: {response.text[:200]}")
else:
    print(f"   ✅ SUCCESS")

# Test 2: Same exact structure but with Excited emotion_vector_id
print("\n2. Testing Excited emotion_vector_id: 68a6b0ca2edfc11a25045538")
payload_excited = [{
    "text": "안녕하세요",
    "actor_id": "688b02990486383d463c9d1a",
    "tempo": 1,
    "pitch": 0,
    "style_label": "normal-1",
    "style_label_version": "v1",
    "emotion_scale": 1,
    "emotion_vector_id": "68a6b0ca2edfc11a25045538",  # Only difference
    "lang": "auto",
    "mode": "one-vocoder",
    "bp_c_l": True,
    "retake": True,
    "adjust_lastword": 0
}]

response = requests.post(f"{host}/api/speak/batch/post", headers=HEADERS, json=payload_excited)
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    print(f"   Response: {response.text[:200]}")
else:
    print(f"   ✅ SUCCESS")

# Let's also check the exact order of fields matters
print("\n3. Testing with EXACT field order from your example")
payload_exact_order = []
payload_exact_order.append({})
payload_exact_order[0]["text"] = "안녕하세요"
payload_exact_order[0]["actor_id"] = "688b02990486383d463c9d1a"
payload_exact_order[0]["tempo"] = 1
payload_exact_order[0]["pitch"] = 0
payload_exact_order[0]["style_label"] = "normal-1"
payload_exact_order[0]["style_label_version"] = "v1"
payload_exact_order[0]["emotion_scale"] = 1
payload_exact_order[0]["emotion_vector_id"] = "68a6b0ca2edfc11a25045538"
payload_exact_order[0]["lang"] = "auto"
payload_exact_order[0]["mode"] = "one-vocoder"
payload_exact_order[0]["bp_c_l"] = True
payload_exact_order[0]["retake"] = True
payload_exact_order[0]["adjust_lastword"] = 0

response = requests.post(f"{host}/api/speak/batch/post", headers=HEADERS, json=payload_exact_order)
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    print(f"   Response: {response.text[:200]}")
else:
    print(f"   ✅ SUCCESS")

print("\n" + "=" * 60)
print("Payload comparison:")
print("Working payload:", json.dumps(payload_working[0], indent=2))
print("\nExcited payload:", json.dumps(payload_excited[0], indent=2))
print("\nOnly difference is emotion_vector_id value!")