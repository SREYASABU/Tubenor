const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Proxy /auth/ requests to backend, EXCEPT GET /auth/callback
  // (that needs to be handled by React Router for OAuth)
  app.use(
    '/auth',
    createProxyMiddleware({
      target: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
      bypass: function (req, res, proxyOptions) {
        // Don't proxy GET requests to /auth/callback - let React Router handle them
        if (req.method === 'GET' && req.url.startsWith('/auth/callback')) {
          return '/index.html'; // Serve React app instead
        }
      },
    })
  );

  // Proxy /agents/ requests to backend
  app.use(
    '/agents',
    createProxyMiddleware({
      target: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
    })
  );
};

