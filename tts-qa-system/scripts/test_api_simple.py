#!/usr/bin/env python3
"""
Simple API test script for TTS endpoint with audio_path workflow
"""

import requests
import json
from pathlib import Path
import sys
from urllib.parse import urljoin

def download_audio_file(audio_path: str, api_key: str) -> bool:
    """Download audio file from the provided path"""
    
    print(f"\nDownloading audio file from: {audio_path}")
    
    # Determine if audio_path is relative or absolute URL
    if audio_path.startswith('http'):
        download_url = audio_path
    else:
        # Assume it's relative to the API base URL
        base_url = "https://dev.icepeak.ai"
        download_url = urljoin(base_url, audio_path.lstrip('/'))
    
    print(f"Download URL: {download_url}")
    
    # Try different auth headers for download
    auth_headers = [
        {"Authorization": f"Bearer {api_key}"},
        {"X-API-Key": api_key},
        {"api-key": api_key},
        {}  # No auth
    ]
    
    for headers in auth_headers:
        try:
            print(f"Trying download with headers: {list(headers.keys())}")
            download_response = requests.get(download_url, headers=headers, timeout=30)
            
            if download_response.status_code == 200:
                content_length = len(download_response.content)
                print(f"✓ Downloaded {content_length} bytes ({content_length/1024:.1f} KB)")
                
                # Save test audio file
                test_output = Path(__file__).parent.parent / 'data' / 'voices' / 'api_test_real.wav'
                test_output.parent.mkdir(parents=True, exist_ok=True)
                
                with open(test_output, 'wb') as f:
                    f.write(download_response.content)
                
                print(f"✓ Audio saved to: {test_output}")
                print(f"✓ Final file size: {test_output.stat().st_size} bytes")
                return True
            else:
                print(f"Download failed: {download_response.status_code}")
                
        except Exception as e:
            print(f"Download error: {str(e)}")
    
    return False

def test_tts_api():
    """Test the TTS API with authentication"""
    
    api_endpoint = "https://dev.icepeak.ai/api/speak/batch/post"
    
    # Get API key
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your API key: ").strip()
    
    if not api_key:
        print("No API key provided.")
        return False
    
    # Test request
    test_request = {
        "text": "Hello, this is a test message for TTS API validation.",
        "actor_id": "voice_001",
        "style_label": "normal-1",
        "emotion_scale": 1.0,
        "tempo": 1,
        "pitch": 0,
        "lang": "en",
        "mode": "one-vocoder",
        "bp_c_l": True,
        "retake": True,
        "adjust_lastword": 0,
        "style_label_version": "v1"
    }
    
    print("="*70)
    print("TTS API TEST")
    print("="*70)
    print(f"Endpoint: {api_endpoint}")
    print("Request:")
    print(json.dumps(test_request, indent=2))
    print()
    
    # Try different authentication methods
    auth_methods = [
        ("Authorization", f"Bearer {api_key}"),
        ("X-API-Key", api_key),
        ("api-key", api_key),
        ("key", api_key)
    ]
    
    for auth_header, auth_value in auth_methods:
        print(f"\nTrying authentication: {auth_header}")
        
        headers = {
            "Content-Type": "application/json",
            auth_header: auth_value
        }
        
        try:
            response = requests.post(api_endpoint, json=test_request, headers=headers, timeout=30)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✓ SUCCESS!")
                
                # Try to parse JSON response
                try:
                    data = response.json()
                    print("Response JSON:")
                    print(json.dumps(data, indent=2))
                    
                    # Look for audio_path
                    audio_path = data.get('audio_path')
                    if audio_path:
                        print(f"\n✓ Found audio_path: {audio_path}")
                        
                        # Download the audio
                        if download_audio_file(audio_path, api_key):
                            print("\n🎉 COMPLETE SUCCESS: API call + audio download working!")
                            return True
                        else:
                            print("\n⚠ API call worked but audio download failed")
                    else:
                        print("\n⚠ No 'audio_path' in response")
                        print("Available keys:", list(data.keys()))
                        
                except json.JSONDecodeError:
                    # Maybe direct audio response
                    print("Response is not JSON, checking if it's direct audio...")
                    content_type = response.headers.get('content-type', '')
                    if 'audio' in content_type or len(response.content) > 10000:
                        print("✓ Appears to be direct audio data")
                        
                        test_output = Path(__file__).parent.parent / 'data' / 'voices' / 'api_test_direct.wav'
                        test_output.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(test_output, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"✓ Direct audio saved to: {test_output}")
                        print(f"✓ File size: {test_output.stat().st_size} bytes")
                        print("\n🎉 SUCCESS: Direct audio response working!")
                        return True
                
                # If we get here, 200 but unknown format
                return False
                
            elif response.status_code == 401:
                print("✗ Authentication failed")
                print(response.text[:200])
                continue  # Try next auth method
                
            else:
                print(f"✗ API error: {response.status_code}")
                print(response.text[:200])
                return False
                
        except Exception as e:
            print(f"✗ Request error: {str(e)}")
            continue
    
    print("\n❌ All authentication methods failed")
    return False

if __name__ == "__main__":
    success = test_tts_api()
    if success:
        print("\n✅ API test successful! Ready to generate all samples.")
    else:
        print("\n❌ API test failed. Please check your API key and try again.")
    
    sys.exit(0 if success else 1)