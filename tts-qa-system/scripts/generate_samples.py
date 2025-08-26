st#!/usr/bin/env python3
"""
Generate all TTS test samples with proper naming conventions
Total: 438 samples (6 reference + 432 variations)
"""

import json
import os
from pathlib import Path
import time
import requests
from typing import Dict, List, Tuple, Optional

class TTSSampleGenerator:
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.output_dir = Path(__file__).parent.parent / 'data' / 'voices'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configurations
        with open(config_dir / 'test_sentences.json', 'r', encoding='utf-8') as f:
            self.test_config = json.load(f)
        
        self.all_samples = []
        self.api_endpoint = None  # Will be set when provided
        
    def generate_filename(self, voice_id: str, emotion_name: str, 
                         match_type: str, scale: float = None,
                         is_reference: bool = False) -> str:
        """
        Generate filename according to naming rules from plan.md
        """
        if is_reference:
            # Reference: {voice_id}_ref_{emotion}.wav
            return f"{voice_id}_ref_{emotion_name}.wav"
        
        # Map emotion names to shorter versions for filenames
        emotion_short = {
            'angry': 'ang', 'sad': 'sad', 'happy': 'hap',
            'whisper': 'whi', 'toneup': 'tup', 'tonedown': 'tdn',
            'excited': 'exc', 'furious': 'fur', 'terrified': 'ter',
            'fear': 'fea', 'surprise': 'sur', 'excitement': 'exm'
        }.get(emotion_name, emotion_name[:3])
        
        # {voice_id}_{emotion}_{match_type}_scale_{scale}.wav
        if scale is not None:
            return f"{voice_id}_{emotion_short}_{match_type}_scale_{scale}.wav"
        return f"{voice_id}_{emotion_short}_{match_type}.wav"
    
    def create_api_request(self, text: str, voice_id: str, 
                          emotion_config: Dict, scale: float = 1.0) -> Dict:
        """
        Create API request payload
        """
        request = {
            "text": text,
            "actor_id": voice_id,
            "emotion_scale": scale,
            "tempo": 1,
            "pitch": 0,
            "lang": "en",  # Changed to English since sentences are in English
            "mode": "one-vocoder",
            "bp_c_l": True,
            "retake": True,
            "adjust_lastword": 0,
            "style_label_version": "v1"
        }
        
        # Handle style-based emotions
        if 'style_label' in emotion_config:
            request["style_label"] = emotion_config['style_label']
        
        # Handle emotion vector-based emotions
        elif 'emotion_vector_id' in emotion_config:
            request["style_label"] = "normal-1"
            request["emotion_vector_id"] = emotion_config['emotion_vector_id']
        
        # Reference case
        else:
            request["style_label"] = "normal-1"
        
        return request
    
    def generate_all_samples(self):
        """
        Generate all 438 samples according to the test matrix
        """
        samples = []
        
        voice_ids = self.test_config['voice_ids']
        scales = self.test_config['emotion_scales']
        
        # 1. Generate 6 reference samples (1 per voice per emotion category)
        print("\n=== Generating Reference Samples ===")
        ref_count = 0
        for voice_id in voice_ids:
            # One reference for style-based emotions
            samples.append({
                'filename': f"{voice_id}_ref_styles.wav",
                'voice_id': voice_id,
                'text': "This is a reference sample for voice calibration and testing.",
                'emotion_config': {},  # normal-1, no emotion
                'scale': 1.0,
                'type': 'reference'
            })
            ref_count += 1
            
            # One reference for audio-based emotions  
            samples.append({
                'filename': f"{voice_id}_ref_audio.wav",
                'voice_id': voice_id,
                'text': "This is a reference sample for audio-based emotion testing.",
                'emotion_config': {},  # normal-1, no emotion
                'scale': 1.0,
                'type': 'reference'
            })
            ref_count += 1
            
            # One reference for prompt-based emotions
            samples.append({
                'filename': f"{voice_id}_ref_prompt.wav",
                'voice_id': voice_id,
                'text': "This is a reference sample for prompt-based emotion testing.",
                'emotion_config': {},  # normal-1, no emotion
                'scale': 1.0,
                'type': 'reference'
            })
            ref_count += 1
        
        print(f"Reference samples: {ref_count}")
        
        # 2. Generate style-based variations (216 samples)
        # 6 styles × 3 sentence types × 6 scales × 2 voices = 216
        print("\n=== Generating Style-Based Variations ===")
        style_count = 0
        style_emotions = ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown']
        
        for voice_id in voice_ids:
            for emotion_name in style_emotions:
                emotion_config = self.test_config['emotions'][emotion_name]
                
                for match_type in ['match', 'neutral', 'opposite']:
                    text = emotion_config['sentences'][match_type]
                    
                    for scale in scales:
                        filename = self.generate_filename(
                            voice_id, emotion_name, match_type, scale
                        )
                        samples.append({
                            'filename': filename,
                            'voice_id': voice_id,
                            'text': text,
                            'emotion_config': emotion_config,
                            'scale': scale,
                            'type': 'style',
                            'emotion': emotion_name,
                            'match_type': match_type
                        })
                        style_count += 1
        
        print(f"Style-based variations: {style_count}")
        
        # 3. Generate emotion vector variations (216 samples)
        # 6 vectors × 3 sentence types × 6 scales × 2 voices = 216
        print("\n=== Generating Emotion Vector Variations ===")
        vector_count = 0
        vector_emotions = ['excited', 'furious', 'terrified', 'fear', 'surprise', 'excitement']
        
        for voice_id in voice_ids:
            for emotion_name in vector_emotions:
                emotion_config = self.test_config['emotions'][emotion_name]
                
                for match_type in ['match', 'neutral', 'opposite']:
                    text = emotion_config['sentences'][match_type]
                    
                    for scale in scales:
                        filename = self.generate_filename(
                            voice_id, emotion_name, match_type, scale
                        )
                        samples.append({
                            'filename': filename,
                            'voice_id': voice_id,
                            'text': text,
                            'emotion_config': emotion_config,
                            'scale': scale,
                            'type': emotion_config['type'],  # 'audio' or 'prompt'
                            'emotion': emotion_name,
                            'match_type': match_type
                        })
                        vector_count += 1
        
        print(f"Emotion vector variations: {vector_count}")
        
        # Summary
        total = ref_count + style_count + vector_count
        print(f"\n=== TOTAL SAMPLES: {total} ===")
        print(f"Expected: 438")
        print(f"Match: {'✓' if total == 438 else '✗'}")
        
        self.all_samples = samples
        return samples
    
    def save_sample_metadata(self):
        """
        Save metadata for all samples to JSON file
        """
        metadata_path = self.output_dir.parent / 'sample_metadata.json'
        
        metadata = {
            'total_samples': len(self.all_samples),
            'reference_samples': len([s for s in self.all_samples if s['type'] == 'reference']),
            'style_samples': len([s for s in self.all_samples if s['type'] == 'style']),
            'audio_vector_samples': len([s for s in self.all_samples if s['type'] == 'audio']),
            'prompt_vector_samples': len([s for s in self.all_samples if s['type'] == 'prompt']),
            'samples': self.all_samples
        }
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\nMetadata saved to: {metadata_path}")
    
    def generate_api_requests_file(self):
        """
        Generate a file with all API requests for review
        """
        requests_path = self.output_dir.parent / 'api_requests.json'
        
        api_requests = []
        for sample in self.all_samples:
            request = self.create_api_request(
                sample['text'],
                sample['voice_id'],
                sample['emotion_config'],
                sample['scale']
            )
            api_requests.append({
                'filename': sample['filename'],
                'request': request
            })
        
        with open(requests_path, 'w', encoding='utf-8') as f:
            json.dump(api_requests, f, indent=2, ensure_ascii=False)
        
        print(f"API requests saved to: {requests_path}")
        
        # Also create a sample of first 5 requests for review
        print("\n=== Sample API Requests (first 5) ===")
        for i, req in enumerate(api_requests[:5], 1):
            print(f"\n{i}. {req['filename']}:")
            print(json.dumps(req['request'], indent=2, ensure_ascii=False))
    
    def call_tts_api(self, request: Dict, filename: str) -> bool:
        """
        Call the TTS API and save the audio file
        Returns True if successful
        """
        if not self.api_endpoint:
            print(f"Skipping {filename}: No API endpoint configured")
            return False
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=request,
                timeout=30
            )
            response.raise_for_status()
            
            # Save audio file
            file_path = self.output_dir / filename
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Generated: {filename}")
            return True
            
        except Exception as e:
            print(f"✗ Failed {filename}: {str(e)}")
            return False
    
    def generate_with_api(self, api_endpoint: str, rate_limit: int = 10):
        """
        Generate all samples using the actual TTS API
        """
        self.api_endpoint = api_endpoint
        
        print(f"\n=== Starting TTS Generation ===")
        print(f"Endpoint: {api_endpoint}")
        print(f"Rate limit: {rate_limit} requests/second")
        print(f"Total samples: {len(self.all_samples)}")
        
        success_count = 0
        failed_samples = []
        
        for i, sample in enumerate(self.all_samples, 1):
            print(f"\n[{i}/{len(self.all_samples)}] Processing {sample['filename']}")
            
            request = self.create_api_request(
                sample['text'],
                sample['voice_id'],
                sample['emotion_config'],
                sample['scale']
            )
            
            if self.call_tts_api(request, sample['filename']):
                success_count += 1
            else:
                failed_samples.append(sample['filename'])
            
            # Rate limiting
            if i < len(self.all_samples):
                time.sleep(1.0 / rate_limit)
        
        # Summary
        print(f"\n=== Generation Complete ===")
        print(f"Success: {success_count}/{len(self.all_samples)}")
        if failed_samples:
            print(f"Failed samples: {len(failed_samples)}")
            for filename in failed_samples[:10]:  # Show first 10
                print(f"  - {filename}")

def main():
    """Main execution"""
    config_dir = Path(__file__).parent.parent / 'config'
    generator = TTSSampleGenerator(config_dir)
    
    # Generate all sample definitions
    samples = generator.generate_all_samples()
    
    # Save metadata
    generator.save_sample_metadata()
    
    # Generate API requests file for review
    generator.generate_api_requests_file()
    
    print("\n" + "="*70)
    print("Sample generation plan complete!")
    print("Next steps:")
    print("1. Review the generated files:")
    print("   - data/sample_metadata.json (all sample definitions)")
    print("   - data/api_requests.json (all API requests)")
    print("2. Set your API endpoint in the script")
    print("3. Run with --generate flag to actually generate audio files")
    
    # Check for command line argument to actually generate
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--generate':
        api_endpoint = input("\nEnter TTS API endpoint: ").strip()
        if api_endpoint:
            generator.generate_with_api(api_endpoint)
        else:
            print("No endpoint provided. Exiting.")

if __name__ == "__main__":
    main()