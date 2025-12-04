/**
 * API Service for EchoMind Frontend
 * Handles all communication with the FastAPI backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}${API_VERSION}`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    
    if (error.response) {
      // Server responded with error status
      console.error('Error Response:', error.response.data);
    } else if (error.request) {
      // Request made but no response received
      console.error('No response received from server');
    } else {
      // Error in request configuration
      console.error('Error setting up request:', error.message);
    }
    
    return Promise.reject(error);
  }
);

/**
 * Query the EchoMind AI for mental wellness support
 * @param {Object} queryData - Query request data
 * @returns {Promise} Query response with synthesized answer and resources
 */
export const sendQuery = async (queryData) => {
  try {
    const response = await apiClient.post('/query', queryData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Check API health status
 * @returns {Promise} Health check response
 */
export const checkHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Get knowledge base statistics
 * @returns {Promise} Statistics about the vector database
 */
export const getStats = async () => {
  try {
    const response = await apiClient.get('/stats');
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Ingest a new document into the knowledge base (admin function)
 * @param {Object} documentData - Document to ingest
 * @returns {Promise} Ingestion result
 */
export const ingestDocument = async (documentData) => {
  try {
    const response = await apiClient.post('/ingest', documentData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default {
  sendQuery,
  checkHealth,
  getStats,
  ingestDocument,
};
