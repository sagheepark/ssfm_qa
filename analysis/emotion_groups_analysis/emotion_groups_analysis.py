#!/usr/bin/env python3
"""
TTS Emotion Groups Analysis - Separate analysis by emotion implementation type

Groups:
1. Emotion Labels (6): angry, sad, happy, whisper, toneup, tonedown
2. Emotion Vectors - First 3: excited, furious, terrified  
3. Emotion Vectors - Last 3: fear, surprise, excitement

Goal: Understand if different emotion features show different scaling behaviors
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path

class EmotionGroupsAnalyzer:
    def __init__(self, csv_path):
        """Initialize with evaluation data"""
        self.output_dir = Path('/Users/bagsanghui/ssfm30_qa/analysis/emotion_groups_analysis')
        self.data = self.load_and_parse_data(csv_path)
        self.prepare_emotion_groups()
        
    def load_and_parse_data(self, csv_path):
        """Load CSV and parse JSON scores"""
        df = pd.read_csv(csv_path)
        
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
        df['text_type'] = sample_parts[2]
        df['scale'] = sample_parts[4].astype(float)
        df['expressivity'] = df['session_id'].str.extract(r'expressivity_([^_]+)')
        
        print(f"Loaded {len(df)} evaluations")
        return df
    
    def prepare_emotion_groups(self):
        """Categorize emotions into groups based on implementation type"""
        # Define emotion groups
        self.emotion_groups = {
            'emotion_labels': ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown'],
            'vector_first3': ['excited', 'furious', 'terrified'],
            'vector_last3': ['fear', 'surprise', 'excitement']
        }
        
        # Add emotion group to dataframe
        def categorize_emotion(emotion_name):
            for group, emotions in self.emotion_groups.items():
                if emotion_name in emotions:
                    return group
            return 'unknown'
        
        self.data['emotion_group'] = self.data['emotion_name'].apply(categorize_emotion)
        
        # Print group statistics
        print("\n=== EMOTION GROUP STATISTICS ===")
        for group, emotions in self.emotion_groups.items():
            count = len(self.data[self.data['emotion_group'] == group])
            print(f"{group.upper()}: {count} evaluations")
            print(f"  Emotions: {emotions}")
        
        print(f"\nTotal known emotions: {len(self.data[self.data['emotion_group'] != 'unknown'])}")
        print(f"Unknown emotions: {len(self.data[self.data['emotion_group'] == 'unknown'])}")
    
    def analyze_groups_by_scale(self):
        """Analyze each emotion group's performance across scales"""
        print("\n=== EMOTION GROUPS vs SCALE ANALYSIS ===")
        
        results = []
        for scale in sorted(self.data['scale'].unique()):
            for expr in ['none', '0.6']:
                for group in self.emotion_groups.keys():
                    subset = self.data[
                        (self.data['scale'] == scale) & 
                        (self.data['expressivity'] == expr) &
                        (self.data['emotion_group'] == group)
                    ]
                    
                    if len(subset) > 0:
                        results.append({
                            'scale': scale,
                            'expressivity': expr,
                            'emotion_group': group,
                            'emotion_mean': subset['emotion'].mean(),
                            'quality_mean': subset['quality'].mean(),
                            'similarity_mean': subset['similarity'].mean(),
                            'count': len(subset)
                        })
        
        self.group_results = pd.DataFrame(results)
        
        # Display results by group
        for group in self.emotion_groups.keys():
            print(f"\n{group.upper().replace('_', ' ')} GROUP:")
            print("=" * 60)
            print("Scale | Expr  | Emotion | Quality | Similarity | Count")
            print("=" * 60)
            
            group_data = self.group_results[self.group_results['emotion_group'] == group]
            for _, row in group_data.sort_values(['expressivity', 'scale']).iterrows():
                print(f"{row['scale']:5.1f} | {row['expressivity']:4s} | {row['emotion_mean']:7.2f} | {row['quality_mean']:7.2f} | {row['similarity_mean']:10.2f} | {row['count']:5.0f}")
        
        return self.group_results
    
    def find_optimal_ranges_by_group(self):
        """Find optimal scale ranges for each emotion group"""
        print("\n=== OPTIMAL RANGES BY EMOTION GROUP ===")
        
        self.group_recommendations = {}
        
        for group in self.emotion_groups.keys():
            print(f"\n{group.upper().replace('_', ' ')} GROUP ANALYSIS:")
            print("-" * 50)
            
            group_data = self.group_results[self.group_results['emotion_group'] == group]
            
            for expr in ['none', '0.6']:
                expr_data = group_data[group_data['expressivity'] == expr].sort_values('scale')
                
                if len(expr_data) == 0:
                    continue
                    
                print(f"\n  {expr.upper()} EXPRESSIVITY:")
                
                # Find peak emotion score
                peak_idx = expr_data['emotion_mean'].idxmax()
                peak_row = expr_data.loc[peak_idx]
                print(f"    Peak emotion: {peak_row['emotion_mean']:.2f} at scale {peak_row['scale']:.1f}")
                
                # Find quality threshold (last scale >= 4.0)
                quality_ok = expr_data[expr_data['quality_mean'] >= 4.0]
                max_quality_scale = quality_ok['scale'].max() if not quality_ok.empty else None
                print(f"    Quality >4.0 up to scale: {max_quality_scale}")
                
                # Calculate improvement rates
                scales = expr_data['scale'].values
                emotions = expr_data['emotion_mean'].values
                
                improvements = []
                for i in range(1, len(emotions)):
                    improvement = (emotions[i] - emotions[i-1]) / (scales[i] - scales[i-1])
                    improvements.append(improvement)
                    print(f"    Scale {scales[i-1]:.1f}→{scales[i]:.1f}: {improvement:+.3f} emotion/scale")
                
                # Find plateau point (improvement < 0.1)
                plateau_scale = None
                for i, improvement in enumerate(improvements):
                    if improvement < 0.1:
                        plateau_scale = scales[i+1]
                        break
                
                print(f"    Plateau after scale: {plateau_scale if plateau_scale else 'None detected'}")
                
                # Store recommendations
                if group not in self.group_recommendations:
                    self.group_recommendations[group] = {}
                
                self.group_recommendations[group][expr] = {
                    'peak_scale': peak_row['scale'],
                    'peak_emotion': peak_row['emotion_mean'],
                    'max_quality_scale': max_quality_scale,
                    'plateau_scale': plateau_scale
                }
    
    def compare_groups_expressivity_effectiveness(self):
        """Compare 0.6 vs none effectiveness across groups"""
        print("\n=== EXPRESSIVITY 0.6 EFFECTIVENESS BY GROUP ===")
        
        for group in self.emotion_groups.keys():
            print(f"\n{group.upper().replace('_', ' ')} GROUP:")
            print("-" * 50)
            print("Scale | Emotion Diff | Quality Diff | Winner")
            print("-" * 50)
            
            group_data = self.group_results[self.group_results['emotion_group'] == group]
            
            for scale in sorted(group_data['scale'].unique()):
                none_row = group_data[(group_data['scale'] == scale) & (group_data['expressivity'] == 'none')]
                six_row = group_data[(group_data['scale'] == scale) & (group_data['expressivity'] == '0.6')]
                
                if not none_row.empty and not six_row.empty:
                    emotion_diff = six_row['emotion_mean'].iloc[0] - none_row['emotion_mean'].iloc[0]
                    quality_diff = six_row['quality_mean'].iloc[0] - none_row['quality_mean'].iloc[0]
                    
                    if emotion_diff > 0.3 and quality_diff > -0.3:
                        winner = '0.6 Strong ✅'
                    elif emotion_diff > 0.1 and quality_diff > -0.5:
                        winner = '0.6 ✅'
                    elif emotion_diff < -0.3 or quality_diff < -0.5:
                        winner = 'none'
                    else:
                        winner = 'similar'
                    
                    print(f'{scale:5.1f} | {emotion_diff:12.2f} | {quality_diff:12.2f} | {winner}')
    
    def create_group_comparison_visualization(self):
        """Create comprehensive visualization comparing emotion groups"""
        print(f"\n=== CREATING EMOTION GROUP VISUALIZATIONS ===")
        
        # Set up the plotting
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('TTS Emotion Groups Analysis: Different Features, Different Behaviors\n491 Evaluations by Implementation Type', fontsize=16, fontweight='bold')
        
        colors = {
            'emotion_labels': '#1f77b4',  # Blue
            'vector_first3': '#ff7f0e',   # Orange  
            'vector_last3': '#2ca02c'     # Green
        }
        
        group_names = {
            'emotion_labels': 'Emotion Labels\n(angry, sad, happy, whisper, toneup, tonedown)',
            'vector_first3': 'Vector First 3\n(excited, furious, terrified)',
            'vector_last3': 'Vector Last 3\n(fear, surprise, excitement)'
        }
        
        # Plot 1-3: Emotion Expression vs Scale for each group
        for idx, group in enumerate(self.emotion_groups.keys()):
            ax = axes[0, idx]
            
            group_data = self.group_results[self.group_results['emotion_group'] == group]
            
            for expr in ['none', '0.6']:
                expr_data = group_data[group_data['expressivity'] == expr].sort_values('scale')
                if not expr_data.empty:
                    linestyle = '-' if expr == 'none' else '--'
                    marker = 'o' if expr == 'none' else 's'
                    ax.plot(expr_data['scale'], expr_data['emotion_mean'], 
                           marker=marker, linestyle=linestyle, linewidth=3, markersize=8,
                           color=colors[group], alpha=0.8 if expr == 'none' else 1.0,
                           label=f'Expressivity {expr}')
            
            ax.axhline(y=4.0, color='red', linestyle=':', alpha=0.7, label='Midpoint')
            ax.set_xlabel('Emotion Scale')
            ax.set_ylabel('Emotion Expression Score')
            ax.set_title(group_names[group], fontsize=11, fontweight='bold')
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)
            ax.set_ylim(2.5, 6.0)
        
        # Plot 4: Quality comparison across groups
        ax4 = axes[1, 0]
        for group in self.emotion_groups.keys():
            group_data = self.group_results[self.group_results['emotion_group'] == group]
            
            # Average across expressivity types
            avg_data = group_data.groupby('scale').agg({
                'quality_mean': 'mean'
            }).reset_index()
            
            ax4.plot(avg_data['scale'], avg_data['quality_mean'], 
                    'o-', linewidth=3, markersize=8, color=colors[group],
                    label=group.replace('_', ' ').title())
        
        ax4.axhline(y=4.0, color='red', linestyle='--', alpha=0.7, label='Acceptable threshold')
        ax4.set_xlabel('Emotion Scale')
        ax4.set_ylabel('Quality Score')
        ax4.set_title('Quality Performance by Group', fontweight='bold')
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)
        
        # Plot 5: Expressivity 0.6 advantage by group
        ax5 = axes[1, 1]
        
        x_offset = {'emotion_labels': -0.1, 'vector_first3': 0, 'vector_last3': 0.1}
        
        for group in self.emotion_groups.keys():
            group_data = self.group_results[self.group_results['emotion_group'] == group]
            
            advantages = []
            scales = []
            
            for scale in sorted(group_data['scale'].unique()):
                none_row = group_data[(group_data['scale'] == scale) & (group_data['expressivity'] == 'none')]
                six_row = group_data[(group_data['scale'] == scale) & (group_data['expressivity'] == '0.6')]
                
                if not none_row.empty and not six_row.empty:
                    advantage = six_row['emotion_mean'].iloc[0] - none_row['emotion_mean'].iloc[0]
                    advantages.append(advantage)
                    scales.append(scale + x_offset[group])
            
            if advantages:
                bars = ax5.bar(scales, advantages, width=0.2, alpha=0.7, 
                              color=colors[group], label=group.replace('_', ' ').title())
                
                # Color bars based on advantage level
                for bar, advantage in zip(bars, advantages):
                    if advantage > 0.3:
                        bar.set_color(colors[group])
                        bar.set_alpha(1.0)
                    elif advantage < -0.3:
                        bar.set_color('red')
                        bar.set_alpha(0.7)
                    else:
                        bar.set_alpha(0.5)
        
        ax5.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax5.axhline(y=0.3, color='green', linestyle='--', alpha=0.7, label='Strong advantage')
        ax5.axhline(y=-0.3, color='red', linestyle='--', alpha=0.7, label='Disadvantage')
        ax5.set_xlabel('Emotion Scale')
        ax5.set_ylabel('Emotion Advantage (0.6 - none)')
        ax5.set_title('0.6 Expressivity Advantage by Group', fontweight='bold')
        ax5.legend(fontsize=9)
        ax5.grid(True, alpha=0.3)
        
        # Plot 6: Peak performance summary
        ax6 = axes[1, 2]
        
        # Create peak performance comparison
        peak_data = []
        for group in self.emotion_groups.keys():
            for expr in ['none', '0.6']:
                if group in self.group_recommendations and expr in self.group_recommendations[group]:
                    peak_data.append({
                        'group': group,
                        'expressivity': expr,
                        'peak_scale': self.group_recommendations[group][expr]['peak_scale'],
                        'peak_emotion': self.group_recommendations[group][expr]['peak_emotion']
                    })
        
        if peak_data:
            peak_df = pd.DataFrame(peak_data)
            
            for group in self.emotion_groups.keys():
                group_peaks = peak_df[peak_df['group'] == group]
                
                none_peak = group_peaks[group_peaks['expressivity'] == 'none']
                six_peak = group_peaks[group_peaks['expressivity'] == '0.6']
                
                if not none_peak.empty:
                    ax6.scatter(none_peak['peak_scale'].iloc[0], none_peak['peak_emotion'].iloc[0],
                              s=200, color=colors[group], marker='o', alpha=0.7, 
                              label=f'{group.replace("_", " ").title()} (none)')
                
                if not six_peak.empty:
                    ax6.scatter(six_peak['peak_scale'].iloc[0], six_peak['peak_emotion'].iloc[0],
                              s=200, color=colors[group], marker='s', alpha=1.0,
                              label=f'{group.replace("_", " ").title()} (0.6)')
        
        ax6.set_xlabel('Peak Scale')
        ax6.set_ylabel('Peak Emotion Score')
        ax6.set_title('Peak Performance Comparison\n(Circle=none, Square=0.6)', fontweight='bold')
        ax6.legend(fontsize=8)
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save figure
        output_path = self.output_dir / 'emotion_groups_comparison.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        
        print(f"📊 Saved: {output_path}")
    
    def generate_group_specific_recommendations(self):
        """Generate recommendations for each emotion group"""
        print(f"\n" + "="*80)
        print("EMOTION GROUPS STRATEGIC RECOMMENDATIONS")
        print("="*80)
        
        for group in self.emotion_groups.keys():
            print(f"\n🎯 {group.upper().replace('_', ' ')} GROUP:")
            print(f"   Emotions: {self.emotion_groups[group]}")
            print("-" * 60)
            
            if group in self.group_recommendations:
                for expr in ['none', '0.6']:
                    if expr in self.group_recommendations[group]:
                        rec = self.group_recommendations[group][expr]
                        print(f"   {expr.upper()} Expressivity:")
                        print(f"     Peak performance: {rec['peak_emotion']:.2f} at scale {rec['peak_scale']:.1f}")
                        print(f"     Quality threshold: {rec['max_quality_scale']}")
                        print(f"     Plateau after: {rec['plateau_scale']}")
        
        print(f"\n📋 IMPLEMENTATION-SPECIFIC INSIGHTS:")
        print("-" * 50)
        print("• EMOTION LABELS: Traditional discrete emotion categories")
        print("• VECTOR FIRST 3: High-intensity emotional states")  
        print("• VECTOR LAST 3: Complex/nuanced emotional expressions")
        print("\nDifferent emotion features may require different scaling strategies!")
    
    def save_detailed_report(self):
        """Save detailed analysis report"""
        report_path = self.output_dir / 'emotion_groups_analysis_report.md'
        
        with open(report_path, 'w') as f:
            f.write("# TTS Emotion Groups Analysis Report\n\n")
            f.write("## Emotion Group Definitions\n\n")
            
            for group, emotions in self.emotion_groups.items():
                f.write(f"### {group.replace('_', ' ').title()}\n")
                f.write(f"Emotions: {', '.join(emotions)}\n")
                f.write(f"Count: {len(self.data[self.data['emotion_group'] == group])} evaluations\n\n")
            
            f.write("## Key Findings\n\n")
            f.write("- Different emotion implementation types show distinct scaling behaviors\n")
            f.write("- Vector-based emotions may have different optimal scale ranges than labels\n")
            f.write("- Expressivity 0.6 effectiveness varies by emotion group\n\n")
            
            f.write("## Detailed Results\n\n")
            f.write("See emotion_groups_comparison.png for visual analysis\n")
        
        print(f"📄 Saved report: {report_path}")

def main():
    """Execute complete emotion groups analysis"""
    analyzer = EmotionGroupsAnalyzer('/Users/bagsanghui/ssfm30_qa/analysis/current_evaluations.csv')
    
    # Run comprehensive analysis
    analyzer.analyze_groups_by_scale()
    analyzer.find_optimal_ranges_by_group()
    analyzer.compare_groups_expressivity_effectiveness()
    analyzer.create_group_comparison_visualization()
    analyzer.generate_group_specific_recommendations()
    analyzer.save_detailed_report()

if __name__ == "__main__":
    main()