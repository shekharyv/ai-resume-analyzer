/**
 * API client for communicating with the backend
 */

// Backend API base URL - modify if backend runs on different URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Analyze a resume PDF file
 * @param {File} file - PDF file to analyze
 * @param {string} jobTitle - Optional job title
 * @returns {Promise<Object>} Analysis results
 */
export async function analyzeResume(file, jobTitle = '') {
  const formData = new FormData();
  formData.append('file', file);
  
  if (jobTitle && jobTitle.trim()) {
    formData.append('job_title', jobTitle.trim());
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      // Try to parse error message from response
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = errorData.detail || `Server error: ${response.status}`;
      throw new Error(errorMessage);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    // Network errors or other issues
    if (error.message.includes('Failed to fetch')) {
      throw new Error('Cannot connect to backend. Make sure the server is running on ' + API_BASE_URL);
    }
    throw error;
  }
}

/**
 * Check backend health
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return await response.json();
  } catch (error) {
    return { error: error.message };
  }
}
