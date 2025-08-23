# TTS QA 자동화 테스트 시스템 구축 계획서

## 🎯 현재 진행 상황 (2025-08-23) - COMPLETE AUDIO REQUIREMENTS

### ✅ 완료된 작업
1. **emotion_label 기반 음성 생성 완료**
   - 258개 음성 파일 성공적으로 생성 (public/voices/)
   - 6개 emotion_labels (angry, sad, happy, whisper, toneup, tonedown)
   - v001, v002 voice별로 생성 완료

2. **emotion_vector_id 설정 및 테스트**
   - 새로운 emotion_vector_ids 생성 및 검증 완료
   - API 연동 테스트 성공 (dev.icepeak.ai)
   - 필수 파라미터 확인: bp_c_l=true, style_label="normal-1"
   - emotion_vector 기반 88개 파일 생성 완료 (40% 진행)

3. **보안 설정 완료**
   - .gitignore 업데이트로 민감 정보 보호
   - API 토큰 및 개인 정보 제외
   - Vercel 배포 환경 유지

### 🚀 새로운 목표: Expressivity 비교 테스트
**목적**: expressivity 파라미터 효과 측정
- **expressivity_none**: 기본 버전 (현재 생성 방식)
- **expressivity_0.6**: 모든 텍스트에 "|0.6" 접미사 추가

**확장된 테스트 매트릭스**:
```
총 테스트 샘플 = 1,728개
- expressivity 버전: 2개 (none, 0.6)
- voice_id: 2개 (v001, v002)  
- emotion 타입: 12개 (6 emotion_labels + 6 emotion_vectors)
- text 타입: 3개 (match, neutral, opposite)
- emotion_scale: 6개 (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
```

### 🔧 진행 중인 작업 (2025-08-23)
- **Complete Reference 오디오 생성**
  - 144개 reference 오디오 생성 중 (72 × 2 expressivity)
  - 각 emotion × text_type 조합의 고유 텍스트 사용
  - Reference는 감정 없는 중립 baseline (style_label="normal-1" only)
  
- **오디오 파일 최종 구성**
  - Target audios: 864개 (432 × 2 expressivity) 
  - Reference audios: 144개 (72 × 2 expressivity)
  - 총 1,008개 오디오 파일

### 📊 핵심 차별점 (이번 실험 설계)
1. **텍스트 고유성**: 각 emotion × text_type 조합이 고유한 텍스트 사용 (72개 고유 텍스트)
2. **정확한 Reference 매칭**: voice_id + emotion + text_type으로 정확히 매칭
3. **Expressivity 비교**: 동일 텍스트로 none vs 0.6 효과 측정 가능
4. **Scale 효과 분석**: 각 reference와 6개 scale 비교로 감정 강도 효과 측정

### 📝 주요 변경사항
- **Actor IDs 업데이트**: 
  - v001: 688b02990486383d463c9d1a (male)
  - v002: 689c69984c7990a1ddca2327 (female)
- **emotion_vector_ids 전체 교체** (위 참조)
- **API 파라미터 수정**: emotion_label 제거, bp_c_l 추가

## 📋 프로젝트 개요

### 목적
Text-to-Speech 모델의 품질을 체계적으로 검증하기 위한 자동화된 테스트 시스템 구축

### 핵심 목표
1. 다양한 파라미터 조합에 대한 음성 자동 생성
2. Reference 음성 대비 품질 평가
3. 변수별 영향도 파악 및 문제 패턴 식별

## 🏗️ 시스템 아키텍처

### 1. 테스트 매트릭스 - COMPLETE AUDIO REQUIREMENTS

#### 1.1 Target Audio Requirements (감정이 적용된 테스트 오디오)
```
총 Target 오디오 = 864개 (432개 × 2 expressivity types)
- voice_id: 2개 (v001, v002)
- emotions: 12개 (emotion_label 6개 + emotion_vector_id 6개)
- text_types: 3개 (match, neutral, opposite) - 각 감정별로 다른 텍스트
- emotion_scale: 6단계 (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
- expressivity: 2개 (none, 0.6)

계산: 2 voices × 12 emotions × 3 text_types × 6 scales × 2 expressivity = 864개
```

#### 1.2 Reference Audio Requirements (중립 baseline 오디오)
```
총 Reference 오디오 = 144개 (72개 × 2 expressivity types)
- voice_id: 2개 (v001, v002)
- emotions: 12개 (각 감정의 고유 텍스트 사용)
- text_types: 3개 (match, neutral, opposite) - 각각 다른 텍스트
- expressivity: 2개 (none, 0.6)
- 설정: style_label="normal-1" only (no emotion)

계산: 2 voices × 12 emotions × 3 text_types × 2 expressivity = 144개

중요: 각 reference는 동일한 voice_id, emotion, text_type을 가진 
      6개의 다른 scale target 오디오와 비교됨
```

#### 1.3 총 오디오 파일 수
```
총 오디오 파일 = 1,008개
- Target audios: 864개
- Reference audios: 144개
```

#### 파라미터 상세

**Emotion 구성 (12개)**
```yaml
emotion_labels: 
  - angry    # "I can't believe you broke your promise again!"
  - sad      # "I really miss the old days when everyone was here together."
  - happy    # "I'm so thrilled about the wonderful surprise party!"
  - whisper  # "Don't make any noise, everyone is sleeping in the next room."
  - toneup   # "Did you really win the grand prize in the competition?"
  - tonedown # "Let me explain this matter in a very serious manner."

emotion_vector_ids (UPDATED 2025-08-22):
  - 68a7b5995b2b44d11cede93c  # Excited: "We're going on the adventure of a lifetime!"
  - 68a7b5a418fc7f54efec5b2f  # Furious: "This is absolutely unacceptable and I demand an explanation!"
  - 68a7b5acb4a6c41c56a161e9  # Terrified: "Something is moving in the shadows and I don't know what!"
  - 68a7b5beb4a6c41c56a161ea  # 두려움: "I'm really scared about what might happen if this goes wrong."
  - 68a7b5c218fc7f54efec5b31  # 놀람: "Oh my goodness, I never expected to see you here today!"
  - 68a7b5c5b4a6c41c56a161eb  # 흥분: "I can hardly wait to share this amazing news with everyone!"

emotion_scales: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

text_types: [match, neutral, opposite]  # 감정 일치, 중립, 반대
```

#### 파라미터 규칙
- `style_label`과 `emotion_vector_id`는 상호 배타적
- `emotion_vector_id` 사용 시 → `style_label = "normal-1"`
- `style_label ≠ "normal-1"` 시 → `emotion_vector_id` 제거
- `emotion_scale`은 `emotion_vector_id` 사용 시에만 적용

#### Reference 음성 정의 (CORRECTED 2025-08-23)
**핵심 원칙**: Reference는 감정이 없는 중립적 baseline
- 각 `voice_id × text` 조합당 1개의 reference 음성
- 설정:
  - `style_label: "normal-1"` (필수)
  - `emotion_label: null` (감정 라벨 없음)
  - `emotion_vector_id: null` (감정 벡터 없음)
  - `emotion_scale: 1.0` (기본값)
- **매칭 규칙**: 
  - 하나의 reference는 동일한 voice_id와 text를 가진 6개 scale의 target 오디오와 비교
  - 예: v001_match_reference.wav는 v001_match_emo_angry의 모든 scale (0.5~3.0)과 비교

### 2. 파일명 규칙 (COMPLETE SPECIFICATION)

```
Target 오디오 형식: {voice_id}_{text_type}_{emotion_type}_{emotion_value}_scale_{scale}.wav
Reference 오디오 형식: {voice_id}_{text_type}_reference_{emotion}.wav

예시 - Target 오디오:
- emotion_label: v001_match_emo_angry_scale_1.5.wav
- emotion_vector: v001_neutral_vec_excited_scale_2.0.wav

예시 - Reference 오디오:
- v001_match_reference_angry.wav (angry의 match 텍스트, 감정 없음)
- v001_neutral_reference_sad.wav (sad의 neutral 텍스트, 감정 없음)
- v002_opposite_reference_happy.wav (happy의 opposite 텍스트, 감정 없음)

폴더 구조:
public/voices/
├── expressivity_none/      # 기본 텍스트
│   ├── [432 target files]  # 감정 적용됨
│   └── [72 reference files] # 감정 없음, normal-1
└── expressivity_0.6/        # 텍스트에 |0.6 추가
    ├── [432 target files]   # 감정 적용됨
    └── [72 reference files] # 감정 없음, normal-1

Reference 매칭 규칙 (IMPLEMENTED):
- v001_match_emo_angry_scale_*.wav → v001_match_reference_angry.wav
- v002_neutral_vec_excited_scale_*.wav → v002_neutral_reference_excited.wav
- v001_opposite_emo_happy_scale_*.wav → v001_opposite_reference_happy.wav

자동 매칭 공식: {voice_id}_{text_type}_reference_{emotion}.wav
- voice_id: 동일한 화자
- text_type: 동일한 텍스트 유형 (match/neutral/opposite)  
- emotion: 동일한 감정의 텍스트 내용 (감정은 제거됨)
```

### 3. Reference Connection Implementation (ACTIVE)

#### 3.1 자동 Reference 매칭 시스템
```javascript
// 실제 구현된 매칭 로직 (src/lib/sampleData.ts)
function getReferenceFilename(sample: TTSSample): string {
  return `${sample.voice_id}_${sample.text_type}_reference_${sample.emotion_value}.wav`;
}

// 예시 매칭
Target:    "v001_match_emo_angry_scale_1.5.wav"
Reference: "v001_match_reference_angry.wav"
Text:      "I can't believe you broke your promise again!" (동일)
Emotion:   Target(angry 적용) vs Reference(감정 없음, normal-1)
```

#### 3.2 UI에서의 Reference 표시
```typescript
// AudioPlayer 컴포넌트에서 자동으로 reference 표시
<AudioPlayer sample={sample} isReference={true} />  // Reference audio
<AudioPlayer sample={sample} isReference={false} /> // Target audio

// 각 target sample마다 matching reference가 자동으로 함께 표시됨
```

#### 3.3 Reference 검증 완료
```
✓ 144개 reference 파일 생성 완료 (72 × 2 expressivity)
✓ 자동 매칭 로직 구현 완료 (getReferenceFilename 함수)
✓ UI 연결 완료 (AudioPlayer 컴포넌트)
✓ 매칭 테스트 완료 (모든 voice × emotion × text_type 조합)
```

### 4. 샘플링 전략 (Dynamic Random Sampling)

```python
sampling_strategy = {
    "method": "dynamic_random_with_auto_reference",
    "total_target_samples": 432,  # 2 voice × 12 emotion × 3 text × 6 scale (per expressivity)
    "total_reference_samples": 72,  # 2 voice × 12 emotion × 3 text (no emotion, per expressivity)
    "total_unique_texts": 72,  # Each emotion × text_type has unique content
    "samples_per_session": 25,  # 세션당 랜덤 선택 (targets only)
    "total_sessions": 56,  # 14명 × 4세션
    "total_evaluations": 1400,  # 56 × 25
    
    "coverage_analysis": {
        "avg_evals_per_sample": 3.24,  # 1400 / 432
        "min_1_eval_probability": "96.2%",
        "min_2_evals_probability": "78%"
    },
    
    "sampling_rules": {
        "매 세션마다": "432개 target 중 25개 새로 랜덤 선택",
        "중복 허용": "세션 간 중복 가능, 세션 내 중복 불가",
        "reference 자동 표시": "각 target과 매칭되는 reference 자동 표시 (구현완료)",
        "reference 매칭": "voice_id + emotion + text_type이 같은 reference 연결 (구현완료)",
        "균형 유지": "완전 랜덤이지만 extreme bias 방지",
        "텍스트 고유성": "각 emotion × text_type 조합은 고유한 텍스트 사용 (72개 unique)",
        "실시간 연결": "UI에서 target 선택시 matching reference 즉시 표시"
    },
    
    "expected_power": {
        "voice_effect": 0.99,
        "text_effect": 0.95,
        "emotion_effect": 0.75,
        "scale_effect": 0.88,
        "overall": 0.85  # 샘플 수 증가로 약간 감소
    }
}
```

## 💻 구현 컴포넌트

### Phase 1: 음성 생성 자동화 스크립트

```python
# 필요한 모듈들
modules = {
    "ConfigManager": "테스트 설정 및 파라미터 관리",
    "APIClient": "TTS API 호출 및 에러 처리",
    "FileManager": "음성 파일 저장 및 메타데이터 관리",
    "TestGenerator": "테스트 케이스 조합 생성",
    "BatchProcessor": "대량 요청 처리 및 rate limiting",
    "ReferenceManager": "오디오/프롬프트 레퍼런스 관리"
}

# TTS API 워크플로우 (4단계 비동기 처리)
# API 제약사항 및 규칙 (실제 테스트 결과 기반)
api_constraints = {
    "style_label": "항상 'normal-1' 고정 (다른 값 지원 안함)",
    "emotion_control": "emotion_label 또는 emotion_vector_id 중 하나만 사용",
    "mutual_exclusion": "emotion_vector_id 사용시 emotion_label은 None/빈값",
    "emotion_scale": "0.5 ~ 3.0 범위에서 감정 강도 조절"
}

api_workflow = {
    "step1_request": {
        "url": "https://dev.icepeak.ai/api/speak/batch/post",
        "method": "POST",
        "headers": {"Authorization": "Bearer TOKEN"},
        "data": [
            {
                "text": "string",
                "actor_id": "string (voice_001: 688b02990486383d463c9d1a, voice_002: 689c693264acbc0a5b9fb0e5)", 
                "style_label": "normal-1",  # 항상 고정값
                "emotion_label": "string (optional, emotion_vector_id와 상호배타)",
                "emotion_vector_id": "string (optional, emotion_label과 상호배타)",
                "emotion_scale": "float (0.5-3.0)",
                "tempo": 1,
                "pitch": 0,
                "lang": "auto",
                "mode": "one-vocoder",
                "retake": True,
                "adjust_lastword": 0,
                "style_label_version": "v1"
            }
        ],
        "response": {"result": {"speak_urls": ["url1", "url2"]}}
    },
    
    "step2_poll": {
        "url": "https://dev.icepeak.ai/api/speak/batch/get", 
        "method": "POST",
        "headers": {"Authorization": "Bearer TOKEN"},
        "data": ["speak_url1", "speak_url2"],
        "polling": "5초마다 최대 20회 시도",
        "response": {"result": [{"status": "done", "audio": {"url": "audio_url"}}]}
    },
    
    "step3_get_download_url": {
        "url": "{audio_url}/cloudfront",
        "method": "GET", 
        "headers": {"Authorization": "Bearer TOKEN"},
        "response": {"result": "final_download_url"}
    },
    
    "step4_download": {
        "url": "final_download_url",
        "method": "GET",
        "headers": "none",
        "response": "binary audio data"
    }
}

# 테스트 문장 파일 참조
test_sentences_reference = {
    "file": "tts-test-sentences.md",
    "purpose": "각 감정별 3가지 유형의 테스트 문장 제공",
    "structure": {
        "match": "감정과 어울리는 내용",
        "neutral": "감정과 무관한 중립적 내용", 
        "opposite": "해당 감정과 반대되는 내용"
    },
    "emotions": [
        "Angry", "Sad", "Happy", "Whisper", "Toneup", "Tonedown",
        "Excited", "Furious", "Terrified", "두려움", "놀람", "흥분"
    ],
    "usage": "각 감정의 style_label 또는 emotion_vector_id와 매핑하여 사용"
}

# 레퍼런스 매핑
reference_mapping = {
    "audio1": "path/to/audio_reference_1.wav",
    "audio2": "path/to/audio_reference_2.wav",
    "audio3": "path/to/audio_reference_3.wav",
    "prompt1": "감정 프롬프트 텍스트 1",
    "prompt2": "감정 프롬프트 텍스트 2",
    "prompt3": "감정 프롬프트 텍스트 3"
}
```

#### 구현 순서
1. **설정 파일 생성** (`config.yaml`)
   ```yaml
   api:
     endpoint: "YOUR_API_ENDPOINT"
     rate_limit: 10  # requests per second
     retry_attempts: 3
   
   storage:
     output_dir: "./generated_voices"
     metadata_db: "./metadata.db"
     reference_dir: "./references"
   
   test_parameters:
     voice_ids: ["voice_001", "voice_002"]
     texts: ["text_1", "text_2", "text_3"]
     
     emotion_vectors:
       audio_based:
         - name: "excited"
           id: "68a6b0ca2edfc11a25045538"
           reference: "references/audio/excited.wav"
         - name: "furious"
           id: "68a6b0d2b436060efdc6bc80"
           reference: "references/audio/furious.wav"
         - name: "terrified"
           id: "68a6b0d9b436060efdc6bc82"
           reference: "references/audio/terrified.wav"
       
       prompt_based:
         - name: "두려움"
           id: "68a6b0f7b436060efdc6bc83"
           prompt: "두려움이 가득한 목소리"
         - name: "놀람"
           id: "68a6b10255e3b2836e609969"
           prompt: "놀란 목소리"
         - name: "흥분"
           id: "68a6b1062edfc11a2504553b"
           prompt: "흥분된 목소리"
     
     style_labels: ["normal-1", "style-2", "style-3", "style-4", "style-5", "style-6", "style-7"]
     emotion_scales: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
   ```

2. **샘플링 및 생성**
   ```python
   def generate_full_sample_pool():
       """
       1. 전체 432개 조합 생성
          - 2 voice × 3 text × 6 reference = 6개
          - 2 voice × 3 text × 12 emotion × 6 scale = 432개
       2. 모든 샘플에 대해 음성 생성
       3. 메타데이터와 함께 저장
       """
       samples = []
       
       # Reference 샘플 (6개)
       for voice in voices:
           for text in texts:
               samples.append({
                   'type': 'reference',
                   'style_label': 'normal-1',
                   'emotion_scale': 1.0
               })
       
       # Style 샘플 (216개)
       for voice in voices:
           for text in texts:
               for style in style_labels[1:]:  # normal-1 제외
                   for scale in emotion_scales:
                       samples.append({
                           'type': 'style',
                           'style_label': style,
                           'emotion_scale': scale
                       })
       
       # Emotion vector 샘플 (216개)
       for voice in voices:
           for text in texts:
               for emotion_vector in emotion_vectors:
                   for scale in emotion_scales:
                       samples.append({
                           'type': 'emotion_vector',
                           'emotion_vector_id': emotion_vector,
                           'style_label': 'normal-1',
                           'emotion_scale': scale
                       })
       
       return samples  # 총 438개 (6 ref + 432 variations)
   
   def get_session_samples():
       """
       1. 438개 풀에서 25개 랜덤 선택
       2. 세션 ID 생성
       3. 선택된 샘플 리스트 반환
       4. 로그에 세션별 샘플 기록
       """
       import random
       import uuid
       
       all_samples = load_all_samples()  # 438개
       session_samples = random.sample(all_samples, 25)
       session_id = str(uuid.uuid4())
       
       return {
           'session_id': session_id,
           'samples': session_samples
       }
   ```

### Phase 2: QA 테스트 플랫폼 - Vercel 배포

#### 2.0 배포 전략 (Updated with Supabase Integration)
```yaml
deployment:
  platform: "Vercel"
  repository: "https://github.com/sagheepark/ssfm_qa.git"
  framework: "Next.js 14 with App Router"
  audio_hosting: "Supabase Storage"
  database: "Supabase PostgreSQL"
  realtime: "Supabase Real-time subscriptions"
  
workflow:
  1. "✅ Create Next.js TTS QA application" 
  2. "✅ Push to GitHub repository (without large audio files)"
  3. "✅ Deploy to Vercel with automatic CD/CI"
  4. "🔄 Setup Supabase project for audio storage & database"
  5. "🔄 Upload all 252 audio files (216 samples + 36 references) to Supabase Storage"
  6. "🔄 Create evaluation response tables in Supabase"
  7. "🔄 Update app to use Supabase URLs for audio files"

supabase_integration:
  storage:
    bucket: "tts-audio-samples"
    structure: "/voices/{filename}.wav"
    cdn_delivery: "Global edge cache for fast audio loading"
    
  database_schema:
    tables:
      - "qa_sessions (session_id, user_id, started_at, completed_at)"
      - "sample_evaluations (session_id, sample_id, quality, emotion, similarity, comment, timestamp)"
      - "sample_metadata (sample_id, filename, voice_id, text_type, emotion_type, scale, text_content)"
      
  advantages:
    - "Audio files served from CDN (faster loading)"
    - "28MB+ audio files don't count against Vercel limits"
    - "Database for response analysis and aggregation"
    - "Real-time progress tracking across evaluators"
    - "Scalable for multiple evaluation sessions"

features:
  - "✅ Single Page Application (SPA)"
  - "✅ Dynamic random sampling (25 samples per session)"
  - "✅ Client-side progress tracking with localStorage"
  - "✅ Mobile-responsive design"
  - "🔄 Audio streaming from Supabase Storage CDN"
  - "🔄 Real-time evaluation data collection"
  - "🔄 Progress analytics dashboard"
```

#### 2.1 평가 체계 (Vercel 최적화)

```python
evaluation_axes = {
    "퀄리티": {
        "description": "음성의 전반적인 품질 및 기술적 완성도",
        "scale": [1, 2, 3, 4, 5, 6, 7],
        "guidelines": {
            7: "완벽한 품질, 상용 수준",
            6: "매우 좋은 품질",
            5: "좋은 품질, 미세한 문제",
            4: "보통, 눈에 띄는 문제 있음",
            3: "품질 문제 있지만 사용 가능",
            2: "심각한 품질 문제",
            1: "사용 불가능한 수준"
        },
        "sub_items": ["노이즈", "클리핑", "끊김", "선명도"]
    },
    "감정_표현력": {
        "description": "의도한 감정이 얼마나 잘 표현되었는가",
        "scale": [1, 2, 3, 4, 5, 6, 7],
        "guidelines": {
            7: "완벽한 감정 표현",
            6: "매우 좋은 감정 표현",
            5: "좋은 감정 표현",
            4: "보통의 감정 표현",
            3: "부족한 감정 표현",
            2: "매우 부족한 감정 표현",
            1: "감정이 전혀 표현되지 않음"
        },
        "reference_required": True  # audio/prompt reference 표시
    },
    "화자_유사도": {
        "description": "원본 화자와 얼마나 유사한가",
        "scale": [1, 2, 3, 4, 5, 6, 7],
        "guidelines": {
            7: "완전히 동일한 화자",
            6: "거의 동일한 화자",
            5: "유사하지만 약간의 차이",
            4: "비슷한 편",
            3: "차이가 느껴짐",
            2: "확실히 다른 화자",
            1: "완전히 다른 화자"
        },
        "reference_audio": "필수"
    }
}
```

#### 2.2 웹 인터페이스 구조 (Updated with Editable Results)

```markdown
### 단일 페이지 테스트 인터페이스
1. **시작 화면**
   - 간단한 안내 문구
   - "테스트 시작" 버튼
   - 예상 소요 시간 표시

2. **평가 화면 (Enhanced Navigation & UX)**
   - 진행률 표시 (현재/전체)
   - Reference 음성 재생
   - 레퍼런스 표시:
     * Audio Reference: 원본 오디오 재생 버튼
     * Prompt Reference: 텍스트 프롬프트 표시
   - 테스트 음성 재생
   - 3축 평가 입력 (7점 척도)
   - 선택적 코멘트 입력
   - **Enhanced Navigation:**
     * Previous button (always available)
     * **Primary CTA Next button (prominent, only active when all 3 scores filled)**
     * Separated control section:
       - Reset Session button (destructive action)
       - Stop & Submit button (saves all data to database)
   
3. **종료 화면**
   - 완료 메시지 (after Stop & Submit or completing all samples)
   - Session summary (number of samples evaluated)
   - "새 세션 시작" 버튼

### Enhanced State Management & Data Flow
- **Local-only evaluation storage**: Results stored in localStorage only
- **No per-sample database writes**: Individual evaluations NOT saved to database immediately
- **Batch data submission**: All evaluations saved to database only when:
  - User clicks "Stop & Submit" (partial completion)
  - User completes all 25 samples (full completion)
- **Editable results**: Users can navigate back/forth and modify previous answers
- **Smart navigation**: Next button prominent and disabled until current sample is fully evaluated
- **Session persistence**: localStorage maintains progress across browser sessions
```

#### 2.3 평가 설계 (Dynamic Sampling)

```python
evaluation_design = {
    "evaluators": "익명 (구분 없음)",
    "target_sessions": 56,  # 14명 × 4세션 목표
    "samples_per_session": 25,  # 매 세션 새로운 25개
    
    "dynamic_sampling": {
        "method": "매 세션마다 438개 중 25개 랜덤 선택",
        "benefit": "모든 샘플이 평균 3.2회 평가",
        "coverage": "96% 샘플이 최소 1회 이상 평가"
    },
    
    "session_structure": {
        "warm_up": 2,  # 연습용 샘플
        "actual": 25,  # 실제 평가 샘플
        "navigation": ["이전", "다음", "처음부터"],
        "progress_save": "localStorage (자동)"
    },
    
    "data_collection": {
        "storage": "JSON 파일",
        "format": {
            "session_id": "unique per session",
            "timestamp": "datetime",
            "sample_id": "string",
            "scores": {
                "quality": "1-7",
                "emotion": "1-7",
                "similarity": "1-7"
            },
            "comment": "optional string"
        }
    }
}

# Flask 서버 - Dynamic Sampling
flask_server = """
from flask import Flask, jsonify, request
import json
import random
import uuid
from datetime import datetime

app = Flask(__name__)

@app.route('/api/get-session-samples')
def get_session_samples():
    # 매 요청마다 438개 중 25개를 새로 랜덤 선택
    all_samples = load_all_samples()  # 438개 전체 (6 ref + 432 variations)
    session_samples = random.sample(all_samples, 25)
    session_id = str(uuid.uuid4())
    
    # 세션 로그 저장 (어떤 샘플이 선택되었는지)
    log_session_samples(session_id, session_samples)
    
    return jsonify({
        'session_id': session_id,
        'samples': session_samples,
        'total': 25
    })

@app.route('/api/save-result', methods=['POST'])
def save_result():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    
    with open('data/results.json', 'a') as f:
        json.dump(data, f)
        f.write('\\n')
    
    return jsonify({'status': 'success'})
"""
```

### Phase 3: 데이터 분석 및 리포팅

#### 3.1 Mixed Effects Model 분석

```python
analysis_model = """
Quality_Score = β₀ + β₁(voice) + β₂(text) + β₃(emotion) + β₄(scale) 
                + β₅(emotion×scale) + β₆(emotion_type) 
                + random(evaluator) + random(sample) + ε

where:
- random(sample): 샘플별 난이도 차이 보정 (동적 샘플링의 이점)
- emotion_type: audio_based vs prompt_based vs style_based
- scale: 모든 emotion type에 적용되는 연속 변수
- 각 변수의 주효과 및 상호작용 분석
- 평가자 효과 보정
"""

expected_results = {
    "voice_effect": "p < 0.01, 검정력 0.99",
    "text_effect": "p < 0.01, 검정력 0.95",
    "emotion_main_effect": "p < 0.01, 검정력 0.75",
    "scale_effect": "p < 0.01, 검정력 0.88",
    "emotion×scale_interaction": "style vs vector의 scale 반응 차이",
    "overall_power": "0.85 (438개 샘플, 동적 샘플링)",
    "coverage": "96% 샘플이 평가되어 대부분 조합 포착"
}
```

#### 3.2 자동 품질 검사

```python
automatic_checks = {
    "silence_detection": "무음 구간 감지",
    "clipping_detection": "클리핑 발생 감지",
    "duration_check": "비정상적 길이 감지",
    "volume_analysis": "볼륨 레벨 이상 감지",
    "noise_level": "SNR 측정"
}
```

#### 3.3 통계 분석 메트릭

```python
analysis_metrics = {
    "parameter_impact": {
        "emotion_scale vs 퀄리티": "선형/비선형 관계 분석",
        "emotion_type별 감정표현력": "audio/prompt/style 비교",
        "voice_id별 화자유사도": "화자별 안정성 분석"
    },
    
    "threshold_analysis": {
        "critical_cases": "점수 < 4인 케이스 분석",
        "high_performers": "점수 ≥ 6인 케이스 분석",
        "parameter_patterns": "문제 발생 파라미터 조합"
    },
    
    "reference_effectiveness": {
        "audio_vs_prompt": "레퍼런스 타입별 효과성",
        "scale_optimization": "최적 emotion_scale 값 도출"
    }
}
```

## 📁 프로젝트 구조 (간소화)

```
tts-qa-system/
├── config/
│   ├── config.yaml
│   └── test_parameters.json
├── references/
│   ├── audio/           # 오디오 레퍼런스 파일
│   │   ├── excited.wav
│   │   ├── furious.wav
│   │   └── terrified.wav
│   └── prompts/         # 텍스트 프롬프트
│       └── prompts.json
├── scripts/
│   ├── generate_voices.py
│   ├── api_client.py
│   ├── sampling_strategy.py
│   └── batch_processor.py
├── webapp/
│   ├── app.py           # 간단한 Flask 서버
│   ├── static/
│   │   ├── index.html   # 단일 페이지 앱
│   │   ├── app.js       # 평가 로직 및 상태 관리
│   │   └── styles.css   # 스타일
│   └── data/
│       └── results.json # 평가 결과 저장
├── analysis/
│   ├── mixed_effects_model.py
│   └── report_generator.py
├── data/
│   └── voices/          # 생성된 음성 파일
└── requirements.txt
```

## 🚀 구현 단계별 가이드 (Dynamic Sampling)

### Step 1: 환경 설정 및 레퍼런스 준비 (Day 1)
```bash
# 프로젝트 초기화
mkdir tts-qa-system
cd tts-qa-system
python -m venv venv
source venv/bin/activate

# 최소 패키지만 설치
pip install flask requests pyyaml pandas numpy
```

### Step 2: 음성 생성 스크립트 (Day 2-3)
1. 전체 438개 샘플 조합 생성
   - Reference: 6개 (2 voice × 3 text)
   - Style variations: 216개 (2 × 3 × 6 style × 6 scale)
   - Emotion vector variations: 216개 (2 × 3 × 6 vector × 6 scale)
2. API 호출로 모든 음성 생성
3. 파일명 규칙에 따라 저장
4. 샘플 메타데이터 JSON 생성

### Step 3: 간단한 웹 앱 구축 (Day 3-4)
1. 단일 HTML 페이지 (SPA)
2. 세션 시작 시 서버에서 25개 랜덤 샘플 받기
3. localStorage로 진행 상황 관리
4. Flask로 샘플 제공 및 결과 저장 API 구현

### Step 4: 테스트 및 데이터 수집 (Day 5-8)
1. 평가자들에게 링크 배포
2. 각자 편한 시간에 25개씩 4세션 진행
3. 매 세션마다 다른 샘플 세트 평가
4. JSON 파일로 결과 수집

### Step 5: 분석 (Day 9)
1. 수집된 JSON 데이터 파싱
2. 샘플별 평가 횟수 확인
3. Mixed Effects Model 분석
4. Style vs Emotion Vector의 scale 반응 차이 분석
5. 결과 리포트 생성

## 📊 예상 결과물

### 1. 생성된 데이터
- 음성 파일: 438개 (6 reference + 432 variations)
- 레퍼런스 매핑: JSON 파일로 관리
- 평가 데이터: ~1,400개 (56세션 × 25샘플)

### 2. 샘플 커버리지
```python
coverage_stats = {
    "총 샘플": 438,
    "- Reference": 6,
    "- Style variations": 216,  # 6 styles × 6 scales × 6 combinations
    "- Emotion vector variations": 216,  # 6 vectors × 6 scales × 6 combinations
    "평균 평가 횟수": 3.2,
    "최소 1회 평가": "96%",
    "최소 2회 평가": "78%",
    "미평가 샘플": "< 4%"
}
```

### 3. 수집 데이터 형식
```json
{
  "session_id": "unique-uuid-per-session",
  "timestamp": "2024-01-01T10:30:00",
  "sample_id": "v001_t001_style_happy-1_scale_2.0",
  "scores": {
    "quality": 5,
    "emotion": 6,
    "similarity": 4
  },
  "comment": "optional comment",
  "duration_ms": 8500
}
```

### 4. 분석 리포트
- 변수별 주효과 분석 (검정력 0.85)
- Style vs Emotion Vector의 scale 민감도 비교
- Scale이 각 emotion type에 미치는 영향 분석
- Audio vs Prompt 기반 emotion vector 효과성 비교

## ⚠️ 주의사항

1. **브라우저 호환성**: localStorage 지원 브라우저 확인
2. **데이터 백업**: results.json 주기적 백업
3. **샘플 관리**: 438개 전체 샘플 파일 서버에 준비
4. **세션 로깅**: 각 세션에서 어떤 샘플이 선택되었는지 기록
5. **오디오 파일 경로**: 웹 서버에서 접근 가능하도록 설정
6. **Scale 적용**: 모든 emotion (style_label, emotion_vector)에 scale 적용 확인

## 🔄 향후 개선 사항

1. **적응형 샘플링**: 초기 결과 기반 추가 샘플링
2. **자동 품질 평가**: ML 기반 사전 필터링
3. **A/B 테스트**: 모델 버전 간 비교
4. **실시간 분석**: 평가 진행 중 실시간 통계 업데이트

---

이 문서를 바탕으로 Cursor와 함께 각 컴포넌트를 순차적으로 구현하시면 됩니다. 특히 레퍼런스 처리와 샘플링 전략이 핵심입니다.