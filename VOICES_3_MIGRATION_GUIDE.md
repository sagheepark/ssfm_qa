# voices_3 Migration Guide - COMPLETED ✅

## 🎯 Overview
Successfully migrated TTS QA system to support the new voices_3 dataset with HD1 premium quality audio and enhanced database tracking.

## 📋 Changes Made

### 1. **Database Schema Updates** ✅
- Created V3 table structures (`qa_sessions_v3`, `sample_evaluations_v3`, `sample_metadata_v3`)
- Added HD1 quality tracking and experiment versioning
- Enhanced metadata extraction and storage

### 2. **Smart Routing System** ✅
- Updated `shouldUseV3Tables()` function to detect voices_3 sessions
- Enhanced `saveEvaluationSmart()` and `createSessionSmart()` functions
- Added automatic experiment version detection

### 3. **Application Updates** ✅
- Updated session creation to include voices_3 identifiers
- Added HD1 quality indicators in UI
- Enhanced progress tracking with dataset information

### 4. **Analysis Framework** ✅
- Created `tts_analysis_v3.py` for multi-version analysis
- Added `export_v3_data.py` for data extraction
- Enhanced comparison capabilities between experiment versions

## 🚀 How to Use

### Starting a New voices_3 Session
1. **Open the application** - All new sessions automatically use voices_3
2. **Click "Start HD1 Quality Evaluation"** - Creates voices_3 session
3. **Complete evaluations** - Data automatically routed to V3 tables
4. **Session completed** - Results stored with HD1 quality tracking

### Session ID Format
```
session_[timestamp]_voices_3_expressivity_0.6
```

### Data Structure
```javascript
// V3 Session Data
{
  session_id: "session_1756229497710_voices_3_expressivity_0.6",
  experiment_version: "voices_3",
  audio_quality: "hd1",
  voice_set: "expressivity_0.6",
  // ... other fields
}

// V3 Evaluation Data  
{
  session_id: "session_1756229497710_voices_3_expressivity_0.6",
  sample_id: "v001_angry_match_scale_1.2",
  experiment_version: "voices_3",
  audio_quality: "hd1",
  voice_id: "v001",
  emotion_value: "angry",
  emotion_type: "emotion_label",
  text_type: "match",
  emotion_scale: 1.2,
  scores: { quality: 5, emotion: 6, similarity: 4 },
  // ... other fields
}
```

## 📊 Analysis & Data Export

### Export voices_3 Data
```bash
# Export evaluation data from Supabase
python analysis/export_v3_data.py

# Run comprehensive analysis
python analysis/tts_analysis_v3.py
```

### Analysis Features
- **Multi-version comparison** (voices_2 vs voices_3)
- **HD1 quality impact analysis**
- **Enhanced statistical modeling**
- **Automated report generation**

## 🧪 Testing

### Test Complete Flow
```bash
# Test V3 routing and database operations
node test-voices-3-flow.js
```

### Test Coverage
- ✅ V3 session creation
- ✅ V3 evaluation storage
- ✅ Smart routing logic
- ✅ Data retrieval
- ✅ HD1 quality tracking

## 🎵 Audio System

### Directory Structure
```
public/voices_3/
└── expressivity_0.6/
    ├── 72 reference files (*_reference.wav)
    └── 432 sample files (*_scale_*.wav)
```

### Quality Specifications
- **Audio Quality**: HD1 Premium
- **File Count**: 504 total files
- **Voice IDs**: v001 (male), v002 (female)
- **Emotions**: 6 labels + 6 vectors = 12 total
- **Scales**: 1.0, 1.2, 1.4, 1.6, 1.8, 2.0

## 🔄 Backward Compatibility

### Multi-Version Support
The system maintains full backward compatibility:
- **voices_1** → V1 tables (legacy)
- **voices_2** → V2 tables (previous experiment)
- **voices_3** → V3 tables (current HD1 dataset)

### Automatic Detection
Sessions are automatically routed based on:
- Session ID patterns (`voices_3` identifier)
- Experiment version metadata
- Audio quality indicators

## 📈 Key Benefits

### For Researchers
- **HD1 Audio Quality** - Premium audio for better evaluation accuracy
- **Enhanced Metadata** - Detailed tracking of all experiment parameters
- **Version Comparison** - Easy comparison between experiment versions
- **Automated Analysis** - Comprehensive statistical analysis tools

### For Data Collection
- **Smart Routing** - Automatic table selection based on session type
- **Data Integrity** - Enhanced validation and error handling
- **Progress Tracking** - Real-time session and evaluation monitoring
- **Export Tools** - Easy data extraction for external analysis

## 🚨 Important Notes

### Database Requirements
Ensure these tables exist in your Supabase instance:
- `qa_sessions_v3`
- `sample_evaluations_v3` 
- `sample_metadata_v3`

### Environment Variables
Required for data export and analysis:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### File Dependencies
Make sure these analysis files are available:
- `analysis/tts_analysis_v3.py`
- `analysis/export_v3_data.py`
- `test-voices-3-flow.js`

## ✅ Migration Status

- ✅ **Database Schema**: V3 tables created and configured
- ✅ **Smart Routing**: V3 detection and routing implemented  
- ✅ **UI Updates**: HD1 quality indicators added
- ✅ **Analysis Tools**: Multi-version analysis framework ready
- ✅ **Testing**: Complete flow validation passed
- ✅ **Documentation**: Migration guide completed

## 🎯 Next Steps

1. **Start Collecting Data** - Begin voices_3 evaluation sessions
2. **Monitor Performance** - Track HD1 quality impact on evaluations
3. **Run Analysis** - Compare voices_3 results with previous versions
4. **Generate Reports** - Use enhanced analysis tools for insights

---

**Migration Date**: September 15, 2025  
**Status**: ✅ COMPLETE - READY FOR PRODUCTION  
**Dataset**: voices_3 HD1 Premium Quality (504 files)
