#!/usr/bin/env python3
"""
Test the corrected high-quality download function
"""

import requests
import json
import time
import os

API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODg2ODg2LCJleHAiOjE3NTY4OTA0ODYsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.lUDeAPiF5in-c-jHgT2bnCRqu4FIw3NI3cuH5vUo_9FU5bUQnHov2sL6WcqqzHix9TOS76odlyW7ecE5YAjgODiMcZUe1YLVN1m6vwSR_gVj6P1P_svTlW1F6PvOWIqGTeFfugA6vvcggnO2XeEKW3TegY8AFl2Tw2ctFxTSgV91_3YzYSGZJShozB4FpZmdg1-Y5UHQ6PJVmljWveVSAjkpafCKjKvspjxsocJlrBN26ICfh6iiQ_cpAuZqxiu1VI0OIwzFYLBLbMJkHvNOx5ScD86xgq2RnCnbzti5NgMjvoQT6S7dM2B6p1cvvELl1OFfe7AAonI-IiAK82Ho2w"
BASE_URL = "https://dev.icepeak.ai/api"

def get_high_quality_audio_url(result):
    """CORRECTED: Extract highest quality audio URL from TTS result"""
    audio_section = result.get("audio", {})
    
    # CORRECTED Priority: hd1 is TRUE high quality, not 'high'
    if "hd1" in audio_section and audio_section["hd1"].get("url"):
        return audio_section["hd1"]["url"], "hd1" 
    if "high" in audio_section and audio_section["high"].get("url"):
        return audio_section["high"]["url"], "high"
    if audio_section.get("url"):
        return audio_section["url"], "standard"
    if "low" in audio_section and audio_section["low"].get("url"):
        return audio_section["low"]["url"], "low"
        
    return None, None

def get_cloudfront_download_url(audio_url):
    """Get CloudFront optimized download URL"""
    headers = {"Authorization": API_TOKEN}
    response = requests.get(f"{audio_url}/cloudfront", headers=headers)
    response.raise_for_status()
    return response.json().get("result")

def download_high_quality_audio(result, output_path):
    """Download using corrected high-quality method"""
    audio_url, quality_type = get_high_quality_audio_url(result)
    
    if not audio_url:
        return False, "none", 0
    
    try:
        download_url = get_cloudfront_download_url(audio_url)
        response = requests.get(download_url)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        return True, quality_type, len(response.content)
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False, quality_type, 0

def test_corrected_download():
    """Test the corrected download function"""
    print("🔍 Testing CORRECTED High-Quality Download")
    print("="*50)
    
    # Create TTS request
    test_request = {
        "text": "Testing corrected high-quality download with HD1 priority.",
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
    
    # Generate audio
    response = requests.post(f"{BASE_URL}/speak/batch/post", json=[test_request], headers=headers)
    response.raise_for_status()
    
    speak_urls = response.json().get("result", {}).get("speak_urls", [])
    print(f"✅ Generated speak URLs")
    
    # Poll for completion
    for attempt in range(20):
        poll_response = requests.post(f"{BASE_URL}/speak/batch/get", json=speak_urls, headers=headers)
        poll_response.raise_for_status()
        
        results = poll_response.json().get("result", [])
        if results and results[0].get("status") == "done":
            result = results[0]
            
            # Test our corrected download function
            success, quality_used, file_size = download_high_quality_audio(result, "corrected_test.wav")
            
            print(f"\n📊 CORRECTED DOWNLOAD RESULTS:")
            print(f"✅ Success: {success}")
            print(f"🎵 Quality Used: {quality_used}")
            print(f"📁 File Size: {file_size:,} bytes")
            
            if quality_used == "hd1":
                print(f"✅ CONFIRMED: Now using TRUE high-quality (HD1)!")
            elif quality_used == "high":
                print(f"⚠️  Using 'high' (which equals standard quality)")
            else:
                print(f"❌ Using {quality_used} quality")
                
            return
            
        print(f"  Polling attempt {attempt + 1}/20...")
        time.sleep(1)
    
    print("❌ Timeout")

if __name__ == "__main__":
    test_corrected_download()