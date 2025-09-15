#!/usr/bin/env python3
"""
Quick test to see actual API response structure and verify quality options
"""

import requests
import json
import time

API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODg2ODg2LCJleHAiOjE3NTY4OTA0ODYsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.lUDeAPiF5in-c-jHgT2bnCRqu4FIw3NI3cuH5vUo_9FU5bUQnHov2sL6WcqqzHix9TOS76odlyW7ecE5YAjgODiMcZUe1YLVN1m6vwSR_gVj6P1P_svTlW1F6PvOWIqGTeFfugA6vvcggnO2XeEKW3TegY8AFl2Tw2ctFxTSgV91_3YzYSGZJShozB4FpZmdg1-Y5UHQ6PJVmljWveVSAjkpafCKjKvspjxsocJlrBN26ICfh6iiQ_cpAuZqxiu1VI0OIwzFYLBLbMJkHvNOx5ScD86xgq2RnCnbzti5NgMjvoQT6S7dM2B6p1cvvELl1OFfe7AAonI-IiAK82Ho2w"
BASE_URL = "https://dev.icepeak.ai/api"

def test_single_api_call():
    """Test a single API call and show the full response"""
    print("🔍 Testing Single API Call")
    print("="*50)
    
    test_request = {
        "text": "Quick quality test.",
        "actor_id": "68ad0ca7e68cb082a1c46fd6",
        "style_label": "normal-1",
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "bp_c_l": True,
        "adjust_lastword": 0,
        "style_label_version": "v1"
    }
    
    headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}
    
    # Send request
    print("1. Sending request...")
    response = requests.post(f"{BASE_URL}/speak/batch/post", json=[test_request], headers=headers)
    response.raise_for_status()
    
    result = response.json()
    speak_urls = result.get("result", {}).get("speak_urls", [])
    print(f"✅ Got {len(speak_urls)} speak URLs")
    
    # Poll for completion
    print("2. Polling for result...")
    poll_url = f"{BASE_URL}/speak/batch/get"
    
    for attempt in range(20):  # Increased attempts
        poll_response = requests.post(poll_url, json=speak_urls, headers=headers)
        poll_response.raise_for_status()
        
        results = poll_response.json().get("result", [])
        if results and results[0].get("status") == "done":
            print("✅ Generation complete!")
            
            result = results[0]
            print("\n3. 🔍 FULL RESPONSE STRUCTURE:")
            print("="*50)
            print(json.dumps(result, indent=2))
            
            # Check audio section specifically
            audio = result.get("audio", {})
            print(f"\n4. 📊 AUDIO SECTION ANALYSIS:")
            print("="*50)
            print(f"Standard URL: {audio.get('url', 'NOT FOUND')}")
            print(f"Extension: {audio.get('extension', 'NOT FOUND')}")
            
            if 'high' in audio:
                print(f"HIGH Quality URL: {audio['high'].get('url', 'NOT FOUND')}")
                print(f"HIGH Extension: {audio['high'].get('extension', 'NOT FOUND')}")
            else:
                print("❌ NO 'high' quality option found!")
                
            if 'hd1' in audio:
                print(f"HD1 Quality URL: {audio['hd1'].get('url', 'NOT FOUND')}")
            else:
                print("❌ NO 'hd1' quality option found!")
                
            return result
            
        print(f"  Attempt {attempt + 1}/20...")
        time.sleep(2)
    
    print("❌ Timed out")
    return None

if __name__ == "__main__":
    test_single_api_call()