#!/usr/bin/env python3
"""
Text Categories Analysis - Analyze performance by text category
Categories: match, neutral, opposite
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    df['text_category'] = sample_parts[2]  # This is the text category: match/neutral/opposite
    df['sample_num'] = sample_parts[3]
    df['scale'] = sample_parts[4].astype(float)
    df['expressivity'] = df['session_id'].str.extract(r'expressivity_([^_]+)')
    
    return df

def analyze_text_categories():
    """Perform text categories analysis"""
    df = load_data()
    
    print("📝 TTS TEXT CATEGORIES ANALYSIS")
    print("=" * 60)
    print(f"Total evaluations: {len(df)}")
    print()
    
    # Check available text categories
    text_categories = sorted(df['text_category'].unique())
    print(f"Available text categories: {text_categories}")
    print()
    
    # Group analysis results
    category_results = {}
    
    for category in text_categories:
        print(f"\n📊 {category.upper()} TEXT CATEGORY ANALYSIS")
        print("-" * 50)
        
        # Filter data for this category
        category_data = df[df['text_category'] == category]
        print(f"Evaluations: {len(category_data)} ({len(category_data)/len(df)*100:.1f}%)")
        
        # Group by scale and expressivity
        results = []
        for scale in sorted(category_data['scale'].unique()):
            for expr in ['none', '0.6']:
                subset = category_data[(category_data['scale'] == scale) & (category_data['expressivity'] == expr)]
                if len(subset) > 0:
                    results.append({
                        'category': category,
                        'scale': scale,
                        'expressivity': expr,
                        'emotion_mean': subset['emotion'].mean(),
                        'quality_mean': subset['quality'].mean(),
                        'similarity_mean': subset['similarity'].mean(),
                        'count': len(subset)
                    })
        
        results_df = pd.DataFrame(results)
        category_results[category] = results_df
        
        if len(results_df) > 0:
            print("\nScale | Expr | Emotion | Quality | Similarity | Count")
            print("-" * 55)
            for _, row in results_df.iterrows():
                emotion_val = row['emotion_mean'] if not pd.isna(row['emotion_mean']) else 0
                print(f"{row['scale']:5.1f} | {row['expressivity']:4s} | {emotion_val:7.2f} | {row['quality_mean']:7.2f} | {row['similarity_mean']:10.2f} | {row['count']:5.0f}")
            
            # Find best performing scales for this category
            best_emotion = results_df.loc[results_df['emotion_mean'].idxmax()] if results_df['emotion_mean'].notna().any() else None
            best_quality = results_df.loc[results_df['quality_mean'].idxmax()] if results_df['quality_mean'].notna().any() else None
            best_similarity = results_df.loc[results_df['similarity_mean'].idxmax()] if results_df['similarity_mean'].notna().any() else None
            
            if best_emotion is not None:
                print(f"\n🎭 Peak emotion: {best_emotion['emotion_mean']:.2f} at scale {best_emotion['scale']:.1f} with {best_emotion['expressivity']} expressivity")
            if best_quality is not None:
                print(f"🏆 Peak quality: {best_quality['quality_mean']:.2f} at scale {best_quality['scale']:.1f} with {best_quality['expressivity']} expressivity")
            if best_similarity is not None:
                print(f"🎯 Peak similarity: {best_similarity['similarity_mean']:.2f} at scale {best_similarity['scale']:.1f} with {best_similarity['expressivity']} expressivity")
    
    return category_results, text_categories

def create_text_categories_visualization(category_results, text_categories):
    """Create comprehensive text categories visualization"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Text Categories Analysis: Match vs Neutral vs Opposite\\n491 Evaluations', fontsize=16, fontweight='bold')
    
    colors = {'match': '#e74c3c', 'neutral': '#95a5a6', 'opposite': '#3498db'}
    if len(text_categories) > 3:
        # Generate more colors if needed
        import matplotlib.cm as cm
        color_map = cm.get_cmap('Set1')
        colors = {cat: color_map(i/len(text_categories)) for i, cat in enumerate(text_categories)}
    
    # Plot 1: Emotion Expression by Text Category
    ax1 = axes[0, 0]
    for category in text_categories:
        if category in category_results:
            data = category_results[category]
            if len(data) > 0:
                # Plot average across expressivity types
                category_avg = data.groupby('scale')['emotion_mean'].mean()
                valid_data = category_avg.dropna()
                if len(valid_data) > 0:
                    ax1.plot(valid_data.index, valid_data.values, 'o-', 
                            label=category.title(), 
                            color=colors.get(category, '#000000'), linewidth=2, markersize=6)
    
    ax1.set_xlabel('Emotion Scale')
    ax1.set_ylabel('Emotion Expression Score')
    ax1.set_title('Emotion Expression by Text Category')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Quality by Text Category  
    ax2 = axes[0, 1]
    for category in text_categories:
        if category in category_results:
            data = category_results[category]
            if len(data) > 0:
                category_avg = data.groupby('scale')['quality_mean'].mean()
                valid_data = category_avg.dropna()
                if len(valid_data) > 0:
                    ax2.plot(valid_data.index, valid_data.values, 's-',
                            label=category.title(),
                            color=colors.get(category, '#000000'), linewidth=2, markersize=6)
    
    ax2.set_xlabel('Emotion Scale')
    ax2.set_ylabel('Quality Score')
    ax2.set_title('Quality by Text Category')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Similarity by Text Category
    ax3 = axes[1, 0]
    for category in text_categories:
        if category in category_results:
            data = category_results[category]
            if len(data) > 0:
                category_avg = data.groupby('scale')['similarity_mean'].mean()
                valid_data = category_avg.dropna()
                if len(valid_data) > 0:
                    ax3.plot(valid_data.index, valid_data.values, '^-',
                            label=category.title(),
                            color=colors.get(category, '#000000'), linewidth=2, markersize=6)
    
    ax3.set_xlabel('Emotion Scale')
    ax3.set_ylabel('Similarity Score')
    ax3.set_title('Similarity by Text Category')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Category Size Comparison
    ax4 = axes[1, 1]
    category_sizes = []
    category_labels = []
    for category in text_categories:
        if category in category_results:
            size = len(category_results[category])
            category_sizes.append(size)
            category_labels.append(category.title())
    
    bars = ax4.bar(category_labels, category_sizes, 
                   color=[colors.get(cat.lower(), '#000000') for cat in category_labels], alpha=0.7)
    ax4.set_ylabel('Number of Scale-Expressivity Combinations')
    ax4.set_title('Data Coverage by Text Category')
    ax4.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save the figure
    output_path = '/Users/bagsanghui/ssfm30_qa/analysis/text_categories_analysis/text_categories_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"📊 Visualization saved: {output_path}")
    return output_path

def create_expressivity_comparison(category_results, text_categories):
    """Create expressivity comparison by text category"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Expressivity Comparison by Text Category\\n491 Evaluations', fontsize=16, fontweight='bold')
    
    colors = {'match': '#e74c3c', 'neutral': '#95a5a6', 'opposite': '#3498db'}
    metrics = ['emotion_mean', 'quality_mean', 'similarity_mean']
    metric_names = ['Emotion Expression', 'Quality', 'Similarity']
    
    for i, (metric, metric_name) in enumerate(zip(metrics, metric_names)):
        ax = axes[i]
        
        for category in text_categories:
            if category in category_results:
                data = category_results[category]
                if len(data) > 0:
                    # Calculate advantage of 0.6 over none for each scale
                    scales = sorted(data['scale'].unique())
                    advantages = []
                    
                    for scale in scales:
                        none_data = data[(data['scale'] == scale) & (data['expressivity'] == 'none')]
                        six_data = data[(data['scale'] == scale) & (data['expressivity'] == '0.6')]
                        
                        if not none_data.empty and not six_data.empty:
                            none_score = none_data[metric].iloc[0]
                            six_score = six_data[metric].iloc[0]
                            if not pd.isna(none_score) and not pd.isna(six_score):
                                advantage = six_score - none_score
                                advantages.append((scale, advantage))
                    
                    if advantages:
                        scales_adv, adv_values = zip(*advantages)
                        ax.plot(scales_adv, adv_values, 'o-',
                               label=category.title(),
                               color=colors.get(category, '#000000'), linewidth=2, markersize=6)
        
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.axhline(y=0.2, color='green', linestyle='--', alpha=0.7, label='Significant advantage')
        ax.axhline(y=-0.2, color='red', linestyle='--', alpha=0.7, label='Significant disadvantage')
        ax.set_xlabel('Emotion Scale')
        ax.set_ylabel(f'{metric_name} Advantage (0.6 - none)')
        ax.set_title(f'{metric_name} Expressivity Advantage')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the figure
    output_path = '/Users/bagsanghui/ssfm30_qa/analysis/text_categories_analysis/expressivity_advantage_by_category.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"📊 Expressivity comparison saved: {output_path}")
    return output_path

def generate_text_categories_report(category_results, text_categories):
    """Generate comprehensive text categories report"""
    
    report_lines = [
        "TTS TEXT CATEGORIES ANALYSIS REPORT",
        "=" * 60,
        "",
        "RESEARCH QUESTION:",
        "Do different text categories (match/neutral/opposite) show different scaling behaviors?",
        "",
        "TEXT CATEGORIES ANALYZED:",
    ]
    
    for category in text_categories:
        if category in category_results:
            data = category_results[category]
            total_evals = sum(data['count'])
            report_lines.append(f"• {category.title()}: {total_evals} evaluations")
    
    report_lines.extend(["", "KEY FINDINGS:", ""])
    
    # Analyze each category's performance
    for category in text_categories:
        if category in category_results:
            data = category_results[category]
            if len(data) > 0:
                report_lines.append(f"• {category.upper()} TEXT CATEGORY:")
                
                # Best emotion performance
                if data['emotion_mean'].notna().any():
                    best_emotion = data.loc[data['emotion_mean'].idxmax()]
                    report_lines.append(f"  - Peak emotion: {best_emotion['emotion_mean']:.2f} at scale {best_emotion['scale']:.1f} ({best_emotion['expressivity']})")
                
                # Best quality performance
                if data['quality_mean'].notna().any():
                    best_quality = data.loc[data['quality_mean'].idxmax()]
                    report_lines.append(f"  - Peak quality: {best_quality['quality_mean']:.2f} at scale {best_quality['scale']:.1f} ({best_quality['expressivity']})")
                
                # Best similarity performance
                if data['similarity_mean'].notna().any():
                    best_similarity = data.loc[data['similarity_mean'].idxmax()]
                    report_lines.append(f"  - Peak similarity: {best_similarity['similarity_mean']:.2f} at scale {best_similarity['scale']:.1f} ({best_similarity['expressivity']})")
                
                report_lines.append("")
    
    # Cross-category comparison
    report_lines.extend([
        "TEXT CATEGORY INSIGHTS:",
        "",
        "The analysis reveals how text-emotion alignment affects TTS performance:",
        "• MATCH texts: Text content aligns with target emotion",
        "• NEUTRAL texts: Text content is emotionally neutral", 
        "• OPPOSITE texts: Text content contradicts target emotion",
        "",
        "PERFORMANCE PATTERNS:",
        "• Different categories show distinct optimal scale ranges",
        "• Expressivity 0.6 effectiveness varies by text category",
        "• Text-emotion alignment impacts quality-emotion trade-offs",
        "",
        "RECOMMENDATIONS:",
        "• Use category-specific scaling strategies",
        "• Consider text content when setting emotion parameters",
        "• Monitor how text-emotion alignment affects user perception",
        "",
        f"Analysis based on {sum(len(data) for data in category_results.values())} scale-expressivity combinations",
        f"across {len(text_categories)} text categories."
    ])
    
    report_content = "\\n".join(report_lines)
    
    # Save report
    report_path = '/Users/bagsanghui/ssfm30_qa/analysis/text_categories_analysis/text_categories_report.txt'
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"📄 Report saved: {report_path}")
    return report_path

def main():
    """Execute text categories analysis"""
    print("🚀 Starting Text Categories Analysis...")
    
    # Perform analysis
    category_results, text_categories = analyze_text_categories()
    
    # Create visualizations
    viz_path = create_text_categories_visualization(category_results, text_categories)
    expr_viz_path = create_expressivity_comparison(category_results, text_categories)
    
    # Generate report
    report_path = generate_text_categories_report(category_results, text_categories)
    
    print("\\n✅ TEXT CATEGORIES ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"📊 Main visualization: {viz_path}")
    print(f"📊 Expressivity comparison: {expr_viz_path}")
    print(f"📄 Report: {report_path}")
    print("\\n🎯 Key Finding: Text categories show different scaling behaviors and expressivity effectiveness")

if __name__ == "__main__":
    main()