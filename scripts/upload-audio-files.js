// Upload audio files to Supabase Storage
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Load environment variables
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
  console.error('Missing Supabase environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function uploadAudioFiles() {
  const audioDir = '../tts-qa-system/data/voices';
  const audioPath = path.resolve(__dirname, audioDir);
  
  console.log('📁 Looking for audio files in:', audioPath);
  
  if (!fs.existsSync(audioPath)) {
    console.error('❌ Audio directory not found:', audioPath);
    console.log('Please ensure the tts-qa-system directory exists with audio files');
    return;
  }

  const files = fs.readdirSync(audioPath).filter(file => file.endsWith('.wav'));
  
  console.log(`🎵 Found ${files.length} audio files to upload`);
  
  let uploaded = 0;
  let failed = 0;

  for (const filename of files) {
    try {
      const filePath = path.join(audioPath, filename);
      const fileBuffer = fs.readFileSync(filePath);
      
      console.log(`⬆️  Uploading: ${filename} (${(fileBuffer.length / 1024).toFixed(1)} KB)`);
      
      const { data, error } = await supabase.storage
        .from('tts-audio-samples')
        .upload(`voices/${filename}`, fileBuffer, {
          contentType: 'audio/wav',
          cacheControl: '3600',
          upsert: true // Overwrite if exists
        });

      if (error) {
        console.error(`❌ Failed to upload ${filename}:`, error.message);
        failed++;
      } else {
        console.log(`✅ Uploaded: ${filename}`);
        uploaded++;
      }
      
      // Rate limiting - wait 100ms between uploads
      await new Promise(resolve => setTimeout(resolve, 100));
      
    } catch (err) {
      console.error(`❌ Error processing ${filename}:`, err.message);
      failed++;
    }
  }
  
  console.log('\n📊 Upload Summary:');
  console.log(`✅ Successful: ${uploaded}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📁 Total files: ${files.length}`);
  
  if (uploaded > 0) {
    console.log('\n🎉 Audio files uploaded successfully!');
    console.log('You can now view them in your Supabase Storage dashboard.');
  }
}

// Run the upload
uploadAudioFiles().catch(console.error);