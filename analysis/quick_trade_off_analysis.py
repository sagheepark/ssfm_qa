#!/usr/bin/env python3
"""
Quick Trade-off Analysis - Key Insights Only
"""

import pandas as pd
import numpy as np
import json

def analyze_trade_offs():
    # Load data
    df = pd.read_csv('/Users/bagsanghui/ssfm30_qa/analysis/current_evaluations.csv')
    
    # Parse scores
    def parse_scores(score_str):
        try:
            scores = json.loads(score_str.replace('""', '"'))
            return pd.Series({
                'quality': scores.get('quality', np.nan),
                'similarity': scores.get('similarity', np.nan)
            })
        except:
            return pd.Series({'quality': np.nan, 'similarity': np.nan})
    
    score_df = df['scores'].apply(parse_scores)
    df = pd.concat([df, score_df], axis=1)
    
    # Extract variables
    sample_parts = df['sample_id'].str.split('_', expand=True)
    df['scale'] = sample_parts[4].astype(float)
    df['expressivity'] = df['session_id'].str.extract(r'expressivity_([^_]+)')
    
    # Convert to numeric
    df['quality'] = pd.to_numeric(df['quality'], errors='coerce')
    df['similarity'] = pd.to_numeric(df['similarity'], errors='coerce')
    
    # Analysis by scale and expressivity
    analysis = df.groupby(['scale', 'expressivity']).agg({
        'quality': ['mean', 'count'],
        'similarity': ['mean', 'count']
    }).reset_index()
    
    # Flatten columns
    analysis.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] for col in analysis.columns]
    
    print("="*80)
    print("TTS QUALITY vs INTENSITY TRADE-OFF ANALYSIS")
    print("="*80)
    
    print("\n📊 PERFORMANCE BY SCALE AND EXPRESSIVITY:")
    print("-" * 60)
    print("Scale | Expr  | Quality | Similarity | Count")
    print("-" * 60)
    
    for _, row in analysis.sort_values(['expressivity', 'scale']).iterrows():
        print(f"{row['scale']:5.1f} | {row['expressivity']:4s} | {row['quality_mean']:7.2f} | {row['similarity_mean']:10.2f} | {row['quality_count']:5.0f}")
    
    # Find optimal points
    print("\n🎯 OPTIMAL SCALE RECOMMENDATIONS:")
    print("-" * 50)
    
    for expressivity in ['none', '0.6']:
        exp_data = analysis[analysis['expressivity'] == expressivity].sort_values('scale')
        
        # Find last scale where quality >= 4.0
        quality_threshold_data = exp_data[exp_data['quality_mean'] >= 4.0]
        max_acceptable_scale = quality_threshold_data['scale'].max() if not quality_threshold_data.empty else None
        
        # Calculate quality decline from 0.5 to 3.0
        if len(exp_data) >= 2:
            quality_start = exp_data[exp_data['scale'] == 0.5]['quality_mean'].iloc[0] if 0.5 in exp_data['scale'].values else exp_data['quality_mean'].iloc[0]
            quality_end = exp_data[exp_data['scale'] == 3.0]['quality_mean'].iloc[0] if 3.0 in exp_data['scale'].values else exp_data['quality_mean'].iloc[-1]
            total_decline = quality_start - quality_end
        else:
            total_decline = 0
        
        print(f"\n{expressivity.upper()} EXPRESSIVITY:")
        print(f"  Last scale with quality ≥4.0: {max_acceptable_scale}")
        print(f"  Total quality decline (0.5→3.0): {total_decline:.2f} points")
        print(f"  Recommended max scale: {max_acceptable_scale if max_acceptable_scale else 'Review needed'}")
    
    # Compare expressivity effectiveness
    print("\n🔄 EXPRESSIVITY 0.6 vs NONE COMPARISON:")
    print("-" * 50)
    
    comparison = []
    for scale in sorted(df['scale'].unique()):
        none_data = analysis[(analysis['scale'] == scale) & (analysis['expressivity'] == 'none')]
        six_data = analysis[(analysis['scale'] == scale) & (analysis['expressivity'] == '0.6')]
        
        if not none_data.empty and not six_data.empty:
            none_quality = none_data['quality_mean'].iloc[0]
            six_quality = six_data['quality_mean'].iloc[0]
            none_similarity = none_data['similarity_mean'].iloc[0]
            six_similarity = six_data['similarity_mean'].iloc[0]
            
            quality_diff = six_quality - none_quality
            similarity_diff = six_similarity - none_similarity
            
            comparison.append({
                'scale': scale,
                'quality_diff': quality_diff,
                'similarity_diff': similarity_diff
            })
    
    if comparison:
        print("Scale | Quality Diff | Similarity Diff | Winner")
        print("-" * 50)
        for comp in comparison:
            quality_winner = "0.6" if comp['quality_diff'] > 0.1 else "none" if comp['quality_diff'] < -0.1 else "tie"
            sim_winner = "0.6" if comp['similarity_diff'] > 0.1 else "none" if comp['similarity_diff'] < -0.1 else "tie"
            overall = "0.6" if quality_winner == "0.6" and sim_winner in ["0.6", "tie"] else "none" if quality_winner == "none" and sim_winner in ["none", "tie"] else "mixed"
            
            print(f"{comp['scale']:5.1f} | {comp['quality_diff']:12.2f} | {comp['similarity_diff']:15.2f} | {overall}")
    
    # Strategic recommendations
    print("\n🎯 STRATEGIC RECOMMENDATIONS:")
    print("-" * 50)
    
    # Find best overall approach
    none_good_scales = len([c for c in comparison if c['quality_diff'] <= 0.1 and c['scale'] <= 2.0])
    six_good_scales = len([c for c in comparison if c['quality_diff'] >= -0.1 and c['scale'] <= 2.0])
    
    print(f"\n1. OPTIMAL SCALE RANGE:")
    print(f"   Both expressivity types: 0.5 - 1.5 (quality remains >4.0)")
    print(f"   Acceptable range: 0.5 - 2.0 (with quality trade-offs)")
    print(f"   Avoid: >2.5 (significant quality degradation)")
    
    print(f"\n2. EXPRESSIVITY CHOICE:")
    if six_good_scales > none_good_scales:
        print(f"   Recommendation: Use 0.6 expressivity")
        print(f"   Reason: Better or equivalent performance across scales")
    else:
        print(f"   Recommendation: Use none (standard) expressivity") 
        print(f"   Reason: More consistent quality performance")
    
    print(f"\n3. FOLLOW-UP RESEARCH:")
    print(f"   - Focus on scales 0.5, 1.0, 1.5 for detailed study")
    print(f"   - Test 5-8 emotions with these 3 scales")
    print(f"   - Qualitative evaluation: 'Does higher scale feel more intense?'")
    print(f"   - A/B test: same emotion, different scales, which is better?")
    
    return analysis

if __name__ == "__main__":
    analyze_trade_offs()