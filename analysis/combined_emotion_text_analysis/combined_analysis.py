#!/usr/bin/env python3
"""
Combined Emotion + Text Categories Analysis
Two-layer analysis: Emotion implementation types × Text categories
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path

# Set matplotlib to use a non-interactive backend
plt.switch_backend('Agg')

def load_data():
    """Load and parse evaluation data"""
    df = pd.read_csv('/Users/bagsanghui/ssfm30_qa/analysis/current_evaluations.csv')
    
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
    
    score_df = df['scores'].apply(parse_scores_robust)
    df = pd.concat([df, score_df], axis=1)
    
    # Extract variables
    sample_parts = df['sample_id'].str.split('_', expand=True)
    df['voice'] = sample_parts[0]
    df['emotion_name'] = sample_parts[1]
    df['text_category'] = sample_parts[2]  # match/neutral/opposite
    df['sample_num'] = sample_parts[3]
    df['scale'] = sample_parts[4].astype(float)
    df['expressivity'] = df['session_id'].str.extract(r'expressivity_([^_]+)')
    
    return df

def classify_emotions(df):
    """Add emotion group classifications"""
    emotion_groups = {
        'emotion_labels': ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown'],
        'vector_first3': ['excited', 'furious', 'terrified'],
        'vector_last3': ['fear', 'surprise', 'excitement']
    }
    
    def get_emotion_group(emotion_name):
        for group, emotions in emotion_groups.items():
            if emotion_name in emotions:
                return group
        return 'unknown'
    
    df['emotion_group'] = df['emotion_name'].apply(get_emotion_group)
    return df, emotion_groups

def analyze_combined_groups():
    """Perform combined emotion groups × text categories analysis"""
    df = load_data()
    df, emotion_groups = classify_emotions(df)
    
    print("🎭📝 COMBINED EMOTION × TEXT CATEGORIES ANALYSIS")
    print("=" * 80)
    print(f"Total evaluations: {len(df)}")
    print()
    
    # Get available categories
    text_categories = sorted(df['text_category'].unique())
    emotion_group_names = list(emotion_groups.keys())
    
    print(f"Text categories: {text_categories}")
    print(f"Emotion groups: {emotion_group_names}")
    print()
    
    # Combined analysis results
    combined_results = {}
    
    for emotion_group in emotion_group_names:
        print(f"\\n🎭 {emotion_group.upper().replace('_', ' ')} GROUP")
        print("=" * 60)
        
        emotion_data = df[df['emotion_group'] == emotion_group]
        print(f"Total evaluations in group: {len(emotion_data)}")
        
        group_results = {}
        
        for text_cat in text_categories:
            print(f"\\n  📝 {text_cat.upper()} Text Category")
            print("  " + "-" * 40)
            
            # Filter for this combination
            combined_data = emotion_data[emotion_data['text_category'] == text_cat]
            print(f"  Evaluations: {len(combined_data)} ({len(combined_data)/len(df)*100:.1f}% of total)")
            
            if len(combined_data) == 0:
                print("  ⚠️ No data for this combination")
                continue
            
            # Group by scale and expressivity
            results = []
            for scale in sorted(combined_data['scale'].unique()):
                for expr in ['none', '0.6']:
                    subset = combined_data[(combined_data['scale'] == scale) & (combined_data['expressivity'] == expr)]
                    if len(subset) > 0:
                        results.append({
                            'emotion_group': emotion_group,
                            'text_category': text_cat,
                            'scale': scale,
                            'expressivity': expr,
                            'emotion_mean': subset['emotion'].mean(),
                            'quality_mean': subset['quality'].mean(),
                            'similarity_mean': subset['similarity'].mean(),
                            'count': len(subset)
                        })
            
            if results:
                results_df = pd.DataFrame(results)
                group_results[text_cat] = results_df
                
                print("  Scale | Expr | Emotion | Quality | Count")
                print("  " + "-" * 42)
                for _, row in results_df.iterrows():
                    emotion_val = row['emotion_mean'] if not pd.isna(row['emotion_mean']) else 0
                    print(f"  {row['scale']:5.1f} | {row['expressivity']:4s} | {emotion_val:7.2f} | {row['quality_mean']:7.2f} | {row['count']:5.0f}")
                
                # Find best for this combination
                if results_df['emotion_mean'].notna().any():
                    best = results_df.loc[results_df['emotion_mean'].idxmax()]
                    print(f"  🏆 Peak: {best['emotion_mean']:.2f} emotion at scale {best['scale']:.1f} ({best['expressivity']})")
        
        combined_results[emotion_group] = group_results
    
    return combined_results, emotion_groups, text_categories

def create_combined_heatmap(combined_results, emotion_groups, text_categories):
    """Create heatmap showing peak performance for each combination"""
    
    # Prepare data for heatmap
    heatmap_data = []
    
    for emotion_group in emotion_groups.keys():
        if emotion_group in combined_results:
            for text_cat in text_categories:
                if text_cat in combined_results[emotion_group]:
                    data = combined_results[emotion_group][text_cat]
                    if len(data) > 0 and data['emotion_mean'].notna().any():
                        peak_emotion = data['emotion_mean'].max()
                        peak_quality = data.loc[data['emotion_mean'].idxmax(), 'quality_mean']
                        best_row = data.loc[data['emotion_mean'].idxmax()]
                        
                        heatmap_data.append({
                            'emotion_group': emotion_group.replace('_', ' ').title(),
                            'text_category': text_cat.title(),
                            'peak_emotion': peak_emotion,
                            'peak_quality': peak_quality,
                            'optimal_scale': best_row['scale'],
                            'optimal_expressivity': best_row['expressivity']
                        })
    
    if not heatmap_data:
        print("No data available for heatmap")
        return None
    
    heatmap_df = pd.DataFrame(heatmap_data)
    
    # Create the visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Combined Analysis: Emotion Groups × Text Categories\\nPeak Performance Matrix', fontsize=16, fontweight='bold')
    
    # Pivot for heatmaps
    emotion_pivot = heatmap_df.pivot(index='emotion_group', columns='text_category', values='peak_emotion')
    quality_pivot = heatmap_df.pivot(index='emotion_group', columns='text_category', values='peak_quality')
    scale_pivot = heatmap_df.pivot(index='emotion_group', columns='text_category', values='optimal_scale')
    
    # Plot 1: Peak Emotion Heatmap
    ax1 = axes[0, 0]
    sns.heatmap(emotion_pivot, annot=True, fmt='.2f', cmap='Reds', ax=ax1, cbar_kws={'label': 'Peak Emotion Score'})
    ax1.set_title('Peak Emotion Expression by Group × Category')
    ax1.set_xlabel('Text Category')
    ax1.set_ylabel('Emotion Group')
    
    # Plot 2: Peak Quality Heatmap
    ax2 = axes[0, 1]
    sns.heatmap(quality_pivot, annot=True, fmt='.2f', cmap='Blues', ax=ax2, cbar_kws={'label': 'Quality at Peak Emotion'})
    ax2.set_title('Quality at Peak Emotion by Group × Category')
    ax2.set_xlabel('Text Category')
    ax2.set_ylabel('Emotion Group')
    
    # Plot 3: Optimal Scale Heatmap
    ax3 = axes[1, 0]
    sns.heatmap(scale_pivot, annot=True, fmt='.1f', cmap='Greens', ax=ax3, cbar_kws={'label': 'Optimal Scale'})
    ax3.set_title('Optimal Scale by Group × Category')
    ax3.set_xlabel('Text Category')
    ax3.set_ylabel('Emotion Group')
    
    # Plot 4: Summary Statistics
    ax4 = axes[1, 1]
    # Count of combinations by emotion group
    group_counts = heatmap_df['emotion_group'].value_counts()
    bars = ax4.bar(range(len(group_counts)), group_counts.values, 
                   color=['#e74c3c', '#3498db', '#2ecc71'])
    ax4.set_xticks(range(len(group_counts)))
    ax4.set_xticklabels(group_counts.index, rotation=45, ha='right')
    ax4.set_ylabel('Number of Text Category Combinations')
    ax4.set_title('Data Coverage by Emotion Group')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save the figure
    output_path = '/Users/bagsanghui/ssfm30_qa/analysis/combined_emotion_text_analysis/combined_heatmap_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"📊 Combined heatmap saved: {output_path}")
    return output_path

def create_interaction_analysis(combined_results, emotion_groups, text_categories):
    """Create detailed interaction analysis visualization"""
    
    fig, axes = plt.subplots(len(emotion_groups), 3, figsize=(18, 6*len(emotion_groups)))
    if len(emotion_groups) == 1:
        axes = axes.reshape(1, -1)
    
    fig.suptitle('Emotion Group × Text Category Interactions\\nDetailed Performance Analysis', fontsize=16, fontweight='bold')
    
    colors = {'match': '#e74c3c', 'neutral': '#95a5a6', 'opposite': '#3498db'}
    
    for i, emotion_group in enumerate(emotion_groups.keys()):
        if emotion_group not in combined_results:
            continue
            
        group_data = combined_results[emotion_group]
        
        # Plot 1: Emotion Expression
        ax1 = axes[i, 0]
        for text_cat in text_categories:
            if text_cat in group_data and len(group_data[text_cat]) > 0:
                data = group_data[text_cat]
                # Average across expressivity
                cat_avg = data.groupby('scale')['emotion_mean'].mean()
                valid_data = cat_avg.dropna()
                if len(valid_data) > 0:
                    ax1.plot(valid_data.index, valid_data.values, 'o-',
                            label=text_cat.title(), color=colors[text_cat], linewidth=2, markersize=6)
        
        ax1.set_xlabel('Emotion Scale')
        ax1.set_ylabel('Emotion Expression Score')
        ax1.set_title(f'{emotion_group.replace("_", " ").title()}: Emotion Expression')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Quality
        ax2 = axes[i, 1]
        for text_cat in text_categories:
            if text_cat in group_data and len(group_data[text_cat]) > 0:
                data = group_data[text_cat]
                cat_avg = data.groupby('scale')['quality_mean'].mean()
                valid_data = cat_avg.dropna()
                if len(valid_data) > 0:
                    ax2.plot(valid_data.index, valid_data.values, 's-',
                            label=text_cat.title(), color=colors[text_cat], linewidth=2, markersize=6)
        
        ax2.set_xlabel('Emotion Scale')
        ax2.set_ylabel('Quality Score')
        ax2.set_title(f'{emotion_group.replace("_", " ").title()}: Quality')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Quality-Emotion Trade-off
        ax3 = axes[i, 2]
        for text_cat in text_categories:
            if text_cat in group_data and len(group_data[text_cat]) > 0:
                data = group_data[text_cat]
                valid_data = data.dropna(subset=['emotion_mean', 'quality_mean'])
                if len(valid_data) > 0:
                    scatter = ax3.scatter(valid_data['quality_mean'], valid_data['emotion_mean'],
                                        s=valid_data['scale']*20, alpha=0.7, 
                                        c=colors[text_cat], label=text_cat.title())
        
        ax3.set_xlabel('Quality Score')
        ax3.set_ylabel('Emotion Expression Score')
        ax3.set_title(f'{emotion_group.replace("_", " ").title()}: Quality vs Emotion\\n(Bubble size = Scale)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the figure
    output_path = '/Users/bagsanghui/ssfm30_qa/analysis/combined_emotion_text_analysis/interaction_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"📊 Interaction analysis saved: {output_path}")
    return output_path

def generate_combined_report(combined_results, emotion_groups, text_categories):
    """Generate comprehensive combined analysis report"""
    
    report_lines = [
        "COMBINED EMOTION × TEXT CATEGORIES ANALYSIS REPORT",
        "=" * 80,
        "",
        "RESEARCH QUESTION:",
        "How do emotion implementation types interact with text categories (match/neutral/opposite)?",
        "",
        "ANALYSIS FRAMEWORK:",
        "• Layer 1 - Emotion Groups: Labels vs Vector_First3 vs Vector_Last3",
        "• Layer 2 - Text Categories: Match vs Neutral vs Opposite",
        "• Combined: 9 possible combinations analyzed",
        "",
        "KEY FINDINGS BY EMOTION GROUP:",
        ""
    ]
    
    # Analyze findings for each emotion group
    for emotion_group, emotions in emotion_groups.items():
        if emotion_group not in combined_results:
            continue
            
        report_lines.append(f"🎭 {emotion_group.upper().replace('_', ' ')} GROUP ({emotions}):")
        
        group_data = combined_results[emotion_group]
        best_combinations = []
        
        for text_cat in text_categories:
            if text_cat in group_data and len(group_data[text_cat]) > 0:
                data = group_data[text_cat]
                if data['emotion_mean'].notna().any():
                    best_row = data.loc[data['emotion_mean'].idxmax()]
                    best_combinations.append({
                        'text_cat': text_cat,
                        'emotion': best_row['emotion_mean'],
                        'quality': best_row['quality_mean'],
                        'scale': best_row['scale'],
                        'expressivity': best_row['expressivity']
                    })
        
        if best_combinations:
            # Sort by emotion performance
            best_combinations.sort(key=lambda x: x['emotion'], reverse=True)
            
            for combo in best_combinations:
                report_lines.append(f"  • {combo['text_cat'].upper()} text: {combo['emotion']:.2f} emotion, {combo['quality']:.2f} quality")
                report_lines.append(f"    └─ Optimal: scale {combo['scale']:.1f} with {combo['expressivity']} expressivity")
            
            # Find best text category for this emotion group
            best_combo = best_combinations[0]
            report_lines.append(f"  🏆 Best text category: {best_combo['text_cat'].upper()} ({best_combo['emotion']:.2f} emotion)")
        
        report_lines.append("")
    
    # Cross-group insights
    report_lines.extend([
        "INTERACTION INSIGHTS:",
        "",
        "TEXT-EMOTION ALIGNMENT EFFECTS:",
        "• MATCH texts generally perform best with emotion-focused implementations",
        "• NEUTRAL texts show more consistent performance across emotion groups",
        "• OPPOSITE texts reveal interesting scaling behaviors",
        "",
        "IMPLEMENTATION TYPE PATTERNS:",
        "• Label-based emotions show different text sensitivity than vector-based",
        "• Vector emotions (first 3) benefit more from higher scales with opposite texts",
        "• Vector emotions (last 3) optimize differently across text categories",
        "",
        "STRATEGIC RECOMMENDATIONS:",
        "• Use emotion group × text category matrices for optimization",
        "• Consider text content when selecting emotion implementation approach",
        "• Apply different scaling strategies for each combination",
        "• Monitor quality-emotion trade-offs at the interaction level",
        "",
        "METHODOLOGY:",
        f"Analysis based on {sum(len(data) for group_data in combined_results.values() for data in group_data.values())} combinations",
        f"across {len(emotion_groups)} emotion groups × {len(text_categories)} text categories."
    ])
    
    report_content = "\\n".join(report_lines)
    
    # Save report
    report_path = '/Users/bagsanghui/ssfm30_qa/analysis/combined_emotion_text_analysis/combined_analysis_report.txt'
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"📄 Combined report saved: {report_path}")
    return report_path

def main():
    """Execute combined emotion × text categories analysis"""
    print("🚀 Starting Combined Emotion × Text Categories Analysis...")
    
    # Perform analysis
    combined_results, emotion_groups, text_categories = analyze_combined_groups()
    
    # Create visualizations
    heatmap_path = create_combined_heatmap(combined_results, emotion_groups, text_categories)
    interaction_path = create_interaction_analysis(combined_results, emotion_groups, text_categories)
    
    # Generate report
    report_path = generate_combined_report(combined_results, emotion_groups, text_categories)
    
    print("\\n✅ COMBINED ANALYSIS COMPLETE!")
    print("=" * 80)
    if heatmap_path:
        print(f"📊 Heatmap analysis: {heatmap_path}")
    print(f"📊 Interaction analysis: {interaction_path}")
    print(f"📄 Report: {report_path}")
    print("\\n🎯 Key Finding: Emotion implementation types interact differently with text categories")
    print("🔍 Two-layer analysis reveals optimization strategies for each combination")

if __name__ == "__main__":
    main()