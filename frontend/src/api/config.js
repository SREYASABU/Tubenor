import axios from 'axios';

// Create axios instance with relative URLs
// The setupProxy.js will handle proxying to the backend in development
// In production (Docker), nginx will handle the proxying
const api = axios.create({
  baseURL: '', // Use relative URLs - proxy will handle routing
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Log API calls for debugging
api.interceptors.request.use((config) => {
  console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
  return config;
}, (error) => {
  return Promise.reject(error);
});

api.interceptors.response.use((response) => {
  console.log(`API Response: ${response.config.url} - ${response.status}`);
  return response;
}, (error) => {
  console.error(`API Error: ${error.config?.url} -`, error.response?.status || error.message);
  return Promise.reject(error);
});

export default api;

