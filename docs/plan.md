# Voice Samples Generation Plan for New Voice IDs

## Overview
Generate new voice sample sets with updated voice_ids in a `voices_2` directory parallel to the current `voices` directory.

## Updated Voice IDs
- **v001**: 68c3cbbc39de69ffd6baad5f (male)
- **v002**: 68c3cbc04b464b622eb32355 (female)

## Fresh API Token
```
Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImVmMjQ4ZjQyZjc0YWUwZjk0OTIwYWY5YTlhMDEzMTdlZjJkMzVmZTEiLCJ0eXAiOiJKV1QifQ.eyJfaWQiOiI2NWQ0MGIyZWQzNzMzNDE2MTI1NDhjZmUiLCJhcHByb3ZlZCI6dHJ1ZSwiYXV0aHR5cGUiOiJmaXJlYmFzZSIsInByb3ZpZGVyIjoicGFzc3dvcmQiLCJpc19wYWlkIjp0cnVlLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHlwZWNhc3QtYTRjOGYiLCJhdWQiOiJ0eXBlY2FzdC1hNGM4ZiIsImF1dGhfdGltZSI6MTc1Njg2NTg3NCwidXNlcl9pZCI6IkljUm1ZNEloZTNVTUZrS0pNVjlNVTRtSjkzZDIiLCJzdWIiOiJJY1JtWTRJaGUzVU1Ga0tKTVY5TVU0bUo5M2QyIiwiaWF0IjoxNzU2ODY1ODg3LCJleHAiOjE3NTY4Njk0ODcsImVtYWlsIjoic2FuZ2hlZSsxQG5lb3NhcGllbmNlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbmdoZWUrMUBuZW9zYXBpZW5jZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.IKhDwBmzcwUPsXrJgIgPiz6mQTo2Ineq6u1kA4_jZpc41pJTDkfJF6mHyA6Ldkcj6y2vBkWIAO_ml_NzEidRetmx6SEnOWHDt9xMRAerTWSQ2bD24RS1y5W4l_SsEg5IeYuROzcfwmaWWqdGyHvCbBDoxPIEPqqwlzTJooMDDRhcd0i4MdISFH68gw4ZMMBLSsrj-NFJ4BeDvjWXyqZctEREN-_l6PxQs7fBpmqI7esjL634cFt7cK_5IMRoWVm0LMj7TJD4zuBMHkk3CzwSw0bKybygZWeJ8kxPKwlSiL7pANjeP5cw4T5uun2EPeIObFQ1E7h3Xoy-H4i4A9hvMA
```

## Target Directory Structure
```
public/
  voices_2/                    # NEW - parallel to voices/
    expressivity_none/         # Baseline without |0.6 suffix
    expressivity_0.6/          # With |0.6 suffix for expressivity test
```

## Critical Requirements

### API Call Requirements
- **MUST include**: `"mode": "one-vocoder"` in all API calls
- Use fresh token provided above
- Follow existing batch request patterns (max 4 requests per batch)

### Reference Audio Requirements
- **Filename pattern**: `{voice_id}_{emotion}_{text_type}_reference.wav`
- **API parameters for references**:
  - `"style_label": "normal-1"`
  - NO `emotion_label` or `emotion_vector_id` 
  - `"emotion_scale": 1.0`
  - `"mode": "one-vocoder"`

### Sample Audio Requirements  
- **Filename pattern**: `{voice_id}_{emotion}_{text_type}_scale_{scale_value}.wav`
- **API parameters for samples**:
  - `"style_label": "normal-1"` 
  - `"emotion_label": {emotion}` OR `"emotion_vector_id": {emotion_vector_id}`
  - `"emotion_scale": {scale_value}`
  - `"mode": "one-vocoder"`

### Emotion Configuration
Based on `/Users/bagsanghui/ssfm30_qa/docs/tts-test-sentences.md`:

**emotion_label emotions** (6):
- angry, sad, happy, whisper, toneup, tonedown

**emotion_vector_id emotions** (6):
- excited: `68a6b0ca2edfc11a25045538`
- furious: `68a6b0d9b436060efdc6bc82` 
- terrified: `68a6b0d2b436060efdc6bc80`
- fear: `68a6b0f7b436060efdc6bc83`
- surprise: `68a6b10255e3b2836e609969`
- excitement: `68a6b1062edfc11a2504553b`

### Scale Values
- 1.0, 1.2, 1.4, 1.6, 1.8, 2.0 (6 scale values)

### Text Types
- match, neutral, opposite (3 text types per emotion)

## Calculation
- 2 voices × 12 emotions × 3 text_types = 72 reference files per expressivity
- 2 voices × 12 emotions × 3 text_types × 6 scales = 432 sample files per expressivity
- **Only for expressivity 0.6**: 72 + 432 = 504 files

## Execution Plan

### Phase 1: Test Setup ✅
- [x] Create plan.md with complete checklist
- [x] Test single API call with new voice_id and token
- [x] Verify `voices_2` directory structure creation

### Phase 2: Script Preparation
- [ ] Duplicate `generate_all_reference_audios.py` → `generate_all_reference_audios_v2.py`
- [ ] Update voice_ids and token in duplicated script
- [ ] Update output directory to `voices_2`
- [ ] Duplicate main generation script for samples
- [ ] Update with new voice_ids, token, and emotion_vector_ids

### Phase 3: Reference Generation
- [ ] Generate reference files for expressivity_none (72 files)
- [ ] Generate reference files for expressivity_0.6 (72 files)
- [ ] Verify all reference files created correctly

### Phase 4: Sample Generation  
- [ ] Generate sample files for expressivity_none (432 files)
- [ ] Generate sample files for expressivity_0.6 (432 files)
- [ ] Verify all sample files created correctly

### Phase 5: Validation
- [ ] Count total files: should be 1,008 files
- [ ] Verify filename patterns match existing conventions
- [ ] Test audio playback of sample files
- [ ] Create summary report

## Key Differences from Previous Setup

### Voice IDs Changed
```
OLD:
v001: "688b02990486383d463c9d1a" 
v002: "689c69984c7990a1ddca2327"

OLD:  
v001: "68ad0ca7e68cb082a1c46fd6"
v002: "68ad0cb625c2800730ac5b48"
```
NEW:
- **v001**: 68c3cbbc39de69ffd6baad5f (male)
- **v002**: 68c3cbc04b464b622eb32355 (female)

### New Emotion Vector IDs
The emotion_vector_id values have been updated in the documentation.

### Directory Structure
- Output to `public/voices_3/` instead of `public/voices/` or `public/voices_2/`
- No need of subdirectory structure (we dont need expressivity_none anymore)

## Success Criteria
1. All 504 files generated successfully
2. No missing or corrupted audio files  
3. Correct filename patterns maintained
4. All API calls include `"mode": "one-vocoder"`
5. Reference files use `style_label: "normal-1"` only
6. Sample files include appropriate emotion parameters

## Audio Quality Improvement Plan (2025-09-03)

### 🎯 **Critical Issue Discovered**
Current voice generation scripts are using **standard quality** audio instead of **high quality**.

### 🔍 **Investigation Results:**
- **TTS API provides multiple quality options**: standard, high, hd1, low
- **Current scripts use**: `result["audio"]["url"]` → Standard quality ❌
- **Should use**: `result["audio"]["high"]["url"]` → High quality ✅ / You should check this, we need hd1(the best quality)
- **Backend approach**: Proper CloudFront optimization with high quality

### 📊 **Quality Comparison:**
```python
# Current (Standard Quality)
audio_url = result["audio"]["url"]
download_url = get_download_url(audio_url)  # Standard quality

# Improved (High Quality)  
audio_url = result["audio"]["high"]["url"]  # High quality source: also check this, we need hd1
download_url = get_download_url(audio_url)  # High quality via CloudFront
```

### 🔧 **Implementation Plan:**

#### Phase 1: Script Updates
- [ ] Update `generate_emotion_vectors_only.py` to use hd1 quality
- [ ] Update `generate_missing_4_fixed.py` to use hd1 quality
- [ ] Update `generate_all_samples_v2.py` to use hd1 quality
- [ ] Update `generate_all_reference_audios_v2.py` to use hd1 quality

#### Phase 2: Quality Enhancement
- [ ] Implement proper high-quality download function
- [ ] Add fallback to standard quality if high quality unavailable
- [ ] Add quality validation and comparison

#### Phase 3: Validation
- [ ] Generate test samples with both qualities
- [ ] Compare audio file sizes and quality metrics
- [ ] Verify improved audio fidelity

### 🎵 **Expected Impact:**
- **Better audio quality** for TTS evaluation
- **Improved research validity** with higher fidelity samples
- **Consistent quality** across all voice samples

### 📋 **Files to Update:**
1. `generate_emotion_vectors_only.py` - Main generation script
2. `generate_all_samples_v2.py` - Batch sample generation
3. `generate_all_reference_audios_v2.py` - Reference audio generation
4. `generate_missing_4_fixed.py` - Missing file generation

## Rollback Plan
If generation fails:
1. Keep existing `voices/` or `voices_2/` directory unchanged
2. Delete incomplete `voices_3/` directory  
3. Debug issues with small test batch
4. Retry with corrected parameters