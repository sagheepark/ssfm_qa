#!/usr/bin/env python3
"""
Comment Insights Extractor for TTS QA System
Separates research-relevant insights from product team action items

Focus Areas:
1. Research Insights: Emotion expression, scale boundaries, expressivity effectiveness
2. Product Team Issues: Technical problems requiring development attention
"""

import pandas as pd
import re
from collections import defaultdict

class CommentInsightsExtractor:
    def __init__(self, csv_path):
        """Initialize with evaluation data"""
        self.data = pd.read_csv(csv_path)
        self.research_insights = []
        self.product_issues = []
        
    def extract_insights(self):
        """Main extraction method"""
        print("=== Comment Insights Extraction ===")
        print(f"Processing {len(self.data)} evaluations...")
        
        for idx, row in self.data.iterrows():
            comment = str(row.get('comment', '')).strip()
            if not comment or comment == 'nan':
                continue
                
            sample_id = row.get('sample_id', '')
            session_info = row.get('session_id', '')
            scores = row.get('scores', '')
            
            # Classify comment type
            insight_type = self.classify_comment(comment)
            
            if insight_type == 'research':
                self.research_insights.append({
                    'sample_id': sample_id,
                    'session_info': session_info,
                    'comment': comment,
                    'scores': scores,
                    'category': self.categorize_research_insight(comment)
                })
            elif insight_type == 'product':
                self.product_issues.append({
                    'sample_id': sample_id,
                    'session_info': session_info,
                    'comment': comment,
                    'scores': scores,
                    'issue_type': self.categorize_product_issue(comment),
                    'severity': self.assess_severity(comment)
                })
                
        self.generate_reports()
    
    def classify_comment(self, comment):
        """Classify comment as research insight or product issue"""
        comment_lower = comment.lower()
        
        # Product issue indicators (technical problems)
        product_indicators = [
            '재생', '품질', '갈라짐', '깨짐', '튕김', '짤림', '끊김', 
            '로봇', '기계', '볼륨', '소리', '음성', '리버브', '스킵',
            '클리핑', '노이즈', '재생 안됨', '음질', '처음', '마지막',
            '리서치', '리포트', '공유'
        ]
        
        # Research insight indicators (emotion/scale effectiveness)
        research_indicators = [
            '감정', '해피', '화', '슬픔', '더', '덜', '강함', '약함',
            '레퍼런스가 더', '타겟이 더', '오히려', '반대', '다름',
            '비슷', '동일', '차이', '효과', '표현', '자연', '부자연'
        ]
        
        # Count indicators
        product_count = sum(1 for indicator in product_indicators if indicator in comment_lower)
        research_count = sum(1 for indicator in research_indicators if indicator in comment_lower)
        
        # Classification logic
        if product_count > research_count:
            return 'product'
        elif research_count > 0:
            return 'research'
        else:
            return 'product'  # Default to product issue for technical problems
    
    def categorize_research_insight(self, comment):
        """Categorize research insights by type"""
        comment_lower = comment.lower()
        
        if any(word in comment_lower for word in ['레퍼런스가 더', '레퍼런스보다', '오히려']):
            return 'reference_comparison'
        elif any(word in comment_lower for word in ['감정', '해피', '화', '슬픔']):
            return 'emotion_expression'
        elif any(word in comment_lower for word in ['스케일', '강함', '약함', '톤']):
            return 'intensity_scale'
        elif any(word in comment_lower for word in ['텍스트', '스크립트', '상반', '반대']):
            return 'text_alignment'
        else:
            return 'general_quality'
    
    def categorize_product_issue(self, comment):
        """Categorize product issues by type"""
        comment_lower = comment.lower()
        
        if any(word in comment_lower for word in ['재생 안됨', '재생이 안됨']):
            return 'playback_failure'
        elif any(word in comment_lower for word in ['스킵', '짤림', '끊김']):
            return 'audio_clipping'
        elif any(word in comment_lower for word in ['갈라짐', '깨짐', '튕김']):
            return 'audio_artifacts'
        elif any(word in comment_lower for word in ['로봇', '기계']):
            return 'robotic_voice'
        elif any(word in comment_lower for word in ['볼륨', '소리', '작게', '크게']):
            return 'volume_issues'
        elif any(word in comment_lower for word in ['리버브', '에코', '음질']):
            return 'audio_quality'
        else:
            return 'technical_other'
    
    def assess_severity(self, comment):
        """Assess severity of product issues"""
        comment_lower = comment.lower()
        
        high_severity = ['재생 안됨', '심각', '문제 많음', '로봇음성되어버림']
        medium_severity = ['갈라짐', '깨짐', '품질 문제', '부자연스러움']
        
        if any(word in comment_lower for word in high_severity):
            return 'high'
        elif any(word in comment_lower for word in medium_severity):
            return 'medium'
        else:
            return 'low'
    
    def generate_reports(self):
        """Generate comprehensive insight reports"""
        print(f"\n=== RESEARCH INSIGHTS SUMMARY ===")
        print(f"Total research insights: {len(self.research_insights)}")
        
        # Research insights by category
        research_categories = defaultdict(list)
        for insight in self.research_insights:
            research_categories[insight['category']].append(insight)
        
        for category, insights in research_categories.items():
            print(f"\n{category.upper().replace('_', ' ')} ({len(insights)} instances):")
            for insight in insights[:3]:  # Show top 3
                print(f"  • {insight['sample_id']}: {insight['comment']}")
            if len(insights) > 3:
                print(f"  ... and {len(insights)-3} more")
        
        print(f"\n=== PRODUCT TEAM ACTION ITEMS ===")
        print(f"Total product issues: {len(self.product_issues)}")
        
        # Product issues by type and severity
        product_categories = defaultdict(lambda: defaultdict(list))
        for issue in self.product_issues:
            product_categories[issue['issue_type']][issue['severity']].append(issue)
        
        for issue_type, severities in product_categories.items():
            print(f"\n{issue_type.upper().replace('_', ' ')}:")
            for severity in ['high', 'medium', 'low']:
                if severity in severities:
                    issues = severities[severity]
                    print(f"  {severity.upper()} PRIORITY ({len(issues)} issues):")
                    for issue in issues[:2]:  # Show top 2 per severity
                        print(f"    • {issue['sample_id']}: {issue['comment']}")
                    if len(issues) > 2:
                        print(f"    ... and {len(issues)-2} more")
        
        print(f"\n=== ACTIONABLE RECOMMENDATIONS ===")
        self.generate_recommendations()
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        
        # Research recommendations
        print("\nRESEARCH FINDINGS:")
        emotion_insights = [i for i in self.research_insights if i['category'] == 'emotion_expression']
        reference_insights = [i for i in self.research_insights if i['category'] == 'reference_comparison']
        
        if emotion_insights:
            print(f"  • Emotion Expression: {len(emotion_insights)} evaluations indicate emotion effectiveness issues")
            print("    → Analyze emotion scale boundaries and implementation methods")
        
        if reference_insights:
            print(f"  • Reference Comparison: {len(reference_insights)} cases where reference outperformed target")
            print("    → Question expressivity 0.6 parameter effectiveness")
        
        # Product team priorities
        print("\nPRODUCT TEAM PRIORITIES:")
        high_severity = [i for i in self.product_issues if i['severity'] == 'high']
        if high_severity:
            print(f"  🔴 HIGH PRIORITY: {len(high_severity)} critical audio issues")
            critical_types = defaultdict(int)
            for issue in high_severity:
                critical_types[issue['issue_type']] += 1
            for issue_type, count in critical_types.items():
                print(f"    → {issue_type.replace('_', ' ')}: {count} instances")
        
        playback_issues = [i for i in self.product_issues if i['issue_type'] == 'playback_failure']
        if playback_issues:
            print(f"  🟡 INFRASTRUCTURE: {len(playback_issues)} playback failures require investigation")
        
        audio_quality = [i for i in self.product_issues if 'audio' in i['issue_type']]
        if audio_quality:
            print(f"  🟠 AUDIO PIPELINE: {len(audio_quality)} rendering/quality issues need attention")

def main():
    """Main execution"""
    extractor = CommentInsightsExtractor('/Users/bagsanghui/ssfm30_qa/sample_evaluations_rows.csv')
    extractor.extract_insights()

if __name__ == "__main__":
    main()