#!/usr/bin/env python3
"""
Investigation script to understand audio quality options in TTS API responses
"""

import requests
import json
import time

# Fresh API token (fixed typo in exp field)
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODg2ODg2LCJleHAiOjE3NTY4OTA0ODYsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.lUDeAPiF5in-c-jHgT2bnCRqu4FIw3NI3cuH5vUo_9FU5bUQnHov2sL6WcqqzHix9TOS76odlyW7ecE5YAjgODiMcZUe1YLVN1m6vwSR_gVj6P1P_svTlW1F6PvOWIqGTeFfugA6vvcggnO2XeEKW3TegY8AFl2Tw2ctFxTSgV91_3YzYSGZJShozB4FpZmdg1-Y5UHQ6PJVmljWveVSAjkpafCKjKvspjxsocJlrBN26ICfh6iiQ_cpAuZqxiu1VI0OIwzFYLBLbMJkHvNOx5ScD86xgq2RnCnbzti5NgMjvoQT6S7dM2B6p1cvvELl1OFfe7AAonI-IiAK82Ho2w"

BASE_URL = "https://dev.icepeak.ai/api"
HEADERS = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

def investigate_audio_structure():
    """Generate one sample and investigate the full audio response structure"""
    print("🔍 Investigating TTS API Audio Response Structure")
    print("=" * 60)
    
    # Create a simple test request
    test_request = {
        "text": "This is a test to investigate audio quality options.",
        "actor_id": "68ad0ca7e68cb082a1c46fd6",  # v001
        "emotion_label": "happy",
        "emotion_scale": 1.0,
        "style_label": "normal-1",
        "lang": "auto",
        "mode": "one-vocoder",
        "retake": True,
        "bp_c_l": True,
        "adjust_lastword": 0,
        "style_label_version": "v1"
    }
    
    print("1. Sending batch request...")
    response = requests.post(f"{BASE_URL}/speak/batch/post", headers=HEADERS, json=[test_request])
    
    if response.status_code != 200:
        print(f"❌ Failed to send request: {response.status_code}")
        print(response.text)
        return
        
    result = response.json()
    speak_urls = result.get("result", {}).get("speak_urls", [])
    print(f"✅ Received {len(speak_urls)} speak URLs")
    
    if not speak_urls:
        print("❌ No speak URLs received")
        return
    
    print("\n2. Polling for completion...")
    for attempt in range(10):
        poll_response = requests.post(f"{BASE_URL}/speak/batch/get", headers=HEADERS, json=speak_urls)
        
        if poll_response.status_code != 200:
            print(f"❌ Poll failed: {poll_response.status_code}")
            continue
            
        results = poll_response.json().get("result", [])
        
        if results and results[0].get("status") == "done":
            print("✅ Generation completed!")
            
            # Deep dive into the response structure
            result = results[0]
            print("\n3. 🔍 DETAILED AUDIO STRUCTURE ANALYSIS:")
            print("=" * 50)
            
            print(f"Status: {result.get('status')}")
            print(f"Audio URL base: {result.get('audio', {}).get('url', 'N/A')}")
            
            # Check for different quality options
            audio_section = result.get("audio", {})
            print(f"\n📊 Available Audio Qualities:")
            print(f"  - Standard: {audio_section.get('url', 'N/A')}")
            print(f"  - Extension: {audio_section.get('extension', 'N/A')}")
            
            if 'high' in audio_section:
                print(f"  - High Quality: {audio_section['high'].get('url', 'N/A')}")
                print(f"  - High Extension: {audio_section['high'].get('extension', 'N/A')}")
                
            if 'hd1' in audio_section:
                print(f"  - HD1 Quality: {audio_section['hd1'].get('url', 'N/A')}")
                print(f"  - HD1 Extension: {audio_section['hd1'].get('extension', 'N/A')}")
                
            if 'low' in audio_section:
                print(f"  - Low Quality: {audio_section['low'].get('url', 'N/A')}")
                print(f"  - Low Extension: {audio_section['low'].get('extension', 'N/A')}")
            
            # Test CloudFront URLs for each quality
            print(f"\n🔗 Testing CloudFront URLs:")
            
            # Test standard quality
            standard_url = audio_section.get('url')
            if standard_url:
                print(f"\n  📡 Standard Quality CloudFront:")
                cloudfront_response = requests.get(f"{standard_url}/cloudfront", headers=HEADERS)
                if cloudfront_response.status_code == 200:
                    cloudfront_data = cloudfront_response.json()
                    print(f"    ✅ CloudFront URL: {cloudfront_data.get('result', 'N/A')}")
                else:
                    print(f"    ❌ CloudFront failed: {cloudfront_response.status_code}")
            
            # Test high quality if available
            high_url = audio_section.get('high', {}).get('url')
            if high_url:
                print(f"\n  📡 High Quality CloudFront:")
                cloudfront_response = requests.get(f"{high_url}/cloudfront", headers=HEADERS)
                if cloudfront_response.status_code == 200:
                    cloudfront_data = cloudfront_response.json()
                    print(f"    ✅ High Quality CloudFront URL: {cloudfront_data.get('result', 'N/A')}")
                else:
                    print(f"    ❌ High Quality CloudFront failed: {cloudfront_response.status_code}")
            
            # Print full JSON for reference
            print(f"\n📄 FULL RESPONSE JSON:")
            print("=" * 30)
            print(json.dumps(result, indent=2))
            
            return result
        
        print(f"  Polling attempt {attempt + 1}/10...")
        time.sleep(1)
    
    print("❌ Timed out waiting for completion")
    return None

if __name__ == "__main__":
    investigate_audio_structure()