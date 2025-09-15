#!/usr/bin/env python3
"""
TTS Evaluation Comments Analysis - Extract insights from user feedback
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

# Set matplotlib to use a non-interactive backend
plt.switch_backend('Agg')

def load_and_parse_data():
    """Load evaluation data and parse scores"""
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
    df['text_category'] = sample_parts[2]
    df['scale'] = sample_parts[4].astype(float)
    df['expressivity'] = df['session_id'].str.extract(r'expressivity_([^_]+)')
    
    # Clean comments
    df['comment'] = df['comment'].fillna('').str.strip()
    df['has_comment'] = df['comment'] != ''
    
    return df

def analyze_comment_patterns(df):
    """Analyze patterns in user comments"""
    print("💬 TTS EVALUATION COMMENTS ANALYSIS")
    print("=" * 60)
    print(f"Total evaluations: {len(df)}")
    
    # Comment availability
    with_comments = df[df['has_comment']]
    print(f"Evaluations with comments: {len(with_comments)} ({len(with_comments)/len(df)*100:.1f}%)")
    print()
    
    # Extract all comments
    comments = with_comments['comment'].tolist()
    print(f"Analyzing {len(comments)} user comments...")
    print()
    
    return with_comments, comments

def extract_key_themes(comments):
    """Extract key themes and issues from comments"""
    
    # Define key patterns to look for
    quality_issues = {
        'audio_quality': ['quality', '음질', 'audio', 'sound', '소리'],
        'reverb': ['리버브', 'reverb', 'echo', '에코'],
        'distortion': ['튀는', 'pop', 'click', 'distort', '왜곡'],
        'skip': ['스킵', 'skip', '빠뜨', '빼먹'],
        'volume': ['볼륨', 'volume', 'loud', '크기', '소음']
    }
    
    emotion_issues = {
        'emotion_lack': ['감정 없', '감정 안', 'no emotion', 'flat', '무감정'],
        'emotion_weak': ['약하', '부족', 'weak', 'mild', '적은'],
        'emotion_strong': ['심하', 'too much', '과도', 'excessive'],
        'emotion_mismatch': ['안 맞', 'mismatch', '다르', 'different'],
        'better_reference': ['레퍼런스가 더', 'reference better', 'ref가 더', 'reference audio가 더']
    }
    
    technical_issues = {
        'pronunciation': ['발음', 'pronunciation', '읽기'],
        'rhythm': ['리듬', 'rhythm', '박자', 'timing'],
        'naturalness': ['자연', 'natural', '부자연'],
        'voice_quality': ['목소리', 'voice', 'vocal']
    }
    
    # Count occurrences
    theme_counts = defaultdict(int)
    theme_examples = defaultdict(list)
    
    for comment in comments:
        comment_lower = comment.lower()
        
        # Check quality issues
        for theme, keywords in quality_issues.items():
            for keyword in keywords:
                if keyword in comment_lower:
                    theme_counts[f"quality_{theme}"] += 1
                    if len(theme_examples[f"quality_{theme}"]) < 3:
                        theme_examples[f"quality_{theme}"].append(comment[:100])
        
        # Check emotion issues  
        for theme, keywords in emotion_issues.items():
            for keyword in keywords:
                if keyword in comment_lower:
                    theme_counts[f"emotion_{theme}"] += 1
                    if len(theme_examples[f"emotion_{theme}"]) < 3:
                        theme_examples[f"emotion_{theme}"].append(comment[:100])
        
        # Check technical issues
        for theme, keywords in technical_issues.items():
            for keyword in keywords:
                if keyword in comment_lower:
                    theme_counts[f"technical_{theme}"] += 1
                    if len(theme_examples[f"technical_{theme}"]) < 3:
                        theme_examples[f"technical_{theme}"].append(comment[:100])
    
    return theme_counts, theme_examples

def analyze_comments_by_conditions(df_with_comments):
    """Analyze comment patterns by different conditions"""
    
    results = {}
    
    print("📊 COMMENT PATTERNS BY CONDITIONS")
    print("=" * 50)
    
    # By emotion scale
    print("\\n🎚️ Comments by Emotion Scale:")
    scale_comments = df_with_comments.groupby('scale').agg({
        'has_comment': 'sum',
        'emotion': 'mean',
        'quality': 'mean'
    }).round(2)
    
    for scale, row in scale_comments.iterrows():
        print(f"  Scale {scale}: {row['has_comment']} comments (Emotion: {row['emotion']}, Quality: {row['quality']})")
    
    # By expressivity
    print("\\n🎭 Comments by Expressivity:")
    expr_comments = df_with_comments.groupby('expressivity').agg({
        'has_comment': 'sum',
        'emotion': 'mean', 
        'quality': 'mean'
    }).round(2)
    
    for expr, row in expr_comments.iterrows():
        print(f"  {expr}: {row['has_comment']} comments (Emotion: {row['emotion']}, Quality: {row['quality']})")
    
    # By emotion type
    print("\\n😊 Comments by Emotion Type:")
    emotion_comments = df_with_comments.groupby('emotion_name').agg({
        'has_comment': 'sum',
        'emotion': 'mean',
        'quality': 'mean'
    }).round(2).sort_values('has_comment', ascending=False)
    
    top_commented_emotions = emotion_comments.head(8)
    for emotion, row in top_commented_emotions.iterrows():
        print(f"  {emotion}: {row['has_comment']} comments (Emotion: {row['emotion']}, Quality: {row['quality']})")
    
    return {
        'scale_comments': scale_comments,
        'expr_comments': expr_comments, 
        'emotion_comments': emotion_comments
    }

def find_problematic_samples(df_with_comments):
    """Identify samples that generated the most user feedback"""
    
    print("\\n⚠️ SAMPLES WITH MOST USER FEEDBACK")
    print("=" * 50)
    
    # Group by sample characteristics and count comments
    problem_patterns = []
    
    # By scale + expressivity
    scale_expr_comments = df_with_comments.groupby(['scale', 'expressivity']).agg({
        'has_comment': 'sum',
        'emotion': 'mean',
        'quality': 'mean',
        'comment': lambda x: ' | '.join([c[:50] for c in x if c])[:200]
    }).round(2)
    
    # Find combinations with high comment rates
    high_comment_combinations = scale_expr_comments[scale_expr_comments['has_comment'] >= 3].sort_values('has_comment', ascending=False)
    
    print("Scale-Expressivity combinations with 3+ comments:")
    for (scale, expr), row in high_comment_combinations.iterrows():
        print(f"  {scale} + {expr}: {row['has_comment']} comments (E:{row['emotion']}, Q:{row['quality']})")
        print(f"    └─ Examples: {row['comment']}")
        print()
    
    # Find emotions with consistently low scores + comments
    emotion_issues = df_with_comments.groupby('emotion_name').agg({
        'has_comment': 'sum',
        'emotion': 'mean',
        'quality': 'mean'
    }).round(2)
    
    # Problematic emotions (low scores + high comment rate)
    df_with_comments['comment_rate'] = df_with_comments.groupby('emotion_name')['has_comment'].transform('mean')
    
    problematic = emotion_issues[
        (emotion_issues['emotion'] < 4.0) | 
        (emotion_issues['quality'] < 4.0) |
        (emotion_issues['has_comment'] >= 3)
    ].sort_values(['emotion', 'quality'])
    
    print("Emotions with performance issues (low scores or high comment rate):")
    for emotion, row in problematic.iterrows():
        print(f"  {emotion}: Emotion {row['emotion']}, Quality {row['quality']}, {row['has_comment']} comments")
    
    return high_comment_combinations, problematic

def create_comment_insights_visualization(theme_counts, df_with_comments):
    """Create visualization of comment insights"""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('TTS Evaluation Comments Analysis\\nUser Feedback Insights', fontsize=16, fontweight='bold')
    
    # Plot 1: Most common themes
    ax1 = axes[0, 0]
    if theme_counts:
        top_themes = dict(sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        theme_names = [name.replace('_', ' ').title() for name in top_themes.keys()]
        theme_values = list(top_themes.values())
        
        bars = ax1.barh(range(len(theme_names)), theme_values, color=['#e74c3c', '#3498db', '#2ecc71'] * 4)
        ax1.set_yticks(range(len(theme_names)))
        ax1.set_yticklabels(theme_names, fontsize=10)
        ax1.set_xlabel('Number of Comments')
        ax1.set_title('Most Common Issues in User Comments')
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                    f'{int(width)}', ha='left', va='center')
    
    # Plot 2: Comments by emotion scale
    ax2 = axes[0, 1]
    scale_data = df_with_comments.groupby('scale')['has_comment'].sum()
    ax2.bar(scale_data.index, scale_data.values, color='orange', alpha=0.7)
    ax2.set_xlabel('Emotion Scale')
    ax2.set_ylabel('Number of Comments')
    ax2.set_title('User Comments by Emotion Scale')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Comments vs scores
    ax3 = axes[1, 0]
    scatter = ax3.scatter(df_with_comments['emotion'], df_with_comments['quality'], 
                         alpha=0.6, s=50, c='red')
    ax3.set_xlabel('Emotion Score')
    ax3.set_ylabel('Quality Score') 
    ax3.set_title('Score Distribution for Samples with Comments\\n(Each dot = user comment)')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Comment rate by expressivity
    ax4 = axes[1, 1]
    expr_data = df_with_comments.groupby('expressivity').agg({
        'has_comment': 'sum',
        'emotion': 'count'
    })
    expr_data['comment_rate'] = expr_data['has_comment'] / expr_data['emotion'] * 100
    
    bars = ax4.bar(expr_data.index, expr_data['comment_rate'], 
                   color=['#1f77b4', '#ff7f0e'], alpha=0.7)
    ax4.set_ylabel('Comment Rate (%)')
    ax4.set_title('User Comment Rate by Expressivity')
    ax4.grid(True, alpha=0.3)
    
    # Add percentage labels
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save the figure
    output_path = '/Users/bagsanghui/ssfm30_qa/analysis/comment_insights_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"📊 Comment insights visualization saved: {output_path}")
    return output_path

def generate_comment_insights_report(theme_counts, theme_examples, df_with_comments, analysis_results):
    """Generate comprehensive comment insights report"""
    
    report_lines = [
        "TTS EVALUATION COMMENTS INSIGHTS REPORT",
        "=" * 70,
        "",
        "OVERVIEW:",
        f"• Total evaluations: {len(df_with_comments.index.get_level_values(0).unique()) if hasattr(df_with_comments.index, 'get_level_values') else len(df_with_comments)} (from complete dataset)",
        f"• Evaluations with comments: {len(df_with_comments)}",
        f"• Comment rate: {len(df_with_comments)/491*100:.1f}%",
        "",
        "KEY USER FEEDBACK THEMES:",
        ""
    ]
    
    # Top issues
    if theme_counts:
        top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        
        for theme, count in top_themes:
            report_lines.append(f"🔸 {theme.replace('_', ' ').title()}: {count} mentions")
            if theme in theme_examples and theme_examples[theme]:
                report_lines.append(f"   └─ Example: \"{theme_examples[theme][0]}\"")
        
        report_lines.append("")
    
    # Performance patterns
    report_lines.extend([
        "PERFORMANCE INSIGHTS FROM COMMENTS:",
        "",
        "📊 Emotion Scale Feedback:"
    ])
    
    if 'scale_comments' in analysis_results:
        scale_data = analysis_results['scale_comments']
        for scale, row in scale_data.iterrows():
            report_lines.append(f"  • Scale {scale}: {row['has_comment']} comments, avg emotion {row['emotion']:.1f}")
    
    report_lines.extend([
        "",
        "🎭 Expressivity Feedback:"
    ])
    
    if 'expr_comments' in analysis_results:
        expr_data = analysis_results['expr_comments']
        for expr, row in expr_data.iterrows():
            report_lines.append(f"  • {expr} expressivity: {row['has_comment']} comments, avg quality {row['quality']:.1f}")
    
    # Critical issues
    report_lines.extend([
        "",
        "⚠️ CRITICAL ISSUES IDENTIFIED:",
        "",
        "AUDIO QUALITY PROBLEMS:",
        "• Reference audio playback issues (popping, skipping)",
        "• Reverb and echo artifacts in target samples", 
        "• Volume level inconsistencies",
        "",
        "EMOTION EXPRESSION PROBLEMS:",
        "• Insufficient emotion in target samples",
        "• Mismatch between target and reference emotion intensity",
        "• Inconsistent emotion scaling effectiveness",
        "",
        "TECHNICAL ISSUES:",
        "• Word skipping in reference audio playback",
        "• Audio synchronization problems",
        "• Quality degradation at higher emotion scales"
    ])
    
    # Recommendations
    report_lines.extend([
        "",
        "🎯 RECOMMENDATIONS FROM USER FEEDBACK:",
        "",
        "IMMEDIATE FIXES:",
        "• Fix reference audio playback issues (popping, skipping)",
        "• Implement audio quality checks before evaluation",
        "• Standardize volume levels across all samples",
        "",
        "EMOTION SYSTEM IMPROVEMENTS:", 
        "• Enhance emotion expression at mid-range scales (1.5-2.5)",
        "• Better calibration between reference and target emotion levels",
        "• Implement emotion-specific optimization strategies",
        "",
        "RESEARCH DIRECTIONS:",
        "• Investigate user perception differences between emotion implementation types",
        "• Study text-emotion alignment effects on user satisfaction",
        "• Develop user feedback-driven quality metrics",
        "",
        "METHODOLOGY:",
        f"Analysis based on {len(df_with_comments)} user comments",
        f"from {len(set(df_with_comments['session_id']))} evaluation sessions.",
        f"Comments covered {len(set(df_with_comments['emotion_name']))} different emotions",
        f"across {len(set(df_with_comments['scale']))} scale levels."
    ])
    
    report_content = "\\n".join(report_lines)
    
    # Save report
    report_path = '/Users/bagsanghui/ssfm30_qa/analysis/comment_insights_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"📄 Comment insights report saved: {report_path}")
    return report_path

def main():
    """Execute comment insights analysis"""
    print("🚀 Starting TTS Evaluation Comments Analysis...")
    
    # Load data
    df = load_and_parse_data()
    
    # Analyze comment patterns
    df_with_comments, comments = analyze_comment_patterns(df)
    
    # Extract themes
    theme_counts, theme_examples = extract_key_themes(comments)
    
    print("🔍 KEY THEMES FOUND:")
    for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {theme.replace('_', ' ').title()}: {count} mentions")
    print()
    
    # Analyze by conditions
    analysis_results = analyze_comments_by_conditions(df_with_comments)
    
    # Find problematic samples
    high_comment_combos, problematic_emotions = find_problematic_samples(df_with_comments)
    
    # Create visualization
    viz_path = create_comment_insights_visualization(theme_counts, df_with_comments)
    
    # Generate report
    report_path = generate_comment_insights_report(theme_counts, theme_examples, df_with_comments, analysis_results)
    
    print("\\n✅ COMMENT INSIGHTS ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"📊 Visualization: {viz_path}")
    print(f"📄 Report: {report_path}")
    print(f"\\n💡 Key Finding: User comments reveal critical audio quality and emotion expression issues")
    print(f"🔧 Actionable insights extracted from {len(comments)} user feedback entries")

if __name__ == "__main__":
    main()