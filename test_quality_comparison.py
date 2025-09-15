#!/usr/bin/env python3
"""
Compare actual file sizes of different quality URLs
"""

import requests
import os

API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg3MzI5MywidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODg2ODg2LCJleHAiOjE3NTY4OTA0ODYsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.lUDeAPiF5in-c-jHgT2bnCRqu4FIw3NI3cuH5vUo_9FU5bUQnHov2sL6WcqqzHix9TOS76odlyW7ecE5YAjgODiMcZUe1YLVN1m6vwSR_gVj6P1P_svTlW1F6PvOWIqGTeFfugA6vvcggnO2XeEKW3TegY8AFl2Tw2ctFxTSgV91_3YzYSGZJShozB4FpZmdg1-Y5UHQ6PJVmljWveVSAjkpafCKjKvspjxsocJlrBN26ICfh6iiQ_cpAuZqxiu1VI0OIwzFYLBLbMJkHvNOx5ScD86xgq2RnCnbzti5NgMjvoQT6S7dM2B6p1cvvELl1OFfe7AAonI-IiAK82Ho2w"

def get_cloudfront_url(audio_url):
    """Get CloudFront download URL"""
    headers = {"Authorization": API_TOKEN}
    response = requests.get(f"{audio_url}/cloudfront", headers=headers)
    response.raise_for_status()
    return response.json().get("result")

def download_and_compare():
    """Download different quality files and compare sizes"""
    print("🔍 Comparing Quality URLs")
    print("="*50)
    
    # URLs from our test above
    standard_url = "https://create-test.icepeak.ai/files/speak/ZGF0YS9zLzIwMjUvOS8zL2xpZ2h0LXNwZWFrY29yZS13b3JrZXItN2M0OWY2ZDk4ZC03a3NzNS9iYjNhNDljMy00ZDVmLTQwYjUtOTRlYy05YzMyMTdkYTMwMTgtbm9ybWFsLndhdg=="
    high_url = "https://create-test.icepeak.ai/files/speak/ZGF0YS9zLzIwMjUvOS8zL2xpZ2h0LXNwZWFrY29yZS13b3JrZXItN2M0OWY2ZDk4ZC03a3NzNS9iYjNhNDljMy00ZDVmLTQwYjUtOTRlYy05YzMyMTdkYTMwMTgtbm9ybWFsLndhdg=="
    hd1_url = "https://create-test.icepeak.ai/files/speak/ZGF0YS9zLzIwMjUvOS8zL2xpZ2h0LXNwZWFrY29yZS13b3JrZXItN2M0OWY2ZDk4ZC03a3NzNS9iYjNhNDljMy00ZDVmLTQwYjUtOTRlYy05YzMyMTdkYTMwMTgud2F2"
    low_url = "https://create-test.icepeak.ai/files/speak/ZGF0YS9zLzIwMjUvOS8zL2xpZ2h0LXNwZWFrY29yZS13b3JrZXItN2M0OWY2ZDk4ZC03a3NzNS9iYjNhNDljMy00ZDVmLTQwYjUtOTRlYy05YzMyMTdkYTMwMTgtbG93Lndhdg=="
    
    qualities = [
        ("standard", standard_url),
        ("high", high_url), 
        ("hd1", hd1_url),
        ("low", low_url)
    ]
    
    os.makedirs("quality_test", exist_ok=True)
    
    for name, audio_url in qualities:
        try:
            print(f"\n📡 Testing {name.upper()} quality...")
            
            # Get CloudFront URL
            download_url = get_cloudfront_url(audio_url)
            print(f"CloudFront URL: {download_url[:50]}...")
            
            # Download file
            response = requests.get(download_url)
            response.raise_for_status()
            
            filename = f"quality_test/test_{name}.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ {name.upper()}: {file_size:,} bytes")
            
        except Exception as e:
            print(f"❌ {name.upper()} failed: {e}")
    
    print(f"\n📊 QUALITY COMPARISON COMPLETE")
    print("Check quality_test/ directory for files")

if __name__ == "__main__":
    download_and_compare()