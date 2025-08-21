#!/usr/bin/env python3
"""
Flask server for TTS QA evaluation platform
Implements dynamic sampling - 25 samples per session from 438 total pool
"""

from flask import Flask, jsonify, request, send_from_directory, render_template_string
import json
import random
import uuid
from datetime import datetime
from pathlib import Path
import os

app = Flask(__name__)

# Configuration
DATA_DIR = Path(__file__).parent.parent / 'data'
VOICES_DIR = DATA_DIR / 'voices'
METADATA_FILE = DATA_DIR / 'sample_metadata.json'
RESULTS_FILE = DATA_DIR / 'results.jsonl'
SESSION_LOG_FILE = DATA_DIR / 'session_log.jsonl'

# Load sample metadata
def load_all_samples():
    """Load all 438 samples from metadata"""
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    return metadata['samples']

# Initialize samples on startup
ALL_SAMPLES = load_all_samples()
print(f"Loaded {len(ALL_SAMPLES)} samples")

@app.route('/')
def index():
    """Serve the main evaluation interface"""
    return send_from_directory('static', 'index.html')

@app.route('/api/get-session-samples')
def get_session_samples():
    """
    Dynamic sampling: Select 25 random samples from 438 for each session
    """
    # Generate new session ID
    session_id = str(uuid.uuid4())
    
    # Randomly select 25 samples from the full pool
    session_samples = random.sample(ALL_SAMPLES, min(25, len(ALL_SAMPLES)))
    
    # Add session-specific IDs for tracking
    for i, sample in enumerate(session_samples):
        sample['session_sample_id'] = f"{session_id}_{i}"
        sample['audio_url'] = f'/audio/{sample["filename"]}'
        
        # Add reference audio URL if applicable
        if sample['type'] == 'reference':
            sample['reference_url'] = None
        else:
            # Find appropriate reference for this voice
            voice_id = sample['voice_id']
            ref_type = 'styles' if sample['type'] == 'style' else sample['type']
            ref_filename = f"{voice_id}_ref_{ref_type}.wav"
            sample['reference_url'] = f'/audio/{ref_filename}'
    
    # Log session creation
    session_log = {
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'sample_count': len(session_samples),
        'sample_ids': [s['filename'] for s in session_samples]
    }
    
    # Save session log
    with open(SESSION_LOG_FILE, 'a') as f:
        json.dump(session_log, f)
        f.write('\n')
    
    return jsonify({
        'session_id': session_id,
        'samples': session_samples,
        'total': len(session_samples)
    })

@app.route('/api/save-result', methods=['POST'])
def save_result():
    """Save evaluation result for a single sample"""
    data = request.json
    
    # Add timestamp
    data['timestamp'] = datetime.now().isoformat()
    
    # Validate required fields
    required_fields = ['session_id', 'sample_id', 'scores']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate scores
    required_scores = ['quality', 'emotion', 'similarity']
    for score in required_scores:
        if score not in data['scores']:
            return jsonify({'error': f'Missing score: {score}'}), 400
        
        # Validate score range (1-7)
        score_value = data['scores'][score]
        if not isinstance(score_value, (int, float)) or score_value < 1 or score_value > 7:
            return jsonify({'error': f'Invalid score for {score}: must be 1-7'}), 400
    
    # Save to results file (JSONL format for easy appending)
    with open(RESULTS_FILE, 'a') as f:
        json.dump(data, f)
        f.write('\n')
    
    return jsonify({'status': 'success', 'message': 'Result saved'})

@app.route('/api/save-session', methods=['POST'])
def save_session():
    """Save complete session data"""
    data = request.json
    
    # Add completion timestamp
    data['completed_at'] = datetime.now().isoformat()
    
    # Save session completion
    session_complete_file = DATA_DIR / f"session_{data['session_id']}.json"
    with open(session_complete_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    return jsonify({
        'status': 'success',
        'message': 'Session saved',
        'file': str(session_complete_file)
    })

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    """Serve audio files from the voices directory"""
    return send_from_directory(VOICES_DIR, filename)

@app.route('/api/stats')
def get_stats():
    """Get current evaluation statistics"""
    stats = {
        'total_samples': len(ALL_SAMPLES),
        'sessions_completed': 0,
        'total_evaluations': 0,
        'coverage': {}
    }
    
    # Count evaluations per sample
    sample_eval_counts = {}
    
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    result = json.loads(line)
                    sample_id = result.get('sample_id', '')
                    sample_eval_counts[sample_id] = sample_eval_counts.get(sample_id, 0) + 1
                    stats['total_evaluations'] += 1
    
    # Calculate coverage statistics
    evaluated_samples = len(sample_eval_counts)
    stats['coverage'] = {
        'evaluated_samples': evaluated_samples,
        'unevaluated_samples': len(ALL_SAMPLES) - evaluated_samples,
        'percentage': round(evaluated_samples / len(ALL_SAMPLES) * 100, 1) if ALL_SAMPLES else 0,
        'avg_evals_per_sample': round(stats['total_evaluations'] / evaluated_samples, 2) if evaluated_samples > 0 else 0
    }
    
    # Count completed sessions
    if SESSION_LOG_FILE.exists():
        with open(SESSION_LOG_FILE, 'r') as f:
            stats['sessions_completed'] = sum(1 for line in f if line.strip())
    
    return jsonify(stats)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'samples_loaded': len(ALL_SAMPLES),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Ensure required directories exist
    DATA_DIR.mkdir(exist_ok=True)
    VOICES_DIR.mkdir(exist_ok=True)
    
    # Create empty results file if it doesn't exist
    if not RESULTS_FILE.exists():
        RESULTS_FILE.touch()
    if not SESSION_LOG_FILE.exists():
        SESSION_LOG_FILE.touch()
    
    print(f"Starting TTS QA Evaluation Server")
    print(f"Data directory: {DATA_DIR}")
    print(f"Voices directory: {VOICES_DIR}")
    print(f"Total samples available: {len(ALL_SAMPLES)}")
    print(f"Samples per session: 25")
    print(f"Server running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)