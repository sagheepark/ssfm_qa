#!/usr/bin/env python3
"""
Quick test to see if basic analysis works
"""

import pandas as pd
import numpy as np
import json

def quick_test():
    """Quick test of basic functionality"""
    print("Loading data...")
    df = pd.read_csv('/Users/bagsanghui/ssfm30_qa/analysis/current_evaluations.csv')
    print(f"Loaded {len(df)} evaluations")
    
    # Parse scores
    def parse_scores_robust(score_str):
        try:
            cleaned = str(score_str).replace('""', '"')
            scores = json.loads(cleaned)
            return pd.Series({
                'quality': float(scores.get('quality', np.nan)),
                'emotion': float(scores.get('emotion', np.nan)),
                'similarity': float(scores.get('similarity', np.nan))
            })
        except:
            return pd.Series({'quality': np.nan, 'emotion': np.nan, 'similarity': np.nan})
    
    print("Parsing scores...")
    score_df = df['scores'].apply(parse_scores_robust)
    df = pd.concat([df, score_df], axis=1)
    
    # Extract variables
    sample_parts = df['sample_id'].str.split('_', expand=True)
    df['emotion_name'] = sample_parts[1]
    df['scale'] = sample_parts[4].astype(float)
    df['expressivity'] = df['session_id'].str.extract(r'expressivity_([^_]+)')
    
    # Define emotion groups
    emotion_labels = ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown']
    vector_first3 = ['excited', 'furious', 'terrified']
    vector_last3 = ['fear', 'surprise', 'excitement']
    
    print("Emotion distribution:")
    for group_name, emotions in [('Labels', emotion_labels), ('Vector_First3', vector_first3), ('Vector_Last3', vector_last3)]:
        count = df[df['emotion_name'].isin(emotions)].shape[0]
        print(f"  {group_name}: {count} evaluations")
    
    print("✅ Basic analysis working - emotion groups identified successfully")

if __name__ == "__main__":
    quick_test()