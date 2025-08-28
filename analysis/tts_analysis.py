#!/usr/bin/env python3
"""
TTS QA System Analysis Script
Based on plan.md Mixed Effects Model requirements

Analysis Model from plan.md:
Quality_Score = β₀ + β₁(voice) + β₂(text) + β₃(emotion) + β₄(scale) 
                + β₅(emotion×scale) + β₆(emotion_type) 
                + random(evaluator) + random(sample) + ε

Data source: sample_evaluations_rows.csv
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm
import warnings
warnings.filterwarnings('ignore')

class TTSAnalyzer:
    def __init__(self, csv_path):
        """Initialize analyzer with data from CSV file"""
        self.data = self.load_and_parse_data(csv_path)
        self.prepare_analysis_variables()
        
    def load_and_parse_data(self, csv_path):
        """Load CSV and parse JSON scores"""
        print(f"Loading data from {csv_path}")
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
        
        # Extract scores
        score_df = df['scores'].apply(parse_scores)
        df = pd.concat([df, score_df], axis=1)
        
        print(f"Loaded {len(df)} evaluations")
        return df
    
    def prepare_analysis_variables(self):
        """Extract variables from sample_id following plan.md structure"""
        print("Parsing sample_id variables...")
        
        # Parse sample_id: {voice}_{emotion}_{text_type}_scale_{scale}
        sample_parts = self.data['sample_id'].str.split('_', expand=True)
        self.data['voice'] = sample_parts[0]  # v001, v002
        self.data['emotion'] = sample_parts[1]  # angry, sad, happy, etc.
        self.data['text_type'] = sample_parts[2]  # match, neutral, opposite
        
        # Handle scale conversion more carefully
        try:
            self.data['scale'] = sample_parts[4].astype(float)  # 0.5, 1.0, etc.
        except (ValueError, KeyError):
            print("Warning: Could not parse scale values from sample_id")
            self.data['scale'] = 1.0  # default value
        
        # Determine emotion_type based on plan.md definitions
        emotion_labels = ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown']
        emotion_vectors = ['excited', 'furious', 'terrified', 'fear', 'surprise', 'excitement']
        
        self.data['emotion_type'] = self.data['emotion'].apply(
            lambda x: 'emotion_label' if x in emotion_labels else 'emotion_vector'
        )
        
        # Extract expressivity from session_id
        self.data['expressivity'] = self.data['session_id'].str.extract(r'expressivity_([^_]+)')
        
        # Create evaluator proxy (session-based for now)
        self.data['evaluator'] = self.data['session_id']
        
        print("Variables prepared:")
        print(f"  - Voices: {self.data['voice'].unique()}")
        print(f"  - Emotions: {len(self.data['emotion'].unique())} unique")
        print(f"  - Text types: {self.data['text_type'].unique()}")
        print(f"  - Scales: {sorted(self.data['scale'].unique())}")
        print(f"  - Emotion types: {self.data['emotion_type'].unique()}")
        print(f"  - Expressivity: {self.data['expressivity'].unique()}")
    
    def run_mixed_effects_analysis(self, outcome='quality'):
        """Run Mixed Effects Model as specified in plan.md"""
        print(f"\n=== Mixed Effects Analysis for {outcome.upper()} ===")
        
        # Remove rows with missing outcome values
        analysis_data = self.data.dropna(subset=[outcome]).copy()
        print(f"Analysis sample: {len(analysis_data)} evaluations")
        
        try:
            # Mixed Effects Model from plan.md
            formula = f"{outcome} ~ voice + text_type + emotion + scale + emotion_type + scale:emotion_type"
            
            model = mixedlm(formula, 
                          data=analysis_data, 
                          groups=analysis_data['evaluator'],  # random(evaluator)
                          re_formula="1")  # random intercept
            
            result = model.fit()
            
            print(f"\nMixed Effects Model Results ({outcome}):")
            print("=" * 50)
            print(result.summary())
            
            # Extract key statistics for plan.md expected results
            pvalues = result.pvalues
            effects = {
                'voice_effect': pvalues.get('voice[T.v002]', 1.0),
                'text_neutral': pvalues.get('text_type[T.neutral]', 1.0),
                'text_opposite': pvalues.get('text_type[T.opposite]', 1.0),
                'scale_effect': pvalues.get('scale', 1.0),
                'emotion_type_effect': pvalues.get('emotion_type[T.emotion_vector]', 1.0)
            }
            
            print(f"\nKey Effects Summary ({outcome}):")
            print("-" * 30)
            for effect, pval in effects.items():
                sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
                print(f"{effect}: p = {pval:.4f} {sig}")
            
            return result, analysis_data
            
        except Exception as e:
            print(f"Mixed effects model failed: {e}")
            print("Running simpler linear model...")
            return self.run_simple_analysis(analysis_data, outcome)
    
    def run_simple_analysis(self, data, outcome):
        """Fallback to simpler analysis if mixed effects fails"""
        import statsmodels.formula.api as smf
        
        # Simple OLS model
        formula = f"{outcome} ~ voice + text_type + emotion + scale + emotion_type"
        model = smf.ols(formula, data=data)
        result = model.fit()
        
        print(f"\nOLS Model Results ({outcome}):")
        print("=" * 50)
        print(result.summary())
        
        return result, data
    
    def automatic_quality_checks(self):
        """Automatic quality checks based on plan.md section 3.2"""
        print("\n=== Automatic Quality Checks ===")
        
        # Quality issues from comments
        quality_issues = {
            'silence_clips': 0,
            'audio_clipping': 0, 
            'duration_issues': 0,
            'volume_problems': 0,
            'robotic_voice': 0
        }
        
        comments = self.data['comment'].fillna('').str.lower()
        
        # Pattern matching for common issues
        patterns = {
            'silence_clips': ['음성 짤림', '끊김', '시작이 짤림', '앞부분', '처음이 짤림'],
            'audio_clipping': ['갈라짐', '깨짐', '튕김', '음성 품질'],
            'robotic_voice': ['로봇', '기계', '기계음'],
            'volume_problems': ['작게', '볼륨', '음량', '소리']
        }
        
        for issue, keywords in patterns.items():
            for keyword in keywords:
                quality_issues[issue] += comments.str.contains(keyword).sum()
        
        print("Quality Issues Detected:")
        for issue, count in quality_issues.items():
            if count > 0:
                print(f"  {issue}: {count} instances")
        
        # Score distribution analysis
        print("\nScore Distributions:")
        for metric in ['quality', 'emotion', 'similarity']:
            scores = self.data[metric].dropna()
            # Convert to numeric if needed
            scores = pd.to_numeric(scores, errors='coerce')
            scores = scores.dropna()  # Remove any conversion failures
            
            if len(scores) > 0:
                print(f"  {metric}: mean={scores.mean():.2f}, std={scores.std():.2f}")
                print(f"    Low scores (<4): {(scores < 4).sum()} ({(scores < 4).mean()*100:.1f}%)")
            else:
                print(f"  {metric}: No valid numeric data")
        
        return quality_issues
    
    def threshold_analysis(self):
        """Critical cases analysis from plan.md section 3.3"""
        print("\n=== Threshold Analysis ===")
        
        for metric in ['quality', 'emotion', 'similarity']:
            # Convert to numeric and clean data
            numeric_data = pd.to_numeric(self.data[metric], errors='coerce')
            valid_data = self.data[numeric_data.notna()].copy()
            valid_data[metric] = numeric_data.dropna()
            
            if len(valid_data) == 0:
                print(f"\n{metric.upper()} - No valid numeric data for analysis")
                continue
                
            # Critical cases (< 4)
            critical = valid_data[valid_data[metric] < 4]
            print(f"\n{metric.upper()} - Critical Cases (score < 4): {len(critical)}")
            
            if len(critical) > 0:
                print("  Parameter patterns in critical cases:")
                print(f"    Voice distribution: {critical['voice'].value_counts().to_dict()}")
                print(f"    Emotion types: {critical['emotion_type'].value_counts().to_dict()}")
                print(f"    Text types: {critical['text_type'].value_counts().to_dict()}")
                if 'scale' in critical.columns:
                    print(f"    Scale ranges: min={critical['scale'].min()}, max={critical['scale'].max()}")
            
            # High performers (≥ 6)
            high = valid_data[valid_data[metric] >= 6]
            print(f"\n{metric.upper()} - High Performers (score ≥ 6): {len(high)}")
            
            if len(high) > 0:
                print("  Parameter patterns in high performers:")
                print(f"    Voice distribution: {high['voice'].value_counts().to_dict()}")
                print(f"    Emotion types: {high['emotion_type'].value_counts().to_dict()}")
    
    def generate_summary_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*60)
        print("TTS QA SYSTEM ANALYSIS SUMMARY REPORT")
        print("="*60)
        
        print(f"\nDataset Overview:")
        print(f"  Total evaluations: {len(self.data)}")
        print(f"  Unique samples: {self.data['sample_id'].nunique()}")
        print(f"  Sessions: {self.data['session_id'].nunique()}")
        print(f"  Expressivity types: {self.data['expressivity'].value_counts().to_dict()}")
        
        # Run all analyses
        quality_issues = self.automatic_quality_checks()
        self.threshold_analysis()
        
        # Run mixed effects for all three metrics
        print(f"\n" + "="*60)
        print("MIXED EFFECTS MODEL ANALYSIS")
        print("="*60)
        
        for outcome in ['quality', 'emotion', 'similarity']:
            try:
                result, data = self.run_mixed_effects_analysis(outcome)
            except Exception as e:
                print(f"Analysis failed for {outcome}: {e}")
        
        print(f"\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)

def main():
    """Main analysis execution"""
    print("TTS QA System Analysis")
    print("Based on plan.md Mixed Effects Model")
    print("="*50)
    
    # Initialize analyzer
    analyzer = TTSAnalyzer('/Users/bagsanghui/ssfm30_qa/sample_evaluations_rows.csv')
    
    # Run comprehensive analysis
    analyzer.generate_summary_report()

if __name__ == "__main__":
    main()