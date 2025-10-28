import React, { useEffect, useState } from 'react';
import api from '../api/config';
import '../styles/OAuthCallback.css';

const OAuthCallback = () => {
  const [status, setStatus] = useState('processing');
  const [error, setError] = useState(null);

  useEffect(() => {
    const handleCallback = async () => {
      console.log('=== OAUTH CALLBACK STARTED ===');
      console.log('Current URL:', window.location.href);
      console.log('Search params:', window.location.search);
      
      // Get authorization code from URL
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const state = urlParams.get('state');
      
      console.log('Extracted code:', code);
      console.log('Code length:', code?.length);
      console.log('Extracted state:', state);
      console.log('==============================');

      if (!code) {
        console.error('❌ NO CODE FOUND!');
        setStatus('error');
        setError('No authorization code received');
        return;
      }

      try {
        const backendUrl = '/auth/callback';
        const payload = { code, state };
        
        console.log('📤 Sending to backend:', backendUrl);
        console.log('📦 Payload:', payload);
        
        // Send code to backend
        const response = await api.post(backendUrl, payload);
        
        console.log('✅ Backend response:', response.data);

        setStatus('success');
        
        // Store user info
        localStorage.setItem('youtube_authenticated', 'true');
        if (response.data.channel_info) {
          localStorage.setItem('channel_info', JSON.stringify(response.data.channel_info));
        }

        // Redirect to home after 2 seconds
        setTimeout(() => {
          window.location.href = '/';
        }, 2);

      } catch (err) {
        console.error('❌ OAuth callback error:', err);
        console.error('Error message:', err.message);
        console.error('Error response:', err.response);
        console.error('Error response data:', err.response?.data);
        console.error('Error response status:', err.response?.status);
        
        setStatus('error');
        const errorMsg = err.response?.data?.detail || err.message || 'Authentication failed';
        setError(errorMsg);
        console.error('Setting error message:', errorMsg);
      }
    };

    handleCallback();
  }, []);

  return (
    <div className="oauth-callback">
      <div className="callback-container">
        {status === 'processing' && (
          <>
            <div className="spinner"></div>
            <h2>Connecting to YouTube...</h2>
            <p>Please wait while we complete the authentication</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="success-icon">✓</div>
            <h2>Successfully Connected!</h2>
            <p>Redirecting you back to Tubenor...</p>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="error-icon">✗</div>
            <h2>Authentication Failed</h2>
            <p>{error}</p>
            <button onClick={() => window.location.href = '/'}>
              Return to Home
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default OAuthCallback;

