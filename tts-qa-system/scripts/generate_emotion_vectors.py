#!/usr/bin/env python3
"""
Generate emotion vector samples (216 samples)
Following TDD approach - final step
"""

import json
import time
import requests
from pathlib import Path
import sys
from typing import Dict

class EmotionVectorGenerator:
    def __init__(self, api_endpoint: str = None):
        self.api_endpoint = api_endpoint
        self.output_dir = Path(__file__).parent.parent / 'data' / 'voices'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load emotion vector samples from API requests
        self.requests_file = Path(__file__).parent.parent / 'data' / 'api_requests.json'
        with open(self.requests_file, 'r', encoding='utf-8') as f:
            all_requests = json.load(f)
        
        # Filter emotion vector samples
        self.vector_requests = []
        vector_emotions = ['_exc_', '_fur_', '_ter_', '_fea_', '_sur_', '_exm_']
        
        for req in all_requests:
            filename = req['filename']
            if any(emotion in filename for emotion in vector_emotions):
                self.vector_requests.append(req)
        
        print(f"Found {len(self.vector_requests)} emotion vector samples to generate")
    
    def generate_mock_audio(self, filename: str):
        """Generate proper test WAV file with actual audio data"""
        import struct
        import math
        
        file_path = self.output_dir / filename
        
        # Audio parameters with slight variation per emotion type
        sample_rate = 44100
        duration = 2.0  # 2 seconds
        
        # Different frequency and pattern based on emotion vector type
        if '_exc_' in filename:
            frequency = 550  # Excited - higher pitch
            pattern = "excited"
        elif '_fur_' in filename:
            frequency = 350  # Furious - lower, intense
            pattern = "furious"
        elif '_ter_' in filename:
            frequency = 300  # Terrified - very low
            pattern = "terrified"
        elif '_fea_' in filename:
            frequency = 320  # Fear - low, trembling
            pattern = "fear"
        elif '_sur_' in filename:
            frequency = 600  # Surprise - high pitch
            pattern = "surprise"
        elif '_exm_' in filename:
            frequency = 500  # Excitement - medium-high
            pattern = "excitement"
        else:
            frequency = 440  # Default
            pattern = "default"
        
        # Generate audio with emotion-specific patterns
        num_samples = int(sample_rate * duration)
        audio_data = []
        
        for i in range(num_samples):
            t = i / sample_rate
            
            if pattern == "excited":
                # Fast oscillation
                amplitude = 0.3 * math.sin(2 * math.pi * frequency * t) * (1 + 0.2 * math.sin(20 * t))
            elif pattern == "furious":
                # Harsh, distorted
                amplitude = 0.3 * math.sin(2 * math.pi * frequency * t) * (1 + 0.5 * math.sin(5 * t))
            elif pattern in ["terrified", "fear"]:
                # Trembling effect
                trembling = 1 + 0.1 * math.sin(2 * math.pi * 8 * t)
                amplitude = 0.2 * math.sin(2 * math.pi * frequency * t) * trembling
            elif pattern == "surprise":
                # Sharp attack, quick decay
                envelope = math.exp(-t * 2)
                amplitude = 0.4 * math.sin(2 * math.pi * frequency * t) * envelope
            else:
                # Standard sine wave
                amplitude = 0.3 * math.sin(2 * math.pi * frequency * t) * math.exp(-t * 0.5)
            
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
    
    def verify_emotion_vectors(self):
        """Verify all emotion vector samples are correctly formatted"""
        print("\n" + "="*70)
        print("Verifying Emotion Vector Samples")
        print("="*70)
        
        errors = []
        for item in self.vector_requests:
            req = item['request']
            filename = item['filename']
            
            # Check style_label is normal-1
            if req.get('style_label') != 'normal-1':
                errors.append(f"{filename}: style_label should be 'normal-1', got '{req.get('style_label')}'")
            
            # Check has emotion_vector_id
            if 'emotion_vector_id' not in req:
                errors.append(f"{filename}: missing emotion_vector_id")
            
            # Check emotion_vector_id format
            vector_id = req.get('emotion_vector_id', '')
            if len(vector_id) != 24:  # MongoDB ObjectId length
                errors.append(f"{filename}: invalid emotion_vector_id format")
        
        if errors:
            print("✗ Errors found:")
            for error in errors[:5]:
                print(f"  - {error}")
            return False
        
        print(f"✓ All {len(self.vector_requests)} emotion vector samples are correctly formatted")
        return True
    
    def generate_emotion_vectors(self):
        """Generate emotion vector samples with progress tracking"""
        print("\n" + "="*70)
        print("Generating Emotion Vector Samples (TDD Step 3)")
        print("="*70)
        
        success_count = 0
        failed_samples = []
        
        # Group by emotion type
        emotion_groups = {
            'excited': [], 'furious': [], 'terrified': [], 
            'fear': [], 'surprise': [], 'excitement': []
        }
        
        for item in self.vector_requests:
            filename = item['filename']
            if '_exc_' in filename:
                emotion_groups['excited'].append(item)
            elif '_fur_' in filename:
                emotion_groups['furious'].append(item)
            elif '_ter_' in filename:
                emotion_groups['terrified'].append(item)
            elif '_fea_' in filename:
                emotion_groups['fear'].append(item)
            elif '_sur_' in filename:
                emotion_groups['surprise'].append(item)
            elif '_exm_' in filename:
                emotion_groups['excitement'].append(item)
        
        # Process each emotion group
        for emotion_name, items in emotion_groups.items():
            if not items:
                continue
                
            print(f"\nProcessing {emotion_name} emotion vector ({len(items)} samples):")
            
            for i, item in enumerate(items):
                if i < 3 or i == len(items) - 1:  # Show first 3 and last
                    filename = item['filename']
                    request_data = item['request']
                    
                    print(f"  [{i+1}/{len(items)}] {filename}")
                    print(f"    Vector ID: {request_data.get('emotion_vector_id', 'N/A')[:8]}...")
                    
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
        print("Emotion Vector Generation Complete")
        print("="*70)
        print(f"Successfully generated: {success_count}/{len(self.vector_requests)}")
        
        if failed_samples:
            print(f"Failed samples: {len(failed_samples)}")
            for sample in failed_samples[:5]:
                print(f"  - {sample}")
        
        # Check generated files
        vector_files = []
        for pattern in ['*_exc_*', '*_fur_*', '*_ter_*', '*_fea_*', '*_sur_*', '*_exm_*']:
            vector_files.extend(list(self.output_dir.glob(pattern)))
        
        print(f"\nEmotion vector files in directory: {len(vector_files)}")
        
        return success_count == len(self.vector_requests)

def main():
    """Main execution following TDD approach"""
    
    # Get API endpoint from command line or environment
    api_endpoint = None
    if len(sys.argv) > 1:
        api_endpoint = sys.argv[1]
    
    generator = EmotionVectorGenerator(api_endpoint)
    
    # Step 1: Verify emotion vector format (Red phase - test)
    print("TDD Step 1: Testing emotion vector sample format...")
    if not generator.verify_emotion_vectors():
        print("Failed verification. Fix the generate_samples.py script.")
        return 1
    
    # Step 2: Generate emotion vectors (Green phase - implementation)
    print("\nTDD Step 2: Generating emotion vector samples...")
    if api_endpoint:
        print(f"Using API endpoint: {api_endpoint}")
    else:
        print("No API endpoint provided - generating mock files for testing")
    
    success = generator.generate_emotion_vectors()
    
    if success:
        print("\n✓ Emotion vector samples generated successfully!")
        print("\nNext step: Run verification script to check all 438 samples")
    else:
        print("\n✗ Some emotion vector samples failed to generate")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())