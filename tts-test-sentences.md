
# TTS 감정별 테스트 문장 리스트

## 🎯 Expressivity 비교 테스트 (2025-08-22)

### 테스트 목적
- **expressivity_none**: 기본 텍스트 (기존 방식)
- **expressivity_0.6**: 모든 텍스트에 "|0.6" 접미사 추가하여 expressivity 효과 측정

### voice_id 리스트
- **v001**: 688b02990486383d463c9d1a (male)
- **v002**: 689c69984c7990a1ddca2327 (female)

## 테스트 문장 구성
각 감정당 3개 문장:
1. **일치**: 감정과 어울리는 내용
2. **중립**: 감정과 무관한 중립적 내용
3. **반대**: 해당 감정과 반대되는 내용

**Expressivity 버전**:
- **기본**: 원본 텍스트
- **0.6**: 원본 텍스트 + "|0.6"

---

## 1. emotion_label: Angry
1. **일치**: "I can't believe you broke your promise again after everything we discussed!"
2. **중립**: "The meeting is scheduled for three o'clock in the conference room."
3. **반대**: "Your thoughtfulness and kindness truly made my day so much better."

## 2. emotion_label: Sad
1. **일치**: "I really miss the old days when everyone was still here together."
2. **중립**: "The report needs to be submitted by Friday afternoon without fail."
3. **반대**: "This is absolutely the best news I've heard all year long!"

## 3. emotion_label: Happy
1. **일치**: "I'm so thrilled about the wonderful surprise party you organized for me!"
2. **중립**: "Please remember to turn off the lights when you leave the office."
3. **반대**: "Everything seems to be going wrong and nothing works out anymore."

## 4. emotion_label: Whisper
1. **일치**: "Don't make any noise, everyone is sleeping in the next room."
2. **중립**: "The quarterly financial report shows steady growth in all departments."
3. **반대**: "Everyone needs to hear this important announcement right now!"

## 5. emotion_label: Toneup
1. **일치**: "Did you really win the grand prize in the competition?"
2. **중립**: "The train arrives at platform seven every hour on weekdays."
3. **반대**: "Everything is perfectly calm and there's nothing to worry about here."

## 6. emotion_label: Tonedown
1. **일치**: "Let me explain this matter in a very serious and professional manner."
2. **중립**: "The document contains information about the new policy changes."
3. **반대**: "This is so incredibly exciting and I can barely contain myself!"

## 7. emotion_vector_id: 68a7b5995b2b44d11cede93c (Excited)
1. **일치**: "We're going on the adventure of a lifetime starting tomorrow morning!"
2. **중립**: "The temperature today is expected to reach seventy-two degrees."
3. **반대**: "I'm too exhausted and drained to do anything at all today."

## 8. emotion_vector_id: 68a7b5a418fc7f54efec5b2f (Furious)
1. **일치**: "This is absolutely unacceptable and I demand an explanation immediately!"
2. **중립**: "The library closes at eight o'clock on weekday evenings."
3. **반대**: "I completely understand your position and I'm not upset at all."

## 9. emotion_vector_id: 68a7b5acb4a6c41c56a161e9 (Terrified)
1. **일치**: "Something is moving in the shadows and I don't know what it is!"
2. **중립**: "The coffee machine is located on the third floor break room."
3. **반대**: "I feel completely safe and protected in this wonderful place."

## 10. emotion_vector_id: 68a7b5beb4a6c41c56a161ea (두려움)
1. **일치**: "I'm really scared about what might happen if this goes wrong."
2. **중립**: "The new software update will be installed next Tuesday morning."
3. **반대**: "I have complete confidence that everything will work out perfectly."

## 11. emotion_vector_id: 68a7b5c218fc7f54efec5b31 (놀람)
1. **일치**: "Oh my goodness, I never expected to see you here today!"
2. **중립**: "The parking lot is located behind the main building entrance."
3. **반대**: "This is exactly what I predicted would happen all along."

## 12. emotion_vector_id: 68a7b5c5b4a6c41c56a161eb (흥분)
1. **일치**: "I can hardly wait to share this amazing news with everyone!"
2. **중립**: "Please fill out the form and return it to the front desk."
3. **반대**: "This is rather boring and I'm not interested in it at all."

---

## 사용 지침

### 파일명 규칙
```
{voice_id}_{text_idx}_{emotion}_{match_type}.wav

예시:
- v001_t001_angry_match.wav (감정 일치)
- v001_t002_angry_neutral.wav (중립)
- v001_t003_angry_opposite.wav (반대)
```

### 테스트 목적
- **일치 문장**: 감정 표현이 내용과 자연스럽게 어울리는지 확인
- **중립 문장**: 감정이 중립적 내용에도 잘 적용되는지 확인
- **반대 문장**: 극단적 상황에서 감정 표현의 강도와 명확성 확인

### 총 샘플 수
- 12개 감정 × 3개 문장 유형 = 36개 기본 조합
- 각 조합 × 6개 emotion_scale = 216개
- 2개 voice × 216개 = 432개 테스트 샘플