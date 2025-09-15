#!/usr/bin/env python3
"""
High-Quality Audio Download Implementation
Following TDD principles from CLAUDE.md
"""

import requests
import os
from pathlib import Path

# Fresh API token
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODg2ODg2LCJleHAiOjE3NTY4OTA0ODYsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.lUDeAPiF5in-c-jHgT2bnCRqu4FIw3NI3cuH5vUo_9FU5bUQnHov2sL6WcqqzHix9TOS76odlyW7ecE5YAjgODiMcZUe1YLVN1m6vwSR_gVj6P1P_svTlW1F6PvOWIqGTeFfugA6vvcggnO2XeEKW3TegY8AFl2Tw2ctFxTSgV91_3YzYSGZJShozB4FpZmdg1-Y5UHQ6PJVmljWveVSAjkpafCKjKvspjxsocJlrBN26ICfh6iiQ_cpAuZqxiu1VI0OIwzFjlrBN26ICfh6iiQ_cpAuZqxiu1VI0OIwzFYLBLbMJkHvNOx5ScD86xgq2RnCnbzti5NgMjvoQT6S7dM2B6p1cvvELl1OFfe7AAonI-IiAK82Ho2w"

def get_high_quality_audio_url(result):
    """
    Extract the highest quality audio URL from TTS API result.
    Prioritizes: high > hd1 > standard > low
    """
    audio_section = result.get("audio", {})
    
    # Priority order: high quality first
    if "high" in audio_section and audio_section["high"].get("url"):
        return audio_section["high"]["url"], "high"
    
    # Fallback to HD1 quality  
    if "hd1" in audio_section and audio_section["hd1"].get("url"):
        return audio_section["hd1"]["url"], "hd1"
    
    # Fallback to standard quality
    if audio_section.get("url"):
        return audio_section["url"], "standard"
    
    # Last resort: low quality
    if "low" in audio_section and audio_section["low"].get("url"):
        return audio_section["low"]["url"], "low"
    
    return None, None

def get_cloudfront_download_url(audio_url):
    """Get optimized CloudFront download URL (backend approach)"""
    cloudfront_url = f"{audio_url}/cloudfront"
    headers = {"Authorization": API_TOKEN}
    
    response = requests.get(cloudfront_url, headers=headers)
    response.raise_for_status()
    
    return response.json().get("result")

def download_high_quality_audio(result, output_path):
    """
    Download highest quality audio using backend-recommended approach.
    Returns: (success: bool, quality_used: str, file_size: int)
    """
    # Step 1: Get best quality audio URL
    audio_url, quality_type = get_high_quality_audio_url(result)
    
    if not audio_url:
        print(f"❌ No audio URL found in result")
        return False, "none", 0
    
    print(f"📡 Using {quality_type} quality audio")
    
    try:
        # Step 2: Get CloudFront optimized URL (backend approach)
        download_url = get_cloudfront_download_url(audio_url)
        
        if not download_url:
            print(f"❌ Failed to get CloudFront URL")
            return False, quality_type, 0
        
        # Step 3: Download the actual audio file
        response = requests.get(download_url)
        response.raise_for_status()
        
        # Step 4: Save to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        file_size = len(response.content)
        print(f"✅ Downloaded {quality_type} quality: {file_size:,} bytes")
        
        return True, quality_type, file_size
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False, quality_type, 0

def compare_audio_qualities():
    """Test function to compare different audio qualities"""
    print("🧪 Testing High-Quality Audio Download")
    print("=" * 50)
    
    # This would typically be called with a real TTS result
    # For now, we'll demonstrate the API structure
    
    mock_result = {
        "audio": {
            "url": "https://example.com/standard.wav",
            "extension": "wav",
            "high": {
                "url": "https://example.com/high.wav", 
                "extension": "wav"
            },
            "hd1": {
                "url": "https://example.com/hd1.wav",
                "extension": "wav" 
            },
            "low": {
                "url": "https://example.com/low.wav",
                "extension": "wav"
            }
        }
    }
    
    # Test quality selection
    audio_url, quality = get_high_quality_audio_url(mock_result)
    print(f"Selected quality: {quality}")
    print(f"Selected URL: {audio_url}")
    
    # Test with missing high quality
    mock_result_no_high = {
        "audio": {
            "url": "https://example.com/standard.wav",
            "extension": "wav"
        }
    }
    
    audio_url, quality = get_high_quality_audio_url(mock_result_no_high)
    print(f"Fallback quality: {quality}")
    print(f"Fallback URL: {audio_url}")

if __name__ == "__main__":
    compare_audio_qualities()