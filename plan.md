# TTS QA System - Complete Documentation & Blueprint

## 🎯 System Overview (2025-08-23)

### **Project Status: PRODUCTION READY ✅**
A comprehensive Text-to-Speech Quality Assessment system for evaluating emotional expressivity in TTS outputs.

---

## 📋 System Architecture

### **Core Components**
1. **Frontend Application** (Next.js 15 + TypeScript + Tailwind CSS)
2. **Database Layer** (Supabase with PostgreSQL)
3. **Audio Generation** (External TTS API integration)
4. **Evaluation Interface** (React-based assessment tools)

### **File Structure**
```
src/
├── app/
│   └── page.tsx           # Main evaluation interface
├── components/
│   ├── AudioPlayer.tsx    # Color-coded audio playback
│   ├── EvaluationForm.tsx # Assessment form
│   └── DatabaseConnectionError.tsx
├── lib/
│   ├── types.ts          # TypeScript definitions
│   ├── sampleData.ts     # Audio sample generation logic
│   └── supabase.ts       # Database operations
public/
└── voices/               # Audio file storage
    ├── expressivity_none/    # 504 files
    └── expressivity_0.6/     # 504 files
```

---

## 🔧 Technical Implementation

### **Audio Sample Matrix**
- **Total Files**: 1,008 audio files
- **Target Samples**: 864 files (432 × 2 expressivity types)
- **Reference Samples**: 144 files (72 × 2 expressivity types)

**Sample Breakdown**:
```
2 voices × 12 emotions × 3 text_types × 6 scales × 2 expressivity = 864 targets
2 voices × 12 emotions × 3 text_types × 2 expressivity = 144 references
```

### **Emotion Categories**
- **Emotion Labels**: angry, sad, happy, whisper, toneup, tonedown
- **Emotion Vectors**: excited, furious, terrified, fear, surprise, excitement
- **Text Types**: match, neutral, opposite
- **Scales**: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0
- **Expressivity**: none (standard), 0.6 (enhanced)

### **File Naming Convention**
- **Target**: `{voice_id}_{text_type}_{emo|vec}_{emotion}_scale_{scale}.wav`
- **Reference**: `{voice_id}_{text_type}_reference_{emotion}.wav`

### **Reference Audio Logic**
```typescript
export function getReferenceFilename(sample: TTSSample): string {
  return `${sample.voice_id}_${sample.text_type}_reference_${sample.emotion_value}.wav`;
}
```

---

## 🎨 User Interface Design

### **Current UI Structure**
1. **Enhanced Text Display**: Gradient box with shared text content
2. **Reference Audio Player**: Blue-themed with neutral baseline
3. **Target Audio Player**: Orange-themed with emotional content
4. **Evaluation Form**: 3-dimension scoring system

### **Color-Coded System**
- **Blue**: Reference audio (neutral baseline)
  - Play button: `bg-blue-600`
  - Slider handle: `#3b82f6`
  - Title text: `text-blue-800`
- **Orange**: Target audio (emotional)
  - Play button: `bg-orange-600` 
  - Slider handle: `#ea580c`
  - Title text: `text-orange-800`

### **AudioPlayer Component Props**
```typescript
interface AudioPlayerProps {
  sample: TTSSample;
  autoPlay?: boolean;
  voiceSet?: 'expressivity_none' | 'expressivity_0.6';
  isReference?: boolean;
  simplified?: boolean;
  title?: string;
  colorScheme?: 'blue' | 'orange';
}
```

---

## 💾 Database Schema

### **Sessions Table**
```sql
session_id: string (primary key)
started_at: timestamp
completed_at: timestamp
samples_data: json
voice_set: string
```

### **Evaluations Table**
```sql
session_id: string
sample_id: string
scores: json {quality, emotion, similarity}
comment: text
timestamp: timestamp
duration_ms: integer
```

---

## 🌐 Deployment & Environment

### **Production Environment**
- **Platform**: Vercel
- **Database**: Supabase PostgreSQL
- **Domain**: Custom domain via Vercel
- **CDN**: Vercel Edge Network for audio files

### **Environment Variables**
```bash
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

### **Build & Deploy**
```bash
npm run build    # Production build
git push origin main  # Auto-deploy via Vercel
```

### **Audio File Management**
- **Storage**: Git LFS for large audio files
- **Delivery**: Static file serving via Vercel
- **Organization**: Folder-based by expressivity type

---

## 📊 Evaluation Methodology

### **Assessment Dimensions**
1. **Quality** (1-7): Overall audio quality and clarity
2. **Emotion** (1-7): Emotional expressiveness accuracy
3. **Similarity** (1-7): Consistency with reference baseline

### **Evaluation Flow**
1. User listens to reference audio (neutral)
2. User listens to target audio (with emotion)
3. User rates on 3 dimensions + optional comment
4. Progress auto-saved locally
5. Final submission to database

### **Session Management**
- **Sample Size**: 25 random samples per session
- **Progress Tracking**: Real-time progress bar
- **Data Persistence**: localStorage + database backup
- **Session Recovery**: Automatic session restoration

---

## 🔄 Data Processing Pipeline

### **Audio Generation Workflow**
```python
# Example from generate_all_reference_audios.py
1. Define emotion texts (72 unique combinations)
2. Create TTS requests with style_label="normal-1"
3. Process in batches (API limit: 4 concurrent)
4. Download and organize by folder structure
5. Validate file completeness
```

### **Sample Data Generation**
```typescript
// From sampleData.ts
1. Generate sample pool from all combinations
2. Apply proper filename formatting (toFixed(1))
3. Map reference files via getReferenceFilename()
4. Shuffle and select random subset for session
```

---

## 📈 Performance & Monitoring

### **Key Metrics**
- Build size: ~163 kB (optimized)
- Audio files: 1,008 files (~2-4 seconds each)
- Session completion: ~15 minutes average
- Database operations: Supabase real-time sync

### **Error Handling**
- Database connection fallbacks
- Audio file validation
- Session recovery mechanisms
- Graceful degradation for missing files

---

## 🔒 Security & Privacy

### **Data Protection**
- No PII collection beyond session metadata
- Supabase RLS (Row Level Security) enabled
- API tokens secured via environment variables
- Git security: .gitignore for sensitive files

### **Access Control**
- Public evaluation interface
- Anonymous data collection
- No user authentication required
- Session-based data isolation

---

## 🚀 System Requirements

### **Development Environment**
- Node.js 18+
- Next.js 15
- TypeScript 5+
- Tailwind CSS 3+
- Supabase CLI (optional)

### **Production Requirements**
- Vercel hosting account
- Supabase project
- Git LFS for audio files
- Custom domain (optional)

### **Browser Support**
- Modern browsers with HTML5 audio support
- Chrome, Firefox, Safari, Edge
- Mobile responsive design
- Web Audio API compatibility

---

## 📋 Issues Resolved

### **Critical Fixes Applied** ✅
1. **Scale Format Consistency**: Fixed 1 vs 1.0 formatting across system
2. **Reference Audio Logic**: Proper filename matching and display
3. **UI Simplification**: Removed redundancy, enhanced visibility
4. **Color-Coded Controls**: Blue/orange theme for clear distinction
5. **Error Handling**: Comprehensive validation and fallbacks

---

## 📝 Usage Instructions

### **For Researchers**
1. Clone repository
2. Set up Supabase database
3. Configure environment variables
4. Generate or upload audio files
5. Deploy to Vercel
6. Share evaluation URL with participants

### **For Participants**
1. Access evaluation URL
2. Choose voice set (standard/enhanced)
3. Complete 25 sample evaluations
4. Submit results for analysis

---

## 🔮 Future Enhancements

### **Platform Expansion Vision**
- Multi-experiment support
- Custom emotion categories
- Advanced analytics dashboard
- Automated report generation
- API for external integrations

---

*Last Updated: 2025-08-23*
*System Status: Production Ready*
*Total Development Time: ~3 days intensive development*