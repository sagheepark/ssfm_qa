#!/usr/bin/env python3
"""
TTS QA System Analysis Script for voices_3 Dataset
Enhanced to support multiple experiment versions (voices_2 and voices_3)

Analysis Model:
Quality_Score = β₀ + β₁(voice) + β₂(text) + β₃(emotion) + β₄(scale) 
                + β₅(emotion×scale) + β₆(emotion_type) + β₇(audio_quality)
                + β₈(experiment_version) + random(evaluator) + random(sample) + ε

Data source: Supports both CSV files and direct Supabase queries
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
import os
from typing import Optional, Dict, List
warnings.filterwarnings('ignore')

class TTSAnalyzerV3:
    def __init__(self, csv_path: Optional[str] = None, supabase_data: Optional[Dict] = None):
        """Initialize analyzer with data from CSV file or Supabase"""
        if csv_path and os.path.exists(csv_path):
            self.data = self.load_and_parse_data(csv_path)
        elif supabase_data:
            self.data = self.load_from_supabase_data(supabase_data)
        else:
            raise ValueError("Either csv_path or supabase_data must be provided")
        
        self.prepare_analysis_variables()
        self.detect_experiment_versions()
        
    def detect_experiment_versions(self):
        """Detect which experiment versions are present in the data"""
        versions = []
        
        # Check for voices_3 indicators
        if 'audio_quality' in self.data.columns:
            versions.append('voices_3')
        if any('voices_3' in str(sid) for sid in self.data['session_id']):
            versions.append('voices_3')
            
        # Check for voices_2 indicators  
        if 'experiment_version' in self.data.columns:
            exp_versions = self.data['experiment_version'].unique()
            versions.extend([v for v in exp_versions if v not in versions])
        
        # Check session IDs for version indicators
        if any('voices_2' in str(sid) for sid in self.data['session_id']):
            if 'voices_2' not in versions:
                versions.append('voices_2')
                
        self.experiment_versions = versions if versions else ['unknown']
        print(f"Detected experiment versions: {self.experiment_versions}")
        
    def load_from_supabase_data(self, supabase_data: Dict) -> pd.DataFrame:
        """Load data from Supabase query results"""
        # Convert Supabase data format to DataFrame
        if 'evaluations' in supabase_data:
            evaluations = supabase_data['evaluations']
        else:
            evaluations = supabase_data
            
        # Convert to DataFrame
        df = pd.DataFrame(evaluations)
        
        # Parse scores JSON if needed
        if 'scores' in df.columns and df['scores'].dtype == 'object':
            scores_df = pd.json_normalize(df['scores'])
            df = pd.concat([df.drop('scores', axis=1), scores_df], axis=1)
            
        return df
        
    def load_and_parse_data(self, csv_path: str) -> pd.DataFrame:
        """Load data from CSV and parse JSON scores"""
        print(f"Loading data from: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows")
        
        # Parse JSON scores into separate columns
        if 'scores' in df.columns:
            def safe_parse_scores(scores_str):
                try:
                    if pd.isna(scores_str):
                        return {'quality': None, 'emotion': None, 'similarity': None}
                    if isinstance(scores_str, str):
                        return json.loads(scores_str)
                    return scores_str
                except (json.JSONDecodeError, TypeError):
                    return {'quality': None, 'emotion': None, 'similarity': None}
            
            scores_data = df['scores'].apply(safe_parse_scores)
            scores_df = pd.json_normalize(scores_data)
            
            # Combine with original data
            df = pd.concat([df.drop('scores', axis=1), scores_df], axis=1)
            
        return df
        
    def prepare_analysis_variables(self):
        """Extract analysis variables from sample_id and enhance data"""
        print("Preparing analysis variables...")
        
        # Parse sample_id to extract metadata
        def parse_sample_id(sample_id):
            """Parse sample_id format: {voice}_{emotion}_{text_type}_scale_{scale}"""
            if pd.isna(sample_id):
                return {'voice_id': None, 'emotion_value': None, 'text_type': None, 'scale': None}
                
            parts = str(sample_id).split('_')
            if len(parts) >= 5:
                return {
                    'voice_id': parts[0],  # v001, v002
                    'emotion_value': parts[1],  # angry, sad, excited, etc.
                    'text_type': parts[2],  # match, neutral, opposite
                    'scale': float(parts[4]) if parts[4].replace('.', '').isdigit() else None
                }
            return {'voice_id': None, 'emotion_value': None, 'text_type': None, 'scale': None}
        
        # Apply parsing if columns don't already exist
        if 'voice_id' not in self.data.columns:
            parsed_data = self.data['sample_id'].apply(parse_sample_id)
            parsed_df = pd.json_normalize(parsed_data)
            self.data = pd.concat([self.data, parsed_df], axis=1)
        
        # Determine emotion_type based on emotion_value
        def classify_emotion_type(emotion_value):
            if pd.isna(emotion_value):
                return None
            emotion_labels = ['angry', 'sad', 'happy', 'whisper', 'toneup', 'tonedown']
            return 'emotion_label' if emotion_value in emotion_labels else 'emotion_vector'
        
        if 'emotion_type' not in self.data.columns:
            self.data['emotion_type'] = self.data['emotion_value'].apply(classify_emotion_type)
        
        # Add experiment version detection based on session_id
        def detect_experiment_version(session_id):
            if pd.isna(session_id):
                return 'unknown'
            session_str = str(session_id)
            if 'voices_3' in session_str:
                return 'voices_3'
            elif 'voices_2' in session_str or 'expressivity' in session_str:
                return 'voices_2'
            else:
                return 'voices_1'
        
        if 'experiment_version' not in self.data.columns:
            self.data['experiment_version'] = self.data['session_id'].apply(detect_experiment_version)
        
        # Add audio quality detection
        if 'audio_quality' not in self.data.columns:
            def detect_audio_quality(session_id, experiment_version):
                if experiment_version == 'voices_3':
                    return 'hd1'
                elif experiment_version == 'voices_2':
                    return 'high'
                else:
                    return 'standard'
            
            self.data['audio_quality'] = self.data.apply(
                lambda row: detect_audio_quality(row['session_id'], row['experiment_version']), 
                axis=1
            )
        
        # Convert timestamp to datetime
        if 'timestamp' in self.data.columns:
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        
        print(f"Prepared data shape: {self.data.shape}")
        print(f"Experiment versions found: {self.data['experiment_version'].value_counts().to_dict()}")
        print(f"Audio quality distribution: {self.data['audio_quality'].value_counts().to_dict()}")
        
    def run_comprehensive_analysis(self):
        """Run comprehensive analysis including version comparisons"""
        print("\n" + "="*60)
        print("COMPREHENSIVE TTS ANALYSIS - MULTI-VERSION SUPPORT")
        print("="*60)
        
        # Basic statistics
        self.basic_statistics()
        
        # Version comparison analysis
        if len(self.experiment_versions) > 1:
            self.version_comparison_analysis()
        
        # Audio quality analysis
        self.audio_quality_analysis()
        
        # Traditional analyses
        self.emotion_scale_analysis()
        self.voice_comparison()
        self.text_type_analysis()
        self.mixed_effects_analysis()
        
        # Generate comprehensive report
        self.generate_comprehensive_report()
        
    def version_comparison_analysis(self):
        """Compare performance across different experiment versions"""
        print("\n" + "-"*50)
        print("VERSION COMPARISON ANALYSIS")
        print("-"*50)
        
        version_stats = self.data.groupby('experiment_version').agg({
            'quality': ['mean', 'std', 'count'],
            'emotion': ['mean', 'std'],
            'similarity': ['mean', 'std']
        }).round(3)
        
        print("\nVersion Statistics:")
        print(version_stats)
        
        # Statistical tests between versions
        versions = self.data['experiment_version'].unique()
        if len(versions) >= 2:
            for i, v1 in enumerate(versions):
                for v2 in versions[i+1:]:
                    data_v1 = self.data[self.data['experiment_version'] == v1]
                    data_v2 = self.data[self.data['experiment_version'] == v2]
                    
                    for metric in ['quality', 'emotion', 'similarity']:
                        if metric in data_v1.columns and metric in data_v2.columns:
                            stat, p_value = stats.ttest_ind(
                                data_v1[metric].dropna(), 
                                data_v2[metric].dropna()
                            )
                            print(f"\n{v1} vs {v2} - {metric}:")
                            print(f"  t-statistic: {stat:.4f}, p-value: {p_value:.4f}")
                            print(f"  Significant difference: {'Yes' if p_value < 0.05 else 'No'}")
        
        # Create version comparison plots
        self.plot_version_comparison()
        
    def audio_quality_analysis(self):
        """Analyze the impact of audio quality on evaluation scores"""
        print("\n" + "-"*50)
        print("AUDIO QUALITY ANALYSIS")
        print("-"*50)
        
        quality_stats = self.data.groupby('audio_quality').agg({
            'quality': ['mean', 'std', 'count'],
            'emotion': ['mean', 'std'],
            'similarity': ['mean', 'std']
        }).round(3)
        
        print("\nAudio Quality Statistics:")
        print(quality_stats)
        
        # Create audio quality comparison plot
        self.plot_audio_quality_comparison()
        
    def plot_version_comparison(self):
        """Create plots comparing different experiment versions"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Experiment Version Comparison', fontsize=16)
        
        metrics = ['quality', 'emotion', 'similarity']
        
        # Box plots for each metric
        for i, metric in enumerate(metrics):
            if metric in self.data.columns:
                ax = axes[i//2, i%2]
                sns.boxplot(data=self.data, x='experiment_version', y=metric, ax=ax)
                ax.set_title(f'{metric.title()} Score by Version')
                ax.set_xlabel('Experiment Version')
                ax.set_ylabel(f'{metric.title()} Score')
        
        # Overall score comparison (if we have all metrics)
        if all(metric in self.data.columns for metric in metrics):
            ax = axes[1, 1]
            self.data['overall_score'] = (self.data['quality'] + self.data['emotion'] + self.data['similarity']) / 3
            sns.boxplot(data=self.data, x='experiment_version', y='overall_score', ax=ax)
            ax.set_title('Overall Score by Version')
            ax.set_xlabel('Experiment Version')
            ax.set_ylabel('Overall Score')
        
        plt.tight_layout()
        plt.savefig('analysis/version_comparison_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def plot_audio_quality_comparison(self):
        """Create plots comparing different audio quality levels"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Audio Quality Impact Analysis', fontsize=16)
        
        metrics = ['quality', 'emotion', 'similarity']
        
        # Box plots for each metric
        for i, metric in enumerate(metrics):
            if metric in self.data.columns:
                ax = axes[i//2, i%2]
                sns.boxplot(data=self.data, x='audio_quality', y=metric, ax=ax)
                ax.set_title(f'{metric.title()} Score by Audio Quality')
                ax.set_xlabel('Audio Quality')
                ax.set_ylabel(f'{metric.title()} Score')
        
        # Quality vs Emotion correlation by audio quality
        if 'quality' in self.data.columns and 'emotion' in self.data.columns:
            ax = axes[1, 1]
            for quality in self.data['audio_quality'].unique():
                subset = self.data[self.data['audio_quality'] == quality]
                ax.scatter(subset['quality'], subset['emotion'], 
                          alpha=0.6, label=f'{quality} quality')
            ax.set_xlabel('Quality Score')
            ax.set_ylabel('Emotion Score')
            ax.set_title('Quality vs Emotion by Audio Quality')
            ax.legend()
        
        plt.tight_layout()
        plt.savefig('analysis/audio_quality_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def basic_statistics(self):
        """Generate basic statistics for all experiment versions"""
        print("\n" + "-"*50)
        print("BASIC STATISTICS")
        print("-"*50)
        
        # Overall statistics
        numeric_cols = ['quality', 'emotion', 'similarity']
        available_cols = [col for col in numeric_cols if col in self.data.columns]
        
        if available_cols:
            print("\nOverall Statistics:")
            print(self.data[available_cols].describe().round(3))
        
        # Statistics by experiment version
        print(f"\nData Distribution by Experiment Version:")
        version_counts = self.data['experiment_version'].value_counts()
        for version, count in version_counts.items():
            print(f"  {version}: {count} evaluations")
        
        # Statistics by audio quality
        if 'audio_quality' in self.data.columns:
            print(f"\nData Distribution by Audio Quality:")
            quality_counts = self.data['audio_quality'].value_counts()
            for quality, count in quality_counts.items():
                print(f"  {quality}: {count} evaluations")
    
    def emotion_scale_analysis(self):
        """Analyze emotion scale effectiveness across versions"""
        print("\n" + "-"*50)
        print("EMOTION SCALE ANALYSIS (Multi-Version)")
        print("-"*50)
        
        if 'scale' not in self.data.columns or 'emotion' not in self.data.columns:
            print("Missing required columns for emotion scale analysis")
            return
        
        # Scale analysis by version
        for version in self.experiment_versions:
            version_data = self.data[self.data['experiment_version'] == version]
            if len(version_data) > 0:
                print(f"\n{version} Scale Analysis:")
                scale_stats = version_data.groupby('scale')['emotion'].agg(['mean', 'std', 'count']).round(3)
                print(scale_stats)
        
        # Create scale comparison plot
        self.plot_emotion_scale_by_version()
    
    def plot_emotion_scale_by_version(self):
        """Plot emotion scale effectiveness by version"""
        if 'scale' not in self.data.columns or 'emotion' not in self.data.columns:
            return
            
        plt.figure(figsize=(12, 8))
        
        for version in self.experiment_versions:
            version_data = self.data[self.data['experiment_version'] == version]
            if len(version_data) > 0:
                scale_means = version_data.groupby('scale')['emotion'].mean()
                plt.plot(scale_means.index, scale_means.values, 
                        marker='o', label=f'{version}', linewidth=2)
        
        plt.xlabel('Emotion Scale')
        plt.ylabel('Average Emotion Score')
        plt.title('Emotion Scale Effectiveness by Experiment Version')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('analysis/emotion_scale_by_version.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def voice_comparison(self):
        """Compare voice performance across versions"""
        print("\n" + "-"*50)
        print("VOICE COMPARISON ANALYSIS")
        print("-"*50)
        
        if 'voice_id' not in self.data.columns:
            print("Missing voice_id column for voice comparison")
            return
        
        # Voice statistics by version
        for version in self.experiment_versions:
            version_data = self.data[self.data['experiment_version'] == version]
            if len(version_data) > 0 and 'quality' in version_data.columns:
                print(f"\n{version} Voice Performance:")
                voice_stats = version_data.groupby('voice_id')['quality'].agg(['mean', 'std', 'count']).round(3)
                print(voice_stats)
    
    def text_type_analysis(self):
        """Analyze text type performance across versions"""
        print("\n" + "-"*50)
        print("TEXT TYPE ANALYSIS")
        print("-"*50)
        
        if 'text_type' not in self.data.columns:
            print("Missing text_type column for text type analysis")
            return
        
        # Text type statistics by version
        for version in self.experiment_versions:
            version_data = self.data[self.data['experiment_version'] == version]
            if len(version_data) > 0 and 'similarity' in version_data.columns:
                print(f"\n{version} Text Type Performance:")
                text_stats = version_data.groupby('text_type')['similarity'].agg(['mean', 'std', 'count']).round(3)
                print(text_stats)
    
    def mixed_effects_analysis(self):
        """Run mixed effects model including version effects"""
        print("\n" + "-"*50)
        print("MIXED EFFECTS ANALYSIS (Enhanced for Multi-Version)")
        print("-"*50)
        
        # Check required columns
        required_cols = ['quality', 'voice_id', 'text_type', 'emotion_value', 'scale']
        missing_cols = [col for col in required_cols if col not in self.data.columns]
        
        if missing_cols:
            print(f"Missing required columns for mixed effects analysis: {missing_cols}")
            return
        
        # Prepare data for mixed effects model
        model_data = self.data.dropna(subset=required_cols + ['experiment_version'])
        
        if len(model_data) < 20:
            print("Insufficient data for mixed effects analysis")
            return
        
        try:
            # Enhanced model including experiment version and audio quality
            formula = "quality ~ voice_id + text_type + emotion_value + scale + experiment_version"
            if 'audio_quality' in model_data.columns:
                formula += " + audio_quality"
            
            # Add interaction terms
            formula += " + emotion_value:scale"
            
            # Random effects (if we have session identifiers)
            if 'session_id' in model_data.columns:
                model = mixedlm(formula, model_data, groups=model_data['session_id'])
                result = model.fit()
                print("\nMixed Effects Model Results (with session random effects):")
                print(result.summary())
            else:
                # Regular OLS if no grouping variable
                import statsmodels.formula.api as smf
                model = smf.ols(formula, data=model_data)
                result = model.fit()
                print("\nOLS Model Results:")
                print(result.summary())
                
        except Exception as e:
            print(f"Mixed effects analysis failed: {e}")
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive analysis report"""
        print("\n" + "="*60)
        print("COMPREHENSIVE ANALYSIS SUMMARY")
        print("="*60)
        
        # Create summary statistics
        summary = {
            'total_evaluations': len(self.data),
            'experiment_versions': list(self.data['experiment_version'].value_counts().to_dict().items()),
            'date_range': {
                'start': str(self.data['timestamp'].min()) if 'timestamp' in self.data.columns else 'Unknown',
                'end': str(self.data['timestamp'].max()) if 'timestamp' in self.data.columns else 'Unknown'
            }
        }
        
        # Add quality metrics if available
        numeric_cols = ['quality', 'emotion', 'similarity']
        available_cols = [col for col in numeric_cols if col in self.data.columns]
        
        if available_cols:
            summary['score_statistics'] = {}
            for col in available_cols:
                summary['score_statistics'][col] = {
                    'mean': float(self.data[col].mean()),
                    'std': float(self.data[col].std()),
                    'min': float(self.data[col].min()),
                    'max': float(self.data[col].max())
                }
        
        # Save summary to file
        with open('analysis/comprehensive_analysis_summary_v3.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"Analysis complete! Summary saved to: analysis/comprehensive_analysis_summary_v3.json")
        print(f"Plots saved to: analysis/ directory")
        
        return summary

def main():
    """Main analysis function"""
    # Try to find the most recent evaluation data
    possible_files = [
        'analysis/current_evaluations.csv',
        'analysis/sample_evaluations_rows.csv',
        'docs/sample_evaluations_rows.csv'
    ]
    
    csv_file = None
    for file_path in possible_files:
        if os.path.exists(file_path):
            csv_file = file_path
            break
    
    if not csv_file:
        print("No evaluation data file found. Please provide a CSV file or Supabase data.")
        return
    
    # Initialize analyzer
    analyzer = TTSAnalyzerV3(csv_path=csv_file)
    
    # Run comprehensive analysis
    analyzer.run_comprehensive_analysis()

if __name__ == "__main__":
    main()
