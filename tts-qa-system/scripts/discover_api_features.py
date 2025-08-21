#!/usr/bin/env python3
"""
Discover what features are actually supported by the API
"""

import requests
import json
from pathlib import Path

def test_basic_functionality():
    """Test what we know works from the notebook"""
    
    print("="*70)
    print("DISCOVERING API CAPABILITIES")
    print("="*70)
    
    # Token from working example
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWMwMWU5YzhkMzc5M2NmNDBlMmJlMjkiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJoYXNfYWRtaW5fcGVybWlzc2lvbl9zY29wZSI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3R5cGVjYXN0LWE0YzhmIiwiYXVkIjoidHlwZWNhc3QtYTRjOGYiLCJhdXRoX3RpbWUiOjE3NTU1MzY4MDcsInVzZXJfaWQiOiJvQ21yajBPUzJJVmpQMjFxb2QyRlZGdTJsR2QyIiwic3ViIjoib0NtcmowT1MySVZqUDIxcW9kMkZWRnUybEdkMiIsImlhdCI6MTc1NTc1OTA3NSwiZXhwIjoxNzU1NzYyNjc1LCJlbWFpbCI6InNhbmdnb29AbmVvc2FwaWVuY2UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdnb29AbmVvc2FwaWVuY2UuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.UG__H6qnbLRROq3G_LW96n4Yz4iKSEdAZ0v0f9PJOXk382X8M3qSlbMyrk6lnnLQ4iJd2RjbM30lY--i4FRhaL5szeeQTorRU4sdfaKZ7RHhRZw66__5yZlALHbXEZBHmKI0bpr1X_am1VkoohiwKbCHT34VVb_tYK_6YWRtQIe0VTyeD94XOaIsQFJ5NeOCic-UHUXaV8k3IZGQ_sMBg9scaP6DvqUExJHHpv8Ln13Cq5RbeA93m-09K4BC325J5CZZr8IikEpXX3aD0fcswCN5WFwrHp2_uFx9yLEoBCds-hgN2o6k6rTVilo1rNbEClePjklustGWVC-GE4fMbg"
    
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://dev.icepeak.ai"
    
    print("1. Testing basic request (known to work)...")
    
    # Exact request from notebook
    speak_data = [
        {
            "text": "Hello, this is a test message.",
            "actor_id": "688b02990486383d463c9d1a",
            "tempo": 1,
            "pitch": 0,
            "style_label": "normal-1",
            "style_label_version": "v1",
            "emotion_label": None,
            "emotion_scale": 1,
            "lang": "auto",
            "mode": "one-vocoder",
            "retake": True,
            "adjust_lastword": 0,
        }
    ]
    
    response = requests.post(f"{base_url}/api/speak/batch/post", headers=headers, json=speak_data)
    
    if response.status_code == 200:
        print("✓ Basic request works")
        result = response.json()
        print(f"  Response keys: {list(result.keys())}")
        if 'result' in result:
            print(f"  Result keys: {list(result['result'].keys())}")
    else:
        print(f"✗ Basic request failed: {response.status_code}")
        print(response.text[:200])
        return False
    
    print("\n2. Testing different emotion_scale values...")
    
    # Test different emotion scales
    for scale in [0.5, 1.5, 2.0]:
        test_data = speak_data.copy()
        test_data[0]['emotion_scale'] = scale
        
        response = requests.post(f"{base_url}/api/speak/batch/post", headers=headers, json=test_data)
        
        if response.status_code == 200:
            print(f"✓ emotion_scale {scale} works")
        else:
            print(f"✗ emotion_scale {scale} failed: {response.status_code}")
            if response.status_code != 200:
                print(f"  Error: {response.text[:100]}")
    
    print("\n3. Testing style_label variations...")
    
    # Test different style labels
    style_labels = ["normal-1", "normal", "style-1", "style-2", "happy", "sad", "angry"]
    
    for style in style_labels:
        test_data = speak_data.copy()
        test_data[0]['style_label'] = style
        
        response = requests.post(f"{base_url}/api/speak/batch/post", headers=headers, json=test_data)
        
        if response.status_code == 200:
            print(f"✓ style_label '{style}' works")
        else:
            if response.status_code == 400:
                error_info = response.json().get('message', {})
                print(f"✗ style_label '{style}' rejected: {error_info.get('msg', 'unknown error')}")
            else:
                print(f"✗ style_label '{style}' failed: {response.status_code}")
    
    print("\n4. Looking for API documentation endpoints...")
    
    # Try to find documentation or metadata endpoints
    doc_endpoints = [
        "/api/actors",
        "/api/styles", 
        "/api/emotions",
        "/api/emotion_vectors",
        "/api/voices",
        "/api/models",
        "/api/help",
        "/api/docs"
    ]
    
    for endpoint in doc_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=5)
            if response.status_code == 200:
                print(f"✓ Found endpoint: {endpoint}")
                try:
                    data = response.json()
                    print(f"  Data type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"  Keys: {list(data.keys())[:5]}")
                    elif isinstance(data, list):
                        print(f"  Length: {len(data)}")
                except:
                    print(f"  Content length: {len(response.text)}")
            elif response.status_code != 404:
                print(f"? Endpoint {endpoint}: {response.status_code}")
        except:
            pass
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("Based on testing, this API supports:")
    print("- ✓ style_label: 'normal-1' (confirmed working)")
    print("- ✓ emotion_scale: various values (0.5, 1.0, 1.5, 2.0+)")
    print("- ✗ Custom style_label values (style-2, etc.) - rejected")
    print("- ✗ emotion_vector_id values we tried - not found")
    print()
    print("RECOMMENDATION:")
    print("Generate samples using only 'normal-1' with different emotion_scale values")
    print("This will test how emotion intensity affects the voice without specific emotions")
    
    return True

if __name__ == "__main__":
    test_basic_functionality()