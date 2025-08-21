#!/usr/bin/env python3
"""
Batch generation script for all TTS samples
Handles API calls with rate limiting and error recovery
"""

import json
import time
import requests
from pathlib import Path
import sys
from typing import Dict, List
import argparse

class BatchTTSGenerator:
    def __init__(self, api_endpoint: str, api_key: str = None):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.output_dir = Path(__file__).parent.parent / 'data' / 'voices'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load API requests
        self.requests_file = Path(__file__).parent.parent / 'data' / 'api_requests.json'
        with open(self.requests_file, 'r', encoding='utf-8') as f:
            self.api_requests = json.load(f)
        
        # Progress tracking
        self.progress_file = self.output_dir.parent / 'generation_progress.json'
        self.completed_files = self.load_progress()
        
    def load_progress(self) -> set:
        """Load previously completed files"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                return set(data.get('completed', []))
        return set()
    
    def save_progress(self):
        """Save current progress"""
        with open(self.progress_file, 'w') as f:
            json.dump({
                'completed': list(self.completed_files),
                'total': len(self.api_requests),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, indent=2)
    
    def call_api(self, request_data: Dict, filename: str, retry_count: int = 3) -> bool:
        """
        Call TTS API with retry logic
        """
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        for attempt in range(retry_count):
            try:
                response = requests.post(
                    self.api_endpoint,
                    json=request_data,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    # Save audio file
                    file_path = self.output_dir / filename
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    return True
                else:
                    print(f"  API error {response.status_code}: {response.text[:100]}")
                    if attempt < retry_count - 1:
                        print(f"  Retrying in 5 seconds... (attempt {attempt + 2}/{retry_count})")
                        time.sleep(5)
                        
            except requests.exceptions.Timeout:
                print(f"  Timeout error")
                if attempt < retry_count - 1:
                    print(f"  Retrying in 5 seconds... (attempt {attempt + 2}/{retry_count})")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"  Error: {str(e)}")
                if attempt < retry_count - 1:
                    print(f"  Retrying in 5 seconds... (attempt {attempt + 2}/{retry_count})")
                    time.sleep(5)
        
        return False
    
    def generate_all(self, rate_limit: int = 10, start_from: int = 0):
        """
        Generate all samples with rate limiting
        """
        print(f"\n{'='*70}")
        print(f"TTS Batch Generation")
        print(f"{'='*70}")
        print(f"API Endpoint: {self.api_endpoint}")
        print(f"Total samples: {len(self.api_requests)}")
        print(f"Already completed: {len(self.completed_files)}")
        print(f"Rate limit: {rate_limit} requests/second")
        print(f"Output directory: {self.output_dir}")
        print(f"{'='*70}\n")
        
        # Calculate time estimate
        remaining = len(self.api_requests) - len(self.completed_files)
        if remaining > 0:
            estimated_time = remaining / rate_limit
            print(f"Estimated time for remaining: {estimated_time/60:.1f} minutes\n")
        
        success_count = 0
        failed_files = []
        skipped_count = 0
        
        for i, item in enumerate(self.api_requests[start_from:], start=start_from):
            filename = item['filename']
            request_data = item['request']
            
            # Skip if already completed
            if filename in self.completed_files:
                skipped_count += 1
                print(f"[{i+1}/{len(self.api_requests)}] Skipping {filename} (already completed)")
                continue
            
            print(f"[{i+1}/{len(self.api_requests)}] Generating {filename}")
            
            # Show request details for first few samples
            if i < 3:
                print(f"  Text: {request_data['text'][:50]}...")
                if 'style_label' in request_data and request_data['style_label'] != 'normal-1':
                    print(f"  Style: {request_data['style_label']}")
                if 'emotion_vector_id' in request_data:
                    print(f"  Emotion Vector: {request_data['emotion_vector_id'][:8]}...")
                print(f"  Scale: {request_data.get('emotion_scale', 1.0)}")
            
            # Make API call
            if self.call_api(request_data, filename):
                success_count += 1
                self.completed_files.add(filename)
                print(f"  ✓ Success")
                
                # Save progress every 10 successful generations
                if success_count % 10 == 0:
                    self.save_progress()
            else:
                failed_files.append(filename)
                print(f"  ✗ Failed after all retries")
            
            # Rate limiting
            if i < len(self.api_requests) - 1:
                time.sleep(1.0 / rate_limit)
        
        # Save final progress
        self.save_progress()
        
        # Print summary
        print(f"\n{'='*70}")
        print(f"Generation Complete")
        print(f"{'='*70}")
        print(f"Successfully generated: {success_count}")
        print(f"Skipped (already done): {skipped_count}")
        print(f"Failed: {len(failed_files)}")
        print(f"Total completed: {len(self.completed_files)}/{len(self.api_requests)}")
        
        if failed_files:
            print(f"\nFailed files:")
            for f in failed_files[:20]:  # Show first 20
                print(f"  - {f}")
            if len(failed_files) > 20:
                print(f"  ... and {len(failed_files) - 20} more")
            
            # Save failed files list
            failed_file_path = self.output_dir.parent / 'failed_files.json'
            with open(failed_file_path, 'w') as f:
                json.dump(failed_files, f, indent=2)
            print(f"\nFailed files list saved to: {failed_file_path}")
        
        return success_count, failed_files
    
    def verify_generation(self):
        """
        Verify all files were generated correctly
        """
        print(f"\n{'='*70}")
        print(f"Verifying Generated Files")
        print(f"{'='*70}")
        
        expected_files = [item['filename'] for item in self.api_requests]
        existing_files = list(self.output_dir.glob('*.wav'))
        existing_names = [f.name for f in existing_files]
        
        missing_files = []
        for expected in expected_files:
            if expected not in existing_names:
                missing_files.append(expected)
        
        print(f"Expected files: {len(expected_files)}")
        print(f"Existing files: {len(existing_files)}")
        print(f"Missing files: {len(missing_files)}")
        
        if missing_files:
            print(f"\nMissing files:")
            for f in missing_files[:20]:
                print(f"  - {f}")
            if len(missing_files) > 20:
                print(f"  ... and {len(missing_files) - 20} more")
        else:
            print("\n✓ All expected files have been generated!")
        
        # Check file sizes
        small_files = []
        for f in existing_files:
            if f.stat().st_size < 1000:  # Less than 1KB
                small_files.append(f.name)
        
        if small_files:
            print(f"\nWarning: {len(small_files)} files are smaller than 1KB:")
            for f in small_files[:10]:
                print(f"  - {f}")
        
        return len(missing_files) == 0

def main():
    parser = argparse.ArgumentParser(description='Batch generate TTS samples')
    parser.add_argument('--endpoint', required=True, help='TTS API endpoint URL')
    parser.add_argument('--api-key', help='API key for authentication')
    parser.add_argument('--rate-limit', type=int, default=10, help='Requests per second (default: 10)')
    parser.add_argument('--start-from', type=int, default=0, help='Start from sample index (default: 0)')
    parser.add_argument('--verify-only', action='store_true', help='Only verify existing files')
    
    args = parser.parse_args()
    
    generator = BatchTTSGenerator(args.endpoint, args.api_key)
    
    if args.verify_only:
        generator.verify_generation()
    else:
        # Generate samples
        success, failed = generator.generate_all(args.rate_limit, args.start_from)
        
        # Verify after generation
        if success > 0:
            time.sleep(2)
            generator.verify_generation()

if __name__ == "__main__":
    main()