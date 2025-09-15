#!/usr/bin/env python3
"""
TTS Quality vs Intensity Trade-off Analysis

Goals:
1. Find optimal scale range where quality decrease is acceptable for intensity gain
2. Compare expressivity_none vs expressivity_0.6 effectiveness across scales  
3. Identify "clipping point" where expressivity 0.6 stabilizer limits intensity
4. Recommend optimal strategy: which expressivity + scale range to use
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json

class TradeOffAnalyzer:
    def __init__(self, csv_path):
        """Initialize with evaluation data"""
        self.data = self.load_and_parse_data(csv_path)
        self.prepare_analysis_variables()
        
    def load_and_parse_data(self, csv_path):
        """Load CSV and parse JSON scores"""
        df = pd.read_csv(csv_path)
        
        # Parse JSON scores
        def parse_scores(score_str):
            try:
                scores = json.loads(score_str.replace('""', '"'))
                return pd.Series({
                    'quality': scores.get('quality', np.nan),
                    'emotion': scores.get('emotion', np.nan), 
                    'similarity': scores.get('similarity', np.nan)
                })
            except:
                return pd.Series({'quality': np.nan, 'emotion': np.nan, 'similarity': np.nan})
        
        score_df = df['scores'].apply(parse_scores)
        df = pd.concat([df, score_df], axis=1)
        
        return df
    
    def prepare_analysis_variables(self):
        """Extract variables from sample_id"""
        sample_parts = self.data['sample_id'].str.split('_', expand=True)
        self.data['voice'] = sample_parts[0]
        self.data['emotion'] = sample_parts[1]
        self.data['text_type'] = sample_parts[2]
        
        try:
            self.data['scale'] = sample_parts[4].astype(float)
        except:
            self.data['scale'] = 1.0
            
        # Extract expressivity from session_id
        self.data['expressivity'] = self.data['session_id'].str.extract(r'expressivity_([^_]+)')
        
        # Clean data - convert scores to numeric
        for col in ['quality', 'emotion', 'similarity']:
            self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
    
    def analyze_quality_vs_intensity_tradeoff(self):
        """Analyze quality decline vs scale increase to find acceptable trade-off point"""
        print("=== QUALITY vs INTENSITY TRADE-OFF ANALYSIS ===")
        
        # Group by scale and calculate mean quality/similarity
        scale_analysis = self.data.groupby(['scale', 'expressivity']).agg({
            'quality': ['mean', 'std', 'count'],
            'similarity': ['mean', 'std', 'count'],
            'emotion': ['mean', 'std', 'count']
        }).reset_index()
        
        # Flatten column names
        scale_analysis.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] for col in scale_analysis.columns]
        
        print("\nQuality vs Scale Analysis:")
        print("=" * 50)
        for expressivity in ['none', '0.6']:
            exp_data = scale_analysis[scale_analysis['expressivity'] == expressivity]
            print(f"\nEXPRESSIVITY {expressivity.upper()}:")
            print("Scale | Quality | Similarity | Emotion | Sample Count")
            print("-" * 55)
            for _, row in exp_data.iterrows():
                print(f"{row['scale']:5.1f} | {row['quality_mean']:7.2f} | {row['similarity_mean']:10.2f} | {row['emotion_mean']:7.2f} | {row['quality_count']:12.0f}")
        
        return scale_analysis
    
    def find_optimal_trade_off_points(self, scale_analysis):
        """Find optimal trade-off points using multiple criteria"""
        print("\n=== OPTIMAL TRADE-OFF POINT ANALYSIS ===")
        
        recommendations = {}
        
        for expressivity in ['none', '0.6']:
            exp_data = scale_analysis[scale_analysis['expressivity'] == expressivity].sort_values('scale')
            
            if len(exp_data) == 0:
                continue
                
            print(f"\n{expressivity.upper()} EXPRESSIVITY ANALYSIS:")
            print("-" * 40)
            
            # Calculate quality decline rate
            scales = exp_data['scale'].values
            quality_scores = exp_data['quality_mean'].values
            similarity_scores = exp_data['similarity_mean'].values
            
            # Find point where quality drops below acceptable threshold (e.g., 4.0)
            acceptable_quality = 4.0
            quality_threshold_scale = None
            
            for i, (scale, quality) in enumerate(zip(scales, quality_scores)):
                if quality < acceptable_quality:
                    quality_threshold_scale = scales[i-1] if i > 0 else scale
                    break
            
            # Calculate decline rates between consecutive scales
            quality_declines = []
            for i in range(1, len(quality_scores)):
                decline_rate = (quality_scores[i-1] - quality_scores[i]) / (scales[i] - scales[i-1])
                quality_declines.append(decline_rate)
                
            avg_decline_rate = np.mean(quality_declines) if quality_declines else 0
            
            # Find "elbow point" - where decline accelerates
            elbow_scale = self.find_elbow_point(scales, quality_scores)
            
            print(f"Max scale before quality < 4.0: {quality_threshold_scale}")
            print(f"Average quality decline per scale unit: {avg_decline_rate:.3f}")
            print(f"Elbow point (accelerated decline): {elbow_scale:.1f}")
            
            # Recommendation based on multiple criteria
            if quality_threshold_scale:
                recommended_scale = min(quality_threshold_scale, elbow_scale if elbow_scale else quality_threshold_scale)
            else:
                recommended_scale = elbow_scale if elbow_scale else max(scales)
            
            recommendations[expressivity] = {
                'max_scale': recommended_scale,
                'quality_threshold_scale': quality_threshold_scale,
                'elbow_scale': elbow_scale,
                'decline_rate': avg_decline_rate
            }
            
            print(f"🎯 RECOMMENDED MAX SCALE: {recommended_scale:.1f}")
            
        return recommendations
    
    def find_elbow_point(self, x, y):
        """Find elbow point using second derivative"""
        if len(x) < 3:
            return None
            
        # Calculate second derivative
        first_derivative = np.gradient(y, x)
        second_derivative = np.gradient(first_derivative, x)
        
        # Find point of maximum curvature (highest second derivative)
        max_curvature_idx = np.argmax(np.abs(second_derivative))
        return x[max_curvature_idx]
    
    def analyze_expressivity_effectiveness(self):
        """Compare expressivity none vs 0.6 across scales"""
        print("\n=== EXPRESSIVITY 0.6 vs NONE COMPARISON ===")
        
        # Create pivot table for comparison
        comparison_data = self.data.groupby(['scale', 'expressivity']).agg({
            'quality': 'mean',
            'similarity': 'mean',
            'emotion': 'mean'
        }).reset_index()
        
        # Calculate differences (0.6 - none) for each scale
        pivot_quality = comparison_data.pivot(index='scale', columns='expressivity', values='quality')
        pivot_emotion = comparison_data.pivot(index='scale', columns='expressivity', values='emotion')
        
        if 'none' in pivot_quality.columns and '0.6' in pivot_quality.columns:
            quality_diff = pivot_quality['0.6'] - pivot_quality['none']
            
            print("\nQuality Difference (0.6 - none) by Scale:")
            print("Scale | Quality Diff | Interpretation")
            print("-" * 45)
            for scale, diff in quality_diff.items():
                interpretation = "0.6 Better" if diff > 0.1 else "0.6 Worse" if diff < -0.1 else "Similar"
                print(f"{scale:5.1f} | {diff:12.3f} | {interpretation}")
        
        if 'none' in pivot_emotion.columns and '0.6' in pivot_emotion.columns:
            emotion_diff = pivot_emotion['0.6'] - pivot_emotion['none']
            
            print("\nEmotion Expression Difference (0.6 - none) by Scale:")
            print("Scale | Emotion Diff | Interpretation")
            print("-" * 45)
            for scale, diff in emotion_diff.items():
                interpretation = "0.6 Better" if diff > 0.1 else "0.6 Worse" if diff < -0.1 else "Similar"
                print(f"{scale:5.1f} | {diff:11.3f} | {interpretation}")
        
        return pivot_quality, pivot_emotion
    
    def find_expressivity_clipping_point(self, pivot_emotion):
        """Find where expressivity 0.6 effectiveness plateaus (clipping point)"""
        print("\n=== EXPRESSIVITY 0.6 CLIPPING POINT ANALYSIS ===")
        
        if 'none' not in pivot_emotion.columns or '0.6' not in pivot_emotion.columns:
            print("Insufficient data for clipping analysis")
            return None
            
        emotion_diff = pivot_emotion['0.6'] - pivot_emotion['none']
        scales = emotion_diff.index.values
        diffs = emotion_diff.values
        
        # Find where improvement plateaus or starts declining
        clipping_scale = None
        max_improvement = np.max(diffs)
        max_improvement_scale = scales[np.argmax(diffs)]
        
        # Look for plateau: where improvement drops below 80% of max
        plateau_threshold = max_improvement * 0.8
        
        for i, (scale, diff) in enumerate(zip(scales, diffs)):
            if scale > max_improvement_scale and diff < plateau_threshold:
                clipping_scale = scale
                break
        
        print(f"Maximum 0.6 advantage at scale: {max_improvement_scale:.1f}")
        print(f"Maximum advantage value: {max_improvement:.3f}")
        print(f"Effectiveness plateau starts at: {clipping_scale if clipping_scale else 'Not detected'}")
        
        return {
            'max_scale': max_improvement_scale,
            'max_advantage': max_improvement,
            'clipping_scale': clipping_scale
        }
    
    def create_trade_off_visualizations(self, scale_analysis):
        """Create comprehensive visualizations"""
        print("\n=== GENERATING TRADE-OFF VISUALIZATIONS ===")
        
        # Set up the plotting style
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('TTS Quality vs Intensity Trade-off Analysis', fontsize=16)
        
        # Plot 1: Quality vs Scale by Expressivity
        ax1 = axes[0, 0]
        for expressivity in ['none', '0.6']:
            data = scale_analysis[scale_analysis['expressivity'] == expressivity]
            ax1.plot(data['scale'], data['quality_mean'], 'o-', 
                    label=f'Expressivity {expressivity}', linewidth=2, markersize=8)
            ax1.fill_between(data['scale'], 
                           data['quality_mean'] - data['quality_std']/2,
                           data['quality_mean'] + data['quality_std']/2, 
                           alpha=0.3)
        
        ax1.axhline(y=4.0, color='red', linestyle='--', alpha=0.7, label='Acceptable threshold')
        ax1.set_xlabel('Emotion Scale')
        ax1.set_ylabel('Quality Score')
        ax1.set_title('Quality Decline vs Scale')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Similarity vs Scale
        ax2 = axes[0, 1] 
        for expressivity in ['none', '0.6']:
            data = scale_analysis[scale_analysis['expressivity'] == expressivity]
            ax2.plot(data['scale'], data['similarity_mean'], 's-', 
                    label=f'Expressivity {expressivity}', linewidth=2, markersize=8)
        
        ax2.axhline(y=4.0, color='red', linestyle='--', alpha=0.7)
        ax2.set_xlabel('Emotion Scale')
        ax2.set_ylabel('Similarity Score')
        ax2.set_title('Similarity vs Scale')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Emotion Expression vs Scale
        ax3 = axes[1, 0]
        for expressivity in ['none', '0.6']:
            data = scale_analysis[scale_analysis['expressivity'] == expressivity]
            if not data['emotion_mean'].isna().all():
                ax3.plot(data['scale'], data['emotion_mean'], '^-', 
                        label=f'Expressivity {expressivity}', linewidth=2, markersize=8)
        
        ax3.set_xlabel('Emotion Scale')
        ax3.set_ylabel('Emotion Expression Score')
        ax3.set_title('Emotion Expression vs Scale')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Trade-off Matrix (Quality vs Emotion)
        ax4 = axes[1, 1]
        for expressivity in ['none', '0.6']:
            data = scale_analysis[scale_analysis['expressivity'] == expressivity]
            valid_data = data.dropna(subset=['emotion_mean', 'quality_mean'])
            if len(valid_data) > 0:
                scatter = ax4.scatter(valid_data['emotion_mean'], valid_data['quality_mean'], 
                                    s=valid_data['scale']*30, alpha=0.7, 
                                    label=f'Expressivity {expressivity}')
                
                # Add scale labels
                for _, row in valid_data.iterrows():
                    ax4.annotate(f"{row['scale']:.1f}", 
                               (row['emotion_mean'], row['quality_mean']),
                               xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        ax4.set_xlabel('Emotion Expression Score')
        ax4.set_ylabel('Quality Score')  
        ax4.set_title('Quality vs Emotion Trade-off\n(Size = Scale)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/Users/bagsanghui/ssfm30_qa/analysis/trade_off_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        print("📊 Visualizations saved to: trade_off_analysis.png")
    
    def generate_strategic_recommendations(self, recommendations, clipping_analysis):
        """Generate final strategic recommendations"""
        print("\n" + "="*60)
        print("STRATEGIC RECOMMENDATIONS FOR TTS EMOTION SCALING")
        print("="*60)
        
        print("\n🎯 OPTIMAL SCALE RANGES:")
        print("-" * 30)
        
        for expressivity, rec in recommendations.items():
            print(f"\n{expressivity.upper()} EXPRESSIVITY:")
            print(f"  Recommended max scale: {rec['max_scale']:.1f}")
            print(f"  Quality threshold: {rec['quality_threshold_scale']}")
            print(f"  Quality decline rate: {rec['decline_rate']:.3f} points/scale")
        
        print(f"\n🔧 EXPRESSIVITY 0.6 ANALYSIS:")
        if clipping_analysis:
            print(f"  Peak effectiveness at scale: {clipping_analysis['max_scale']:.1f}")
            print(f"  Maximum advantage: {clipping_analysis['max_advantage']:.3f} points")
            clipping = clipping_analysis['clipping_scale']
            print(f"  Effectiveness plateau: {clipping:.1f if clipping else 'Not detected'}")
        
        print(f"\n📋 FOLLOW-UP RESEARCH RECOMMENDATIONS:")
        print("-" * 40)
        
        # Determine optimal strategy based on analysis
        none_rec = recommendations.get('none', {})
        six_rec = recommendations.get('0.6', {})
        
        none_max = none_rec.get('max_scale', 0)
        six_max = six_rec.get('max_scale', 0)
        
        if clipping_analysis and clipping_analysis['max_advantage'] > 0.3:
            print("✅ EXPRESSIVITY 0.6 shows clear advantage")
            print(f"   → Focus qualitative research on 0.6 with scales 0.5-{six_max:.1f}")
        else:
            print("⚠️  EXPRESSIVITY 0.6 advantage unclear")  
            print(f"   → Compare head-to-head: none (0.5-{none_max:.1f}) vs 0.6 (0.5-{six_max:.1f})")
        
        print(f"\n🧪 CONTROLLED EXPERIMENT DESIGN:")
        print("   - Select 2-3 high-performing emotions")
        print("   - Test scales: 0.5, 1.0, 1.5 (based on quality thresholds)")
        print("   - A/B comparison: same text, different expressivity")
        print("   - 5-10 expert evaluators for statistical power")
        
        print(f"\n⚖️ BUSINESS DECISION FRAMEWORK:")
        print("   Quality vs Intensity trade-off acceptance:")
        print("   - Acceptable quality drop: 0.5-1.0 points for strong emotion")
        print("   - Minimum quality threshold: 4.0/7 (current analysis baseline)")
        print("   - Emotion expression gain requirement: >0.5 points improvement")

def main():
    """Execute complete trade-off analysis"""
    analyzer = TradeOffAnalyzer('/Users/bagsanghui/ssfm30_qa/analysis/current_evaluations.csv')
    
    # Run comprehensive analysis
    scale_analysis = analyzer.analyze_quality_vs_intensity_tradeoff()
    recommendations = analyzer.find_optimal_trade_off_points(scale_analysis)
    pivot_quality, pivot_emotion = analyzer.analyze_expressivity_effectiveness()
    clipping_analysis = analyzer.find_expressivity_clipping_point(pivot_emotion)
    
    # Generate visualizations
    analyzer.create_trade_off_visualizations(scale_analysis)
    
    # Final recommendations
    analyzer.generate_strategic_recommendations(recommendations, clipping_analysis)

if __name__ == "__main__":
    main()