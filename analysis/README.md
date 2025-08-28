# TTS QA System Data Analysis

Analysis scripts for TTS QA evaluation data based on plan.md Mixed Effects Model requirements.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
python tts_analysis.py
```

## Analysis Overview

Based on plan.md Phase 3 requirements:

### Mixed Effects Model
```
Quality_Score = β₀ + β₁(voice) + β₂(text) + β₃(emotion) + β₄(scale) 
                + β₅(emotion×scale) + β₆(emotion_type) 
                + random(evaluator) + random(sample) + ε
```

### Key Variables
- **voice**: v001, v002
- **text_type**: match, neutral, opposite  
- **emotion**: 12 emotions (angry, sad, happy, etc.)
- **scale**: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0
- **emotion_type**: emotion_label vs emotion_vector
- **expressivity**: none vs 0.6

### Analysis Components

1. **Mixed Effects Analysis** - Main statistical model
2. **Automatic Quality Checks** - Audio issue detection from comments
3. **Threshold Analysis** - Critical cases (score < 4) and high performers (≥ 6)
4. **Parameter Impact Analysis** - Variable effects on outcomes

### Expected Results (from plan.md)
- voice_effect: p < 0.01, power 0.99
- text_effect: p < 0.01, power 0.95  
- emotion_main_effect: p < 0.01, power 0.75
- scale_effect: p < 0.01, power 0.88
- overall_power: 0.85

## Data Format

Input: `sample_evaluations_rows.csv`
- session_id, sample_id, scores (JSON), comment, timestamp, duration_ms
- Scores: quality, emotion, similarity (1-7 scale)

## Output

Comprehensive analysis report covering:
- Statistical significance of all parameters
- Quality issue patterns from evaluator comments
- Performance thresholds and problem cases
- Parameter optimization recommendations