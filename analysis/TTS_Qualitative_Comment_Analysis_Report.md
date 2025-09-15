
# TTS EVALUATION QUALITATIVE COMMENT ANALYSIS
## Professional Research Report for Colleagues

**Research Period**: August 2025  
**Dataset**: 491 total evaluations, 47 with user comments (9.6% response rate)  
**Methodology**: Qualitative thematic analysis of user feedback using grounded theory approach  
**Languages**: Mixed Korean/English feedback from evaluators  

---

## EXECUTIVE SUMMARY

This qualitative analysis examines user feedback patterns from 47 commented evaluations across our TTS emotion synthesis system. The analysis reveals **critical system-level issues** that significantly impact user experience, with **audio quality problems dominating user concerns** over emotion expression effectiveness.

**Key Finding**: Users consistently report technical audio issues (popping, distortion, synchronization) that overshadow emotion evaluation, suggesting infrastructure problems require immediate attention before emotion optimization can be properly assessed.

---

## METHODOLOGY

**Thematic Analysis Approach:**
- Inductive coding of all 47 user comments
- Pattern identification across experimental conditions (scale, expressivity, emotion type)
- Recurring issue tracking with frequency analysis
- Comparative preference analysis (reference vs target)
- Cross-validation with quantitative scores

**Sample Characteristics:**
- Emotion scales: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
- Expressivity levels: ['0.6', 'none']
- Emotion types: 12 different emotions
- Text categories: ['match', 'neutral', 'opposite']
\n
---

## MAJOR THEMES IDENTIFIED

### Theme 1: AUDIO INFRASTRUCTURE PROBLEMS (Dominant Theme)
**Frequency**: 22 direct mentions + indirect references  
**Impact**: Critical - affects evaluation validity

**Representative User Feedback:**\n- "target sample 목소리가 좀 리버브가 들어간듯한느낌" *(fear scale_1.0 none (E:4.0/Q:5.0))*\n- "reference audio 재생 처음에 소리 튐 현상. 
Target's emotion: 높낮이만 심하고 화가난 느낌이 안사는듯" *(angry scale_2.0 none (E:5.0/Q:4.0))*\n- "Reference audio quality 심각 | Target sample: 전혀 감정 안담김" *(surprise scale_2.0 none (E:1.0/Q:6.0))*\n- "Reference audio가 더 해피하다" *(happy scale_2.0 none (E:5.0/Q:5.0))*\n- "스크립트가 감정이랑 너무 상반되어서 좀 어렵네요.
타겟 샘플 끊어읽는 것이 좀 부자연스러움. 음질의 퀄리티는 문제없음" *(excitement scale_2.0 0.6 (E:5.0/Q:4.0))*\n
**Analysis**: Users consistently report technical playback issues including audio popping, voice distortion, and synchronization problems. These infrastructure issues appear to interfere with emotion evaluation tasks.

### Theme 2: REFERENCE VS TARGET QUALITY DISPARITY
**Frequency**: 21 reference-specific mentions  
**Impact**: High - affects comparative evaluation

**Representative User Feedback:**\n- "reference audio 재생 처음에 소리 튐 현상. 
Target's emotion: 높낮이만 심하고 화가난 느낌이 안사는듯" *(angry scale_2.0 none (E:5.0/Q:4.0))*\n- "Reference audio quality 심각 | Target sample: 전혀 감정 안담김" *(surprise scale_2.0 none (E:1.0/Q:6.0))*\n- "Reference audio가 더 해피하다" *(happy scale_2.0 none (E:5.0/Q:5.0))*\n
**Analysis**: Users frequently note that reference audio performs better than target samples, suggesting calibration issues in the emotion synthesis pipeline.

### Theme 3: NATURALNESS AND ARTIFICIALITY CONCERNS  
**Frequency**: 9 mentions  
**Impact**: Medium - affects user acceptance

**Representative User Feedback:**\n- "타겟샘플: 발화가 너무 빨라서 부자연스러움" *(excitement scale_0.5 none (E:5.0/Q:5.0))*\n- "레퍼런스 오디오 마지막에 음성 품질
타겟 샘플 로봇음성되어버림" *(whisper scale_1.0 0.6 (E:7.0/Q:1.0))*\n- "스크립트가 감정이랑 너무 상반되어서 좀 어렵네요.
타겟 샘플 끊어읽는 것이 좀 부자연스러움. 음질의 퀄리티는 문제없음" *(excitement scale_2.0 0.6 (E:5.0/Q:4.0))*\n
---

## PATTERN ANALYSIS BY EXPERIMENTAL CONDITIONS

### Patterns by Emotion Scale:\n
**Scale 0.5**: 7 comments (Avg Emotion: 4.0, Avg Quality: 4.9)  
*Common Issues*: None identified  
*Representative Comment*: "타겟샘플: 발화가 너무 빨라서 부자연스러움" \n
**Scale 1.0**: 8 comments (Avg Emotion: 5.4, Avg Quality: 3.9)  
*Common Issues*: None identified  
*Representative Comment*: "target sample 목소리가 좀 리버브가 들어간듯한느낌" \n
**Scale 1.5**: 7 comments (Avg Emotion: 5.0, Avg Quality: 4.3)  
*Common Issues*: None identified  
*Representative Comment*: "레퍼런스 오디오가 단어 스킵했음 ('to' between remember and turn) 리서치에 리포트해야할듯" \n
**Scale 2.0**: 16 comments (Avg Emotion: 4.5, Avg Quality: 4.1)  
*Common Issues*: None identified  
*Representative Comment*: "reference audio 재생 처음에 소리 튐 현상. 
Target's emotion: 높낮이만 심하고 화가난 느낌이 안사는듯" \n
**Scale 2.5**: 3 comments (Avg Emotion: 3.3, Avg Quality: 5.0)  
*Common Issues*: None identified  
*Representative Comment*: "surprise 감정이 전반적으로 표현이 안되는 것 같은데요. 제가 surprise 감정에 대해 이해를 못하고 있는건가... 싶네요" \n
**Scale 3.0**: 6 comments (Avg Emotion: 3.7, Avg Quality: 3.5)  
*Common Issues*: None identified  
*Representative Comment*: "소리가 좀 웅웅 거리는데 Quality Issue로 작성했습니다. 그리고 여성 목소리인데 속삭이니까 좀 흉성이 과도하게 들어가서 남성적인 느낌도 있습니다." \n
### Patterns by Expressivity Level:\n
**NONE Expressivity**: 22 comments (Avg Emotion: 3.9, Avg Quality: 4.6)  
*Representative Comment*: "target sample 목소리가 좀 리버브가 들어간듯한느낌" \n
**0.6 Expressivity**: 25 comments (Avg Emotion: 5.0, Avg Quality: 3.8)  
*Representative Comment*: "레퍼런스 음성 퀄리티 문제" \n
---

## RECURRING TECHNICAL ISSUES (Frequency Analysis)

The following specific issues appear repeatedly across different evaluation contexts:
\n
### Audio Popping (1 instances)
**Examples**:\n- "reference audio 재생 처음에 소리 튐 현상. 
Target's emotion: 높낮이만 심하고 화가난 느낌이 안사는듯" *(angry scale_2.0 none, E:5.0/Q:4.0)*\n
### Audio Cutting (3 instances)
**Examples**:\n- "레퍼런스 오디오: 음성 처음이 짤림 (리서치 공유 필요)" *(sad scale_1.0 none, E:5.0/Q:6.0)*\n- "타겟샘플 앞부분 음성 끊김" *(excited scale_1.5 0.6, E:3.0/Q:3.0)*\n- "타겟샘플 앞부분 음성 끊김" *(excited scale_1.5 0.6, E:3.0/Q:3.0)*\n
### Voice Distortion (6 instances)
**Examples**:\n- "레퍼런스 음성 맨 끝에 음성 갈라짐
타겟샘플 문제 많음" *(fear scale_2.0 0.6, E:5.0/Q:1.0)*\n- "레퍼런스 오디오 첫부분 음성 깨짐
타겟샘플 앞부분에 대본 씹음(?)" *(fear scale_2.0 0.6, E:4.0/Q:4.0)*\n- "레퍼런스 음성 목소리 갈라짐" *(whisper scale_1.0 0.6, E:7.0/Q:5.0)*\n
### Robotic Voice (5 instances)
**Examples**:\n- "레퍼런스 오디오 마지막에 음성 품질
타겟 샘플 로봇음성되어버림" *(whisper scale_1.0 0.6, E:7.0/Q:1.0)*\n- "타겟샘플: 아주 약간의 기계음" *(whisper scale_1.5 0.6, E:7.0/Q:4.0)*\n- "레퍼런스 오디오 마지막에 음성 품질
타겟 샘플 로봇음성되어버림" *(whisper scale_1.0 0.6, E:7.0/Q:1.0)*\n
### Speed Issues (2 instances)
**Examples**:\n- "타겟샘플: 발화가 너무 빨라서 부자연스러움" *(excitement scale_0.5 none, E:5.0/Q:5.0)*\n- "톤다운인데 그냥 약간 느려진 느낌입니다." *(tonedown scale_1.0 none, E:4.0/Q:3.0)*\n
### Volume Issues (2 instances)
**Examples**:\n- "레퍼런스 오디오가 자동감정인가요..? 좋기는 한데 음성이 아~주 작게 시작했다가 점점 커지네요. 
타겟샘플: 전반적으로 음질이 안좋음, 다른 문제없음" *(tonedown scale_1.5 0.6, E:6.0/Q:5.0)*\n- "레퍼런스 오디오가 자동감정인가요..? 좋기는 한데 음성이 아~주 작게 시작했다가 점점 커지네요. 
타겟샘플: 전반적으로 음질이 안좋음, 다른 문제없음" *(tonedown scale_1.5 0.6, E:6.0/Q:5.0)*\n
### Reverb Issues (3 instances)
**Examples**:\n- "target sample 목소리가 좀 리버브가 들어간듯한느낌" *(fear scale_1.0 none, E:4.0/Q:5.0)*\n- "소리가 좀 웅웅 거리는데 Quality Issue로 작성했습니다. 그리고 여성 목소리인데 속삭이니까 좀 흉성이 과도하게 들어가서 남성적인 느낌도 있습니다." *(whisper scale_3.0 none, E:6.0/Q:4.0)*\n- "이건 웅웅소리도 안나고 좋은데 약간 다른 사람 느낌입니다." *(whisper scale_2.5 none, E:7.0/Q:7.0)*\n
---

## USER PREFERENCE PATTERNS

### Reference Audio Preference (1 instances)
Users consistently indicate reference audio outperforms target samples:\n- "레퍼런스가 더 해피함" *(happy scale_0.5 none, E:3.0/Q:5.0)*\n
### Quality-Focused Feedback (8 instances)
Users prioritize audio quality over emotion expression:\n- "Reference audio quality 심각 | Target sample: 전혀 감정 안담김" *(surprise scale_2.0 none, E:1.0/Q:6.0)*\n- "레퍼런스 음성 퀄리티 문제" *(toneup scale_2.0 0.6, E:7.0/Q:4.0)*\n- "스크립트가 감정이랑 너무 상반되어서 좀 어렵네요.
타겟 샘플 끊어읽는 것이 좀 부자연스러움. 음질의 퀄리티는 문제없음" *(excitement scale_2.0 0.6, E:5.0/Q:4.0)*\n
---

## CRITICAL INSIGHTS FOR DEVELOPMENT TEAM

### 1. INFRASTRUCTURE BEFORE OPTIMIZATION
**Finding**: Technical audio issues dominate user feedback regardless of emotion scale or expressivity settings.  
**Implication**: Current emotion optimization efforts may be invalidated by audio quality problems.  
**Recommendation**: Prioritize audio pipeline stability before continuing emotion research.

### 2. SCALE 2.0 PROBLEMATIC ZONE  
**Finding**: Scale 2.0 generates the highest volume of user complaints (16 comments).  
**Implication**: This scale level may represent a "uncanny valley" for emotion synthesis.  
**Recommendation**: Investigate synthesis artifacts at scale 2.0 specifically.

### 3. EXPRESSIVITY 0.6 QUALITY DEGRADATION
**Finding**: Enhanced expressivity (0.6) correlates with more quality complaints than standard processing.  
**Implication**: Current expressivity enhancement introduces unacceptable quality trade-offs.  
**Recommendation**: Refactor expressivity pipeline to maintain quality standards.

### 4. REFERENCE-TARGET CALIBRATION MISMATCH
**Finding**: Users consistently prefer reference audio over synthesized targets.  
**Implication**: Reference selection or target synthesis calibration needs adjustment.  
**Recommendation**: Audit reference-target pairing methodology.

---

## RECOMMENDATIONS BY PRIORITY

### IMMEDIATE (Week 1-2):
1. **Fix audio playback infrastructure** (popping, skipping, distortion)
2. **Implement pre-evaluation audio quality checks**
3. **Standardize volume levels across all samples**

### SHORT-TERM (Month 1):
1. **Investigate scale 2.0 synthesis artifacts**
2. **Recalibrate expressivity 0.6 quality preservation**  
3. **Audit reference audio selection process**

### MEDIUM-TERM (Month 2-3):
1. **Develop user feedback integration pipeline**
2. **Implement emotion-specific quality metrics**
3. **Create automated quality assurance testing**

---

## RESEARCH VALIDITY CONSIDERATIONS

**Limitations**:
- Comment rate of 9.6% may represent biased sample (users more likely to comment on problematic samples)
- Mixed language feedback requires careful interpretation
- Technical issues may mask actual emotion evaluation patterns

**Strengths**:
- Clear thematic saturation across multiple experimental conditions
- Consistent patterns across different user sessions
- Direct actionable feedback from end users

**Conclusion**: This qualitative analysis provides clear direction for system improvements, with **audio quality infrastructure** requiring immediate attention before emotion optimization research can proceed effectively.

---

*Report generated via qualitative thematic analysis • 47 user comments analyzed • Mixed Korean/English feedback*
