#!/usr/bin/env python3
"""
Generate style-based emotion samples (216 samples)
Following TDD approach - second step
"""

import json
import time
import requests
from pathlib import Path
import sys
from typing import Dict

class StyleVariationGenerator:
    def __init__(self, api_endpoint: str = None):
        self.api_endpoint = api_endpoint
        self.output_dir = Path(__file__).parent.parent / 'data' / 'voices'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load style variation samples from API requests
        self.requests_file = Path(__file__).parent.parent / 'data' / 'api_requests.json'
        with open(self.requests_file, 'r', encoding='utf-8') as f:
            all_requests = json.load(f)
        
        # Filter style-based samples (those with style-2 through style-7)
        self.style_requests = []
        style_emotions = ['_ang_', '_sad_', '_hap_', '_whi_', '_tup_', '_tdn_']
        
        for req in all_requests:
            filename = req['filename']
            if any(emotion in filename for emotion in style_emotions):
                self.style_requests.append(req)
        
        print(f"Found {len(self.style_requests)} style variation samples to generate")
    
    def generate_mock_audio(self, filename: str):
        """Generate proper test WAV file with actual audio data"""
        import struct
        import math
        import random
        
        file_path = self.output_dir / filename
        
        # Audio parameters with slight variation per file
        sample_rate = 44100
        duration = 2.0  # 2 seconds
        
        # Different frequency based on emotion type for testing
        if '_ang_' in filename:
            frequency = 440  # Angry - A note
        elif '_sad_' in filename:
            frequency = 392  # Sad - G note
        elif '_hap_' in filename:
            frequency = 523  # Happy - C note
        elif '_whi_' in filename:
            frequency = 330  # Whisper - E note
        elif '_tup_' in filename:
            frequency = 587  # Toneup - D note
        elif '_tdn_' in filename:
            frequency = 294  # Tonedown - D note
        else:
            frequency = 440  # Default
        
        # Generate sine wave audio data
        num_samples = int(sample_rate * duration)
        audio_data = []
        
        for i in range(num_samples):
            t = i / sample_rate
            amplitude = 0.3 * math.sin(2 * math.pi * frequency * t) * math.exp(-t * 0.3)
            sample = int(amplitude * 32767)
            audio_data.append(struct.pack('<h', sample))
        
        audio_bytes = b''.join(audio_data)
        
        # Create proper WAV file header
        chunk_size = 36 + len(audio_bytes)
        subchunk2_size = len(audio_bytes)
        
        wav_header = struct.pack('<4sI4s4sIHHIIHH4sI',
            b'RIFF', chunk_size, b'WAVE', b'fmt ', 16, 1, 1,
            sample_rate, sample_rate * 2, 2, 16, b'data', subchunk2_size
        )
        
        with open(file_path, 'wb') as f:
            f.write(wav_header)
            f.write(audio_bytes)
        
        return True
    
    def call_api(self, request_data: Dict, filename: str) -> bool:
        """Call TTS API to generate audio"""
        if not self.api_endpoint:
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
    
    def verify_style_variations(self):
        """Verify all style samples are correctly formatted"""
        print("\n" + "="*70)
        print("Verifying Style Variation Samples")
        print("="*70)
        
        errors = []
        for item in self.style_requests:
            req = item['request']
            filename = item['filename']
            
            # Check style_label is NOT normal-1
            if req.get('style_label') == 'normal-1':
                errors.append(f"{filename}: style_label should not be 'normal-1'")
            
            # Check style_label is one of style-2 through style-7
            valid_styles = ['style-2', 'style-3', 'style-4', 'style-5', 'style-6', 'style-7']
            if req.get('style_label') not in valid_styles:
                errors.append(f"{filename}: invalid style_label '{req.get('style_label')}'")
            
            # Check no emotion_vector_id
            if 'emotion_vector_id' in req:
                errors.append(f"{filename}: should not have emotion_vector_id")
        
        if errors:
            print("✗ Errors found:")
            for error in errors[:5]:
                print(f"  - {error}")
            return False
        
        print(f"✓ All {len(self.style_requests)} style samples are correctly formatted")
        return True
    
    def generate_style_variations(self, batch_size: int = 10):
        """Generate style variation samples with progress tracking"""
        print("\n" + "="*70)
        print("Generating Style Variation Samples (TDD Step 2)")
        print("="*70)
        
        success_count = 0
        failed_samples = []
        
        # Group by emotion type for better progress display
        emotion_groups = {
            'angry': [], 'sad': [], 'happy': [], 
            'whisper': [], 'toneup': [], 'tonedown': []
        }
        
        for item in self.style_requests:
            filename = item['filename']
            if '_ang_' in filename:
                emotion_groups['angry'].append(item)
            elif '_sad_' in filename:
                emotion_groups['sad'].append(item)
            elif '_hap_' in filename:
                emotion_groups['happy'].append(item)
            elif '_whi_' in filename:
                emotion_groups['whisper'].append(item)
            elif '_tup_' in filename:
                emotion_groups['toneup'].append(item)
            elif '_tdn_' in filename:
                emotion_groups['tonedown'].append(item)
        
        # Process each emotion group
        for emotion_name, items in emotion_groups.items():
            if not items:
                continue
                
            print(f"\nProcessing {emotion_name} emotion ({len(items)} samples):")
            
            for i, item in enumerate(items):
                if i < 3 or i == len(items) - 1:  # Show first 3 and last
                    filename = item['filename']
                    request_data = item['request']
                    
                    print(f"  [{i+1}/{len(items)}] {filename}")
                    
                    if self.call_api(request_data, filename):
                        success_count += 1
                    else:
                        failed_samples.append(filename)
                elif i == 3:
                    print(f"  ... generating remaining {len(items) - 4} samples ...")
                    
                    # Process remaining without verbose output
                    for j in range(3, len(items) - 1):
                        if self.call_api(items[j]['request'], items[j]['filename']):
                            success_count += 1
                        else:
                            failed_samples.append(items[j]['filename'])
        
        # Summary
        print("\n" + "="*70)
        print("Style Variation Generation Complete")
        print("="*70)
        print(f"Successfully generated: {success_count}/{len(self.style_requests)}")
        
        if failed_samples:
            print(f"Failed samples: {len(failed_samples)}")
            for sample in failed_samples[:5]:
                print(f"  - {sample}")
        
        # Check generated files
        style_files = []
        for pattern in ['*_ang_*', '*_sad_*', '*_hap_*', '*_whi_*', '*_tup_*', '*_tdn_*']:
            style_files.extend(list(self.output_dir.glob(pattern)))
        
        print(f"\nStyle files in directory: {len(style_files)}")
        
        return success_count == len(self.style_requests)

def main():
    """Main execution following TDD approach"""
    
    # Get API endpoint from command line or environment
    api_endpoint = None
    if len(sys.argv) > 1:
        api_endpoint = sys.argv[1]
    
    generator = StyleVariationGenerator(api_endpoint)
    
    # Step 1: Verify style format (Red phase - test)
    print("TDD Step 1: Testing style variation sample format...")
    if not generator.verify_style_variations():
        print("Failed verification. Fix the generate_samples.py script.")
        return 1
    
    # Step 2: Generate style variations (Green phase - implementation)
    print("\nTDD Step 2: Generating style variation samples...")
    if api_endpoint:
        print(f"Using API endpoint: {api_endpoint}")
    else:
        print("No API endpoint provided - generating mock files for testing")
    
    success = generator.generate_style_variations()
    
    if success:
        print("\n✓ Style variation samples generated successfully!")
        print("\nNext step: Run generate_emotion_vectors.py to generate emotion vector samples")
    else:
        print("\n✗ Some style samples failed to generate")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())