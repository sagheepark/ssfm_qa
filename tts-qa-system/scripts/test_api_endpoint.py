#!/usr/bin/env python3
"""
Test script to verify the actual TTS API endpoint
Tests with a simple request to validate API response and audio generation
"""

import requests
import json
from pathlib import Path
import time
import sys
from urllib.parse import urljoin, urlparse

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
    
    # Headers for download request
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        download_response = requests.get(
            download_url,
            headers=headers,
            timeout=30
        )
        
        if download_response.status_code == 200:
            content_length = len(download_response.content)
            print(f"✓ Downloaded {content_length} bytes ({content_length/1024:.1f} KB)")
            
            # Save test audio file
            test_output = Path(__file__).parent.parent / 'data' / 'voices' / 'api_test_downloaded.wav'
            test_output.parent.mkdir(parents=True, exist_ok=True)
            
            with open(test_output, 'wb') as f:
                f.write(download_response.content)
            
            print(f"✓ Audio saved to: {test_output}")
            print(f"✓ Final file size: {test_output.stat().st_size} bytes")
            
            return True
        else:
            print(f"✗ Download failed with status {download_response.status_code}")
            print(f"Response: {download_response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"✗ Download error: {str(e)}")
        return False

def test_api_endpoint():
    """Test the TTS API with a simple request"""
    
    # API Configuration
    api_endpoint = "https://dev.icepeak.ai/api/speak/batch/post"
    
    # Test request payload
    test_request = {
        "text": "Hello, this is a test message for TTS API validation.",
        "actor_id": "voice_001",
        "style_label": "normal-1",
        "emotion_scale": 1.0,
        "tempo": 1,
        "pitch": 0,
        "lang": "en",  # Changed to English for the test text
        "mode": "one-vocoder",
        "bp_c_l": True,
        "retake": True,
        "adjust_lastword": 0,
        "style_label_version": "v1"
    }
    
    print("="*70)
    print("TTS API ENDPOINT TEST")
    print("="*70)
    print(f"Endpoint: {api_endpoint}")
    print(f"Method: POST")
    print()
    
    print("Test Request Payload:")
    print(json.dumps(test_request, indent=2))
    print()
    
    # Get API key from user input or environment
    api_key = input("Enter your API key: ").strip()
    if not api_key:
        print("No API key provided. Exiting.")
        return False, "No API key"
    
    # Try different authentication formats
    auth_formats = [
        {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        {"Content-Type": "application/json", "X-API-Key": api_key},
        {"Content-Type": "application/json", "api-key": api_key},
        {"Content-Type": "application/json", "key": api_key}
    ]
    
    for i, headers in enumerate(auth_formats):
        auth_method = list(headers.keys())[-1]  # Get the auth header name
        print(f"\nTrying authentication method: {auth_method}")
        
        success, message = try_api_request(api_endpoint, test_request, headers, api_key)
        if success:
            return success, message
        elif "401" not in message:  # If not auth error, don't try other methods
            return success, message
    
    return False, "All authentication methods failed"

def try_api_request(api_endpoint: str, test_request: dict, headers: dict, api_key: str):
    """Try API request with specific headers"""
    
    try:
        print("Sending request to API...")
        start_time = time.time()
        
        response = requests.post(
            api_endpoint,
            json=test_request,
            headers=headers,
            timeout=30
        )
        
        elapsed_time = time.time() - start_time
        print(f"Response received in {elapsed_time:.2f} seconds")
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        if response.status_code == 200:
            print("\n✓ SUCCESS: API responded with 200 OK")
            
            # Parse JSON response to get audio_path
            try:
                response_data = response.json()
                print("Response JSON:")
                print(json.dumps(response_data, indent=2))
                
                # Look for audio_path in response
                audio_path = response_data.get('audio_path')
                if audio_path:
                    print(f"\n✓ Found audio_path: {audio_path}")
                    
                    # Download the audio file
                    success = download_audio_file(audio_path, api_key)
                    if success:
                        return True, "API test and audio download successful"
                    else:
                        return False, "Audio download failed"
                else:
                    print("\n⚠ No 'audio_path' found in response")
                    print("Available keys:", list(response_data.keys()))
                    return False, "No audio_path in response"
                    
            except json.JSONDecodeError:
                print("\n⚠ Response is not JSON")
                content_type = response.headers.get('content-type', '')
                content_length = len(response.content)
                
                print(f"Content-Type: {content_type}")
                print(f"Content-Length: {content_length} bytes ({content_length/1024:.1f} KB)")
                
                if 'audio' in content_type or content_length > 10000:
                    print("✓ Response appears to be direct audio data")
                    
                    # Save test audio file
                    test_output = Path(__file__).parent.parent / 'data' / 'voices' / 'api_test.wav'
                    test_output.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(test_output, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"✓ Test audio saved to: {test_output}")
                    print(f"✓ File size: {test_output.stat().st_size} bytes")
                    
                    return True, "API test successful (direct audio)"
                else:
                    print("⚠ Response doesn't appear to be audio")
                    print("Response content (first 200 chars):")
                    print(response.text[:200])
                    return False, "Unknown response format"
        
        elif response.status_code == 401:
            print("\n✗ AUTHORIZATION ERROR (401)")
            print("The API requires authentication.")
            print("Response:")
            print(response.text[:500])
            return False, "Authentication required"
        
        elif response.status_code == 400:
            print("\n✗ BAD REQUEST (400)")
            print("Request format may be incorrect.")
            print("Response:")
            print(response.text[:500])
            return False, "Bad request format"
        
        else:
            print(f"\n✗ API ERROR ({response.status_code})")
            print("Response:")
            print(response.text[:500])
            return False, f"API error {response.status_code}"
    
    except requests.exceptions.Timeout:
        print("\n✗ TIMEOUT ERROR")
        print("Request timed out after 30 seconds")
        return False, "Timeout"
    
    except requests.exceptions.ConnectionError:
        print("\n✗ CONNECTION ERROR")
        print("Could not connect to the API endpoint")
        return False, "Connection error"
    
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {str(e)}")
        return False, f"Error: {str(e)}"

def test_with_authorization():
    """Test with different authorization approaches"""
    
    print("\n" + "="*70)
    print("TESTING WITH AUTHORIZATION")
    print("="*70)
    
    # Common authorization headers to try
    auth_tests = [
        {},  # No auth (already tested above)
        {"Authorization": "Bearer YOUR_TOKEN_HERE"},
        {"X-API-Key": "YOUR_API_KEY_HERE"},
        {"api-key": "YOUR_API_KEY_HERE"},
    ]
    
    for i, auth_header in enumerate(auth_tests[1:], 1):  # Skip first (no auth)
        print(f"\nTest {i}: {list(auth_header.keys())[0]}")
        print("This would require your actual API key/token.")
        print("Please update the script with your credentials if auth is needed.")

def main():
    """Main test execution"""
    
    # Test basic API call
    success, message = test_api_endpoint()
    
    if success:
        print("\n" + "="*70)
        print("API TEST RESULT: SUCCESS ✓")
        print("="*70)
        print("The API endpoint is working correctly.")
        print("You can now proceed with generating all samples.")
        print()
        print("Next steps:")
        print("1. python3 scripts/batch_generate.py --endpoint https://dev.icepeak.ai/api/speak/batch/post")
        print("2. Or run individual generators with the endpoint")
        
    else:
        print("\n" + "="*70)
        print("API TEST RESULT: FAILED ✗")
        print("="*70)
        print(f"Issue: {message}")
        
        if "Authentication" in message or "401" in message:
            test_with_authorization()
            print("\nPlease provide the correct authorization details.")
        
        print("\nPlease resolve the API issue before proceeding with sample generation.")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())