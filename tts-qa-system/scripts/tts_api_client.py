#!/usr/bin/env python3
"""
Proper TTS API Client following the 4-step asynchronous workflow:
1. POST request to start generation
2. Poll GET to check completion status
3. GET cloudfront URL 
4. Download final audio
"""

import requests
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

class TTSAPIClient:
    def __init__(self, token: str):
        # Extract token from Jupyter notebook
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.base_url = "https://dev.icepeak.ai"
        
    def create_request_payload(self, text: str, actor_id: str, style_label: str = "normal-1", 
                              emotion_vector_id: Optional[str] = None, emotion_scale: float = 1.0) -> Dict:
        """Create TTS request payload following the backend format"""
        
        payload = {
            "text": text,
            "actor_id": actor_id,
            "tempo": 1,
            "pitch": 0,
            "style_label": style_label,
            "style_label_version": "v1",
            "emotion_label": None,
            "emotion_scale": emotion_scale,
            "previous_text": None,
            "next_text": None, 
            "lang": "auto",
            "mode": "one-vocoder",
            "retake": True,
            "adjust_lastword": 0,
        }
        
        # Add emotion_vector_id if provided
        if emotion_vector_id:
            payload["emotion_vector_id"] = emotion_vector_id
            
        return payload
    
    def step1_request_generation(self, requests_data: List[Dict]) -> Optional[List[str]]:
        """Step 1: Send TTS generation request"""
        
        print(f"Step 1: Requesting generation for {len(requests_data)} samples...")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/speak/batch/post",
                headers=self.headers,
                json=requests_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                speak_urls = result.get("result", {}).get("speak_urls", [])
                print(f"✓ Generation requested. Got {len(speak_urls)} speak URLs")
                return speak_urls
            else:
                print(f"✗ Request failed: {response.status_code}")
                print(response.text[:200])
                return None
                
        except Exception as e:
            print(f"✗ Request error: {str(e)}")
            return None
    
    def step2_poll_completion(self, speak_urls: List[str], max_attempts: int = 20, 
                             poll_interval: float = 0.5) -> Optional[List[Dict]]:
        """Step 2: Poll for completion status"""
        
        print(f"Step 2: Polling for completion (max {max_attempts} attempts, {poll_interval}s interval)...")
        
        for attempt in range(max_attempts):
            try:
                response = requests.post(
                    f"{self.base_url}/api/speak/batch/get",
                    headers=self.headers,
                    json=speak_urls,
                    timeout=30
                )
                
                if response.status_code == 200:
                    results = response.json()["result"]
                    
                    # Check if all are done
                    all_done = all(result.get("status") == "done" for result in results)
                    done_count = sum(1 for result in results if result.get("status") == "done")
                    
                    print(f"  Attempt {attempt + 1}: {done_count}/{len(results)} done")
                    
                    if all_done:
                        print("✓ All generations completed!")
                        return results
                else:
                    print(f"✗ Poll failed: {response.status_code}")
                    return None
                    
            except Exception as e:
                print(f"✗ Poll error: {str(e)}")
                return None
            
            time.sleep(poll_interval)
        
        print(f"✗ Polling timed out after {max_attempts} attempts")
        return None
    
    def step3_get_download_url(self, audio_url: str) -> Optional[str]:
        """Step 3: Get CloudFront download URL"""
        
        cloudfront_url = f"{audio_url}/cloudfront"
        
        try:
            response = requests.get(
                cloudfront_url,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                download_url = result.get("result")
                return download_url
            else:
                print(f"✗ CloudFront URL failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ CloudFront error: {str(e)}")
            return None
    
    def step4_download_audio(self, download_url: str, output_path: Path) -> bool:
        """Step 4: Download final audio file"""
        
        try:
            # No authorization needed for final download
            response = requests.get(download_url, timeout=30)
            
            if response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                file_size = output_path.stat().st_size
                print(f"✓ Downloaded: {output_path.name} ({file_size/1024:.1f} KB)")
                return True
            else:
                print(f"✗ Download failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Download error: {str(e)}")
            return False
    
    def generate_audio_batch(self, samples: List[Dict], output_dir: Path) -> Tuple[int, int]:
        """Complete workflow for generating multiple audio samples"""
        
        print("="*70)
        print("TTS BATCH GENERATION - 4-Step Workflow")
        print("="*70)
        
        # Prepare request data
        requests_data = []
        for sample in samples:
            payload = self.create_request_payload(
                text=sample['text'],
                actor_id=sample['actor_id'],
                style_label=sample.get('style_label', 'normal-1'),
                emotion_vector_id=sample.get('emotion_vector_id'),
                emotion_scale=sample.get('emotion_scale', 1.0)
            )
            requests_data.append(payload)
        
        # Step 1: Request generation
        speak_urls = self.step1_request_generation(requests_data)
        if not speak_urls:
            return 0, len(samples)
        
        # Step 2: Poll for completion
        results = self.step2_poll_completion(speak_urls)
        if not results:
            return 0, len(samples)
        
        # Steps 3 & 4: Download each audio file
        success_count = 0
        
        print(f"\nStep 3 & 4: Processing {len(results)} completed generations...")
        
        for i, (result, sample) in enumerate(zip(results, samples)):
            if result.get("status") != "done":
                print(f"✗ Sample {i+1} not completed: {result.get('status')}")
                continue
                
            # Get audio URL (use hd1 for highest quality)
            audio_info = result.get("audio", {})
            audio_url = audio_info.get("hd1", {}).get("url") or audio_info.get("url")
            
            if not audio_url:
                print(f"✗ Sample {i+1} missing audio URL")
                continue
            
            # Step 3: Get download URL
            download_url = self.step3_get_download_url(audio_url)
            if not download_url:
                print(f"✗ Sample {i+1} failed to get download URL")
                continue
            
            # Step 4: Download audio
            output_path = output_dir / sample['filename']
            if self.step4_download_audio(download_url, output_path):
                success_count += 1
            
        failed_count = len(samples) - success_count
        
        print("\n" + "="*70)
        print("BATCH GENERATION COMPLETE")
        print("="*70)
        print(f"Success: {success_count}/{len(samples)}")
        print(f"Failed: {failed_count}")
        
        return success_count, failed_count

def test_single_sample():
    """Test the API with a single sample"""
    
    # Token from Jupyter notebook (you'll need to update this)
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3YmZiMmExMWRkZmZjMGFkMmU2ODE0YzY4NzYzYjhjNjg3NTgxZDgiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWMwMWU5YzhkMzc5M2NmNDBlMmJlMjkiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJoYXNfYWRtaW5fcGVybWlzc2lvbl9zY29wZSI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3R5cGVjYXN0LWE0YzhmIiwiYXVkIjoidHlwZWNhc3QtYTRjOGYiLCJhdXRoX3RpbWUiOjE3NTU1MzY4MDcsInVzZXJfaWQiOiJvQ21yajBPUzJJVmpQMjFxb2QyRlZGdTJsR2QyIiwic3ViIjoib0NtcmowT1MySVZqUDIxcW9kMkZWRnUybEdkMiIsImlhdCI6MTc1NTc1OTA3NSwiZXhwIjoxNzU1NzYyNjc1LCJlbWFpbCI6InNhbmdnb29AbmVvc2FwaWVuY2UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdnb29AbmVvc2FwaWVuY2UuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.UG__H6qnbLRROq3G_LW96n4Yz4iKSEdAZ0v0f9PJOXk382X8M3qSlbMyrk6lnnLQ4iJd2RjbM30lY--i4FRhaL5szeeQTorRU4sdfaKZ7RHhRZw66__5yZlALHbXEZBHmKI0bpr1X_am1VkoohiwKbCHT34VVb_tYK_6YWRtQIe0VTyeD94XOaIsQFJ5NeOCic-UHUXaV8k3IZGQ_sMBg9scaP6DvqUExJHHpv8Ln13Cq5RbeA93m-09K4BC325J5CZZr8IikEpXX3aD0fcswCN5WFwrHp2_uFx9yLEoBCds-hgN2o6k6rTVilo1rNbEClePjklustGWVC-GE4fMbg"
    
    client = TTSAPIClient(token)
    
    # Test sample
    test_sample = {
        'text': "Hello, this is a test message for TTS API validation.",
        'actor_id': "688b02990486383d463c9d1a",  # From notebook
        'style_label': "normal-1",
        'emotion_scale': 1.0,
        'filename': 'test_api_real.wav'
    }
    
    output_dir = Path(__file__).parent.parent / 'data' / 'voices'
    
    success, failed = client.generate_audio_batch([test_sample], output_dir)
    
    if success > 0:
        print("\n🎉 SUCCESS: Real TTS API workflow is working!")
        print(f"Generated file: {output_dir / test_sample['filename']}")
        return True
    else:
        print("\n❌ FAILED: TTS API workflow not working")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_single_sample()
    else:
        print("TTS API Client Module")
        print("Use --test to run a single sample test")
        print("Import this module to use the TTSAPIClient class")