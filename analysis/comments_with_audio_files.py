#!/usr/bin/env python3
"""
Extract comments with corresponding audio file names for raw materials
"""

import pandas as pd
import numpy as np
import json

def extract_comments_with_files():
    """Extract all comments with corresponding audio file information"""
    
    df = pd.read_csv('/Users/bagsanghui/ssfm30_qa/analysis/current_evaluations.csv')
    
    # We don't need to parse scores for this raw material extraction
    
    # Extract sample information
    sample_parts = df['sample_id'].str.split('_', expand=True)
    df['voice'] = sample_parts[0]
    df['emotion_name'] = sample_parts[1]
    df['text_category'] = sample_parts[2]
    df['sample_num'] = sample_parts[3]
    df['scale'] = sample_parts[4]
    df['expressivity'] = df['session_id'].str.extract(r'expressivity_([^_]+)')
    
    # Filter only rows with comments
    df_with_comments = df[df['comment'].notna() & (df['comment'].str.strip() != '')]
    
    # Create raw materials file
    raw_materials = []
    
    for idx, row in df_with_comments.iterrows():
        # Construct likely audio file names (both reference and target)
        base_filename = f"{row['voice']}_{row['emotion_name']}_{row['text_category']}_{row['sample_num']}"
        reference_file = f"{base_filename}_ref.wav"  # Likely reference file name
        target_file = f"{base_filename}_scale_{row['scale']}.wav"  # Likely target file name
        
        raw_materials.append({
            'sample_id': row['sample_id'],
            'session_type': f"expressivity_{row['expressivity']}",
            'emotion': row['emotion_name'],
            'text_category': row['text_category'],
            'scale': row['scale'],
            'reference_audio_file': reference_file,
            'target_audio_file': target_file,
            'user_comment': row['comment'],
            'timestamp': row['timestamp'],
            'evaluation_duration_ms': row.get('duration_ms', 'N/A')
        })
    
    # Save as CSV for easy reference
    raw_df = pd.DataFrame(raw_materials)
    output_path = '/Users/bagsanghui/ssfm30_qa/analysis/comments_with_audio_filenames.csv'
    raw_df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Raw materials saved: {output_path}")
    print(f"Total comments with audio file references: {len(raw_materials)}")
    
    return output_path, raw_materials

if __name__ == "__main__":
    extract_comments_with_files()