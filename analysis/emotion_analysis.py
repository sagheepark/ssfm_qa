#!/usr/bin/env python3
"""
Emotion Expression Analysis - Extract and visualize emotion scores vs scale
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import re

def load_and_parse_emotion_data():
    """Load data and properly parse all scores including emotion"""
    df = pd.read_csv('/Users/bagsanghui/ssfm30_qa/analysis/current_evaluations.csv')
    
    print(f"Loaded {len(df)} evaluations")
    
    # Parse JSON scores more robustly
    def parse_scores_robust(score_str):
        try:
            # Handle the double quote escaping
            if pd.isna(score_str):
                return pd.Series({'quality': np.nan, 'emotion': np.nan, 'similarity': np.nan})
            
            # Clean up the string
            cleaned = str(score_str).replace('""', '"')
            scores = json.loads(cleaned)
            
            return pd.Series({
                'quality': float(scores.get('quality', np.nan)) if scores.get('quality') is not None else np.nan,
                'emotion': float(scores.get('emotion', np.nan)) if scores.get('emotion') is not None else np.nan,
                'similarity': float(scores.get('similarity', np.nan)) if scores.get('similarity') is not None else np.nan
            })
        except Exception as e:
            print(f"Error parsing: {score_str[:100]}... Error: {e}")
            return pd.Series({'quality': np.nan, 'emotion': np.nan, 'similarity': np.nan})
    
    # Apply parsing
    score_df = df['scores'].apply(parse_scores_robust)
    df = pd.concat([df, score_df], axis=1)
    
    # Extract variables
    sample_parts = df['sample_id'].str.split('_', expand=True)
    df['voice'] = sample_parts[0]
    df['emotion_type'] = sample_parts[1] 
    df['text_type'] = sample_parts[2]
    df['scale'] = sample_parts[4].astype(float)
    df['expressivity'] = df['session_id'].str.extract(r'expressivity_([^_]+)')
    
    # Check emotion data availability
    emotion_valid = df['emotion'].notna().sum()
    print(f"Valid emotion scores: {emotion_valid} out of {len(df)} ({emotion_valid/len(df)*100:.1f}%)")
    
    return df

def analyze_emotion_vs_scale(df):
    """Analyze emotion expression scores vs scale for each expressivity"""
    print("\n=== EMOTION EXPRESSION vs SCALE ANALYSIS ===")
    
    # Group by scale and expressivity
    emotion_analysis = df.groupby(['scale', 'expressivity']).agg({
        'emotion': ['mean', 'std', 'count'],
        'quality': ['mean', 'std', 'count'],  
        'similarity': ['mean', 'std', 'count']
    }).reset_index()
    
    # Flatten column names
    emotion_analysis.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] for col in emotion_analysis.columns]
    
    print("\nEmotion Expression by Scale and Expressivity:")
    print("=" * 60)
    print("Scale | Expr  | Emotion | Quality | Similarity | Count")
    print("=" * 60)
    
    for _, row in emotion_analysis.sort_values(['expressivity', 'scale']).iterrows():
        emotion_mean = row['emotion_mean'] if not pd.isna(row['emotion_mean']) else 0
        print(f"{row['scale']:5.1f} | {row['expressivity']:4s} | {emotion_mean:7.2f} | {row['quality_mean']:7.2f} | {row['similarity_mean']:10.2f} | {row['emotion_count']:5.0f}")
    
    return emotion_analysis

def find_meaningful_scale_range(emotion_analysis):
    """Find the scale range where emotion expression is meaningful"""
    print("\n=== MEANINGFUL SCALE RANGE ANALYSIS ===")
    
    for expressivity in ['none', '0.6']:
        exp_data = emotion_analysis[emotion_analysis['expressivity'] == expressivity].sort_values('scale')
        
        if len(exp_data) == 0:
            continue
            
        print(f"\n{expressivity.upper()} EXPRESSIVITY:")
        print("-" * 30)
        
        # Calculate emotion improvement per scale unit
        scales = exp_data['scale'].values
        emotion_scores = exp_data['emotion_mean'].values
        
        # Remove NaN values
        valid_indices = ~np.isnan(emotion_scores)
        if np.sum(valid_indices) < 2:
            print("  Insufficient emotion data for analysis")
            continue
            
        valid_scales = scales[valid_indices]
        valid_emotions = emotion_scores[valid_indices]
        
        # Calculate improvement rates
        improvements = []
        for i in range(1, len(valid_emotions)):
            improvement = (valid_emotions[i] - valid_emotions[i-1]) / (valid_scales[i] - valid_scales[i-1])
            improvements.append(improvement)
            scale_range = f"{valid_scales[i-1]:.1f} → {valid_scales[i]:.1f}"
            print(f"  {scale_range}: {improvement:+.3f} emotion points per scale unit")
        
        avg_improvement = np.mean(improvements) if improvements else 0
        print(f"  Average improvement: {avg_improvement:+.3f} emotion points per scale unit")
        
        # Find where improvement becomes minimal (< 0.1 per scale unit)
        meaningful_cutoff = None
        for i, improvement in enumerate(improvements):
            if improvement < 0.1:  # Less than 0.1 point improvement per scale
                meaningful_cutoff = valid_scales[i]
                break
        
        if meaningful_cutoff:
            print(f"  🎯 Meaningful scaling stops at: {meaningful_cutoff:.1f}")
        else:
            print(f"  🎯 Emotion scaling remains meaningful throughout range")
        
        # Find peak emotion score
        peak_idx = np.argmax(valid_emotions)
        peak_scale = valid_scales[peak_idx]
        peak_score = valid_emotions[peak_idx]
        print(f"  📈 Peak emotion expression: {peak_score:.2f} at scale {peak_scale:.1f}")

def create_emotion_scale_visualization(df, emotion_analysis):
    """Create comprehensive emotion vs scale visualization"""
    print("\n=== CREATING EMOTION vs SCALE VISUALIZATION ===")
    
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('TTS Emotion Expression vs Scale Analysis\n491 Evaluations - Finding Meaningful Scale Ranges', fontsize=16)
    
    # Plot 1: Emotion Expression vs Scale
    ax1 = axes[0, 0]
    for expressivity in ['none', '0.6']:
        data = emotion_analysis[emotion_analysis['expressivity'] == expressivity]
        valid_data = data.dropna(subset=['emotion_mean'])
        
        if len(valid_data) > 0:
            ax1.plot(valid_data['scale'], valid_data['emotion_mean'], 'o-', 
                    label=f'Expressivity {expressivity}', linewidth=3, markersize=8)
            
            # Add error bars
            ax1.errorbar(valid_data['scale'], valid_data['emotion_mean'], 
                        yerr=valid_data['emotion_std']/2, alpha=0.3, capsize=5)
    
    ax1.axhline(y=4.0, color='red', linestyle='--', alpha=0.7, label='Midpoint (4.0)')
    ax1.set_xlabel('Emotion Scale')
    ax1.set_ylabel('Emotion Expression Score (1-7)')
    ax1.set_title('Emotion Expression vs Scale')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Emotion Improvement Rate
    ax2 = axes[0, 1]
    
    for expressivity in ['none', '0.6']:
        data = emotion_analysis[emotion_analysis['expressivity'] == expressivity].sort_values('scale')
        valid_data = data.dropna(subset=['emotion_mean'])
        
        if len(valid_data) > 1:
            scales = valid_data['scale'].values
            emotions = valid_data['emotion_mean'].values
            
            # Calculate improvement rates
            improvement_rates = []
            scale_midpoints = []
            
            for i in range(1, len(emotions)):
                rate = (emotions[i] - emotions[i-1]) / (scales[i] - scales[i-1])
                improvement_rates.append(rate)
                scale_midpoints.append((scales[i] + scales[i-1]) / 2)
            
            ax2.bar([s + (-0.1 if expressivity == 'none' else 0.1) for s in scale_midpoints], 
                   improvement_rates, width=0.2, alpha=0.7,
                   label=f'Expressivity {expressivity}')
    
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.axhline(y=0.1, color='green', linestyle='--', alpha=0.7, label='Meaningful threshold')
    ax2.set_xlabel('Scale Midpoint')
    ax2.set_ylabel('Emotion Improvement per Scale Unit')
    ax2.set_title('Emotion Improvement Rate vs Scale')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Quality vs Emotion Trade-off by Scale
    ax3 = axes[1, 0]
    colors = {'none': 'blue', '0.6': 'orange'}
    
    for expressivity in ['none', '0.6']:
        data = emotion_analysis[emotion_analysis['expressivity'] == expressivity]
        valid_data = data.dropna(subset=['emotion_mean', 'quality_mean'])
        
        if len(valid_data) > 0:
            scatter = ax3.scatter(valid_data['quality_mean'], valid_data['emotion_mean'], 
                                s=valid_data['scale']*30, alpha=0.7, 
                                c=colors[expressivity], label=f'Expressivity {expressivity}')
            
            # Add scale labels
            for _, row in valid_data.iterrows():
                ax3.annotate(f"{row['scale']:.1f}", 
                           (row['quality_mean'], row['emotion_mean']),
                           xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    ax3.set_xlabel('Quality Score')
    ax3.set_ylabel('Emotion Expression Score')
    ax3.set_title('Quality vs Emotion Trade-off\n(Bubble size = Scale)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Expressivity Comparison
    ax4 = axes[1, 1]
    
    # Calculate differences (0.6 - none) for each scale
    scales_all = sorted(df['scale'].unique())
    emotion_diffs = []
    quality_diffs = []
    
    for scale in scales_all:
        none_data = emotion_analysis[(emotion_analysis['scale'] == scale) & (emotion_analysis['expressivity'] == 'none')]
        six_data = emotion_analysis[(emotion_analysis['scale'] == scale) & (emotion_analysis['expressivity'] == '0.6')]
        
        if not none_data.empty and not six_data.empty:
            emotion_diff = six_data['emotion_mean'].iloc[0] - none_data['emotion_mean'].iloc[0]
            quality_diff = six_data['quality_mean'].iloc[0] - none_data['quality_mean'].iloc[0]
            
            if not pd.isna(emotion_diff):
                emotion_diffs.append((scale, emotion_diff))
            quality_diffs.append((scale, quality_diff))
    
    if emotion_diffs:
        scales_emotion, diffs_emotion = zip(*emotion_diffs)
        ax4.bar([s - 0.1 for s in scales_emotion], diffs_emotion, 0.2, 
               label='Emotion Diff', color='purple', alpha=0.7)
    
    if quality_diffs:
        scales_quality, diffs_quality = zip(*quality_diffs)
        ax4.bar([s + 0.1 for s in scales_quality], diffs_quality, 0.2,
               label='Quality Diff', color='green', alpha=0.7)
    
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax4.axhline(y=0.2, color='green', linestyle='--', alpha=0.7, label='Significant advantage')
    ax4.axhline(y=-0.2, color='red', linestyle='--', alpha=0.7, label='Significant disadvantage')
    ax4.set_xlabel('Emotion Scale')
    ax4.set_ylabel('Score Difference (0.6 - none)')
    ax4.set_title('Expressivity 0.6 vs None Comparison')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/bagsanghui/ssfm30_qa/analysis/emotion_scale_analysis.png', 
               dpi=300, bbox_inches='tight')
    plt.show()
    
    print("📊 Emotion analysis saved to: emotion_scale_analysis.png")

def main():
    """Execute emotion analysis"""
    df = load_and_parse_emotion_data()
    emotion_analysis = analyze_emotion_vs_scale(df)
    find_meaningful_scale_range(emotion_analysis)
    create_emotion_scale_visualization(df, emotion_analysis)

if __name__ == "__main__":
    main()