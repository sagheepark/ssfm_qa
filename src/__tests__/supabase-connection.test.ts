import { saveEvaluation, createSession } from '@/lib/supabase';

describe('Supabase Connection Tests', () => {
  test('should successfully save evaluation when environment variables are available', async () => {
    // Arrange
    const mockEvaluation = {
      session_id: 'test_session_123',
      sample_id: 'test_sample_123',
      scores: { quality: 5, emotion: 4, similarity: 3 },
      comment: 'test comment',
      timestamp: '2025-08-21T12:00:00.000Z',
      duration_ms: 5000
    };

    // Act & Assert
    // This should not throw "Database connection not available" error
    await expect(saveEvaluation(mockEvaluation)).resolves.toBeDefined();
  });

  test('should successfully create session when environment variables are available', async () => {
    // Arrange
    const mockSessionData = {
      session_id: 'test_session_123',
      started_at: '2025-08-21T12:00:00.000Z',
      samples_data: []
    };

    // Act & Assert
    // This should not throw "Database connection not available" error
    await expect(createSession(mockSessionData)).resolves.toBeDefined();
  });

  test('should have Supabase client properly initialized', () => {
    // This test verifies the root cause - environment variables should be available
    expect(process.env.NEXT_PUBLIC_SUPABASE_URL).toBeDefined();
    expect(process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY).toBeDefined();
    expect(process.env.NEXT_PUBLIC_SUPABASE_URL).toContain('supabase.co');
  });
});