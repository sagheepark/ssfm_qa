#!/usr/bin/env python3
"""
Generate reference audio samples only (6 samples)
Following TDD approach - start with minimal implementation
"""

import json
import time
import requests
from pathlib import Path
import sys
from typing import Dict

class ReferenceGenerator:
    def __init__(self, api_endpoint: str = None):
        self.api_endpoint = api_endpoint
        self.output_dir = Path(__file__).parent.parent / 'data' / 'voices'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load only reference samples from API requests
        self.requests_file = Path(__file__).parent.parent / 'data' / 'api_requests.json'
        with open(self.requests_file, 'r', encoding='utf-8') as f:
            all_requests = json.load(f)
        
        # Filter only reference samples
        self.reference_requests = [
            req for req in all_requests 
            if '_ref_' in req['filename']
        ]
        
        print(f"Found {len(self.reference_requests)} reference samples to generate")
    
    def generate_mock_audio(self, filename: str):
        """Generate proper test WAV file with actual audio data"""
        import struct
        import math
        
        file_path = self.output_dir / filename
        
        # Audio parameters
        sample_rate = 44100
        duration = 2.0  # 2 seconds
        frequency = 440  # A note
        
        # Generate sine wave audio data
        num_samples = int(sample_rate * duration)
        audio_data = []
        
        for i in range(num_samples):
            t = i / sample_rate
            # Generate a simple sine wave with some variation
            amplitude = 0.3 * math.sin(2 * math.pi * frequency * t) * math.exp(-t * 0.5)
            sample = int(amplitude * 32767)  # 16-bit signed
            audio_data.append(struct.pack('<h', sample))
        
        audio_bytes = b''.join(audio_data)
        
        # Create proper WAV file header
        chunk_size = 36 + len(audio_bytes)
        subchunk2_size = len(audio_bytes)
        
        wav_header = struct.pack('<4sI4s4sIHHIIHH4sI',
            b'RIFF',           # ChunkID
            chunk_size,        # ChunkSize
            b'WAVE',           # Format
            b'fmt ',           # Subchunk1ID
            16,                # Subchunk1Size (PCM)
            1,                 # AudioFormat (PCM)
            1,                 # NumChannels (mono)
            sample_rate,       # SampleRate
            sample_rate * 2,   # ByteRate
            2,                 # BlockAlign
            16,                # BitsPerSample
            b'data',           # Subchunk2ID
            subchunk2_size     # Subchunk2Size
        )
        
        with open(file_path, 'wb') as f:
            f.write(wav_header)
            f.write(audio_bytes)
        
        return True
    
    def call_api(self, request_data: Dict, filename: str) -> bool:
        """Call TTS API to generate audio"""
        if not self.api_endpoint:
            print(f"  No API endpoint - generating mock file")
            return self.generate_mock_audio(filename)
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                file_path = self.output_dir / filename
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"  API error {response.status_code}: {response.text[:100]}")
                return False
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            return False
    
    def generate_references(self):
        """Generate only the 6 reference samples"""
        print("\n" + "="*70)
        print("Generating Reference Samples (TDD Step 1)")
        print("="*70)
        
        success_count = 0
        
        for i, item in enumerate(self.reference_requests, 1):
            filename = item['filename']
            request_data = item['request']
            
            print(f"\n[{i}/{len(self.reference_requests)}] Generating {filename}")
            print(f"  Voice: {request_data['actor_id']}")
            print(f"  Style: {request_data['style_label']}")
            print(f"  Text: {request_data['text'][:50]}...")
            
            if self.call_api(request_data, filename):
                success_count += 1
                print(f"  ✓ Success")
            else:
                print(f"  ✗ Failed")
        
        # Summary
        print("\n" + "="*70)
        print("Reference Generation Complete")
        print("="*70)
        print(f"Successfully generated: {success_count}/{len(self.reference_requests)}")
        
        # Verify files exist
        existing_refs = list(self.output_dir.glob('*_ref_*.wav'))
        print(f"Reference files in directory: {len(existing_refs)}")
        for ref_file in existing_refs:
            size_kb = ref_file.stat().st_size / 1024
            print(f"  - {ref_file.name} ({size_kb:.1f} KB)")
        
        return success_count == len(self.reference_requests)
    
    def verify_references(self):
        """Verify all reference samples are correctly formatted"""
        print("\n" + "="*70)
        print("Verifying Reference Samples")
        print("="*70)
        
        for item in self.reference_requests:
            req = item['request']
            filename = item['filename']
            
            # Check style_label is normal-1
            if req.get('style_label') != 'normal-1':
                print(f"✗ {filename}: style_label should be 'normal-1', got '{req.get('style_label')}'")
                return False
            
            # Check no emotion_vector_id
            if 'emotion_vector_id' in req:
                print(f"✗ {filename}: should not have emotion_vector_id")
                return False
            
            # Check emotion_scale is 1.0
            if req.get('emotion_scale') != 1.0:
                print(f"✗ {filename}: emotion_scale should be 1.0, got {req.get('emotion_scale')}")
                return False
        
        print("✓ All reference samples are correctly formatted")
        return True

def main():
    """Main execution following TDD approach"""
    
    # Get API endpoint from command line or environment
    api_endpoint = None
    if len(sys.argv) > 1:
        api_endpoint = sys.argv[1]
    
    generator = ReferenceGenerator(api_endpoint)
    
    # Step 1: Verify reference format (Red phase - test)
    print("TDD Step 1: Testing reference sample format...")
    if not generator.verify_references():
        print("Failed verification. Fix the generate_samples.py script.")
        return 1
    
    # Step 2: Generate references (Green phase - implementation)
    print("\nTDD Step 2: Generating reference samples...")
    if api_endpoint:
        print(f"Using API endpoint: {api_endpoint}")
    else:
        print("No API endpoint provided - generating mock files for testing")
    
    success = generator.generate_references()
    
    if success:
        print("\n✓ Reference samples generated successfully!")
        print("\nNext step: Run generate_style_variations.py to generate style-based samples")
    else:
        print("\n✗ Some reference samples failed to generate")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())