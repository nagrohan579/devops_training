const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');
const fs = require('fs');
const http = require('http');
const app = express();
const PORT = process.env.PORT || 3000;
const USER_ID = process.env.USER_ID || 'A';

// Get backend URL from environment or default to localhost:5000
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:5000';

console.log(`Initializing proxy with USER_ID=${USER_ID}, BACKEND_URL=${BACKEND_URL}`);

// Configure proxy for backend WebSocket connections with enhanced options for stability
const wsProxy = createProxyMiddleware({
  target: BACKEND_URL,
  ws: true,
  changeOrigin: true,
  logLevel: 'debug',
  pathRewrite: function (path) {
    // Ensure the user ID from the URL is preserved when proxying
    console.log(`Original WebSocket request path: ${path}`);
    return path;
  },
  onProxyReqWs: (proxyReq, req, socket, options, head) => {
    // Set longer timeout to prevent WebSocket from closing
    socket.setKeepAlive(true);
    socket.setTimeout(0);
    console.log(`WebSocket connection established for ${req.url}`);
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`Received response for: ${req.url}, status: ${proxyRes.statusCode}`);
  },
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    if (res && res.writeHead) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Proxy error: ' + err);
    }
  }
});

// Create a proxy specifically for REST API endpoints
const apiProxy = createProxyMiddleware({
  target: BACKEND_URL,
  changeOrigin: true,
  logLevel: 'debug',
  pathRewrite: function (path) {
    console.log(`Proxying API request: ${path}`);
    return path;
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`API response received for: ${req.url}, status: ${proxyRes.statusCode}`);
  },
  onError: (err, req, res) => {
    console.error('API Proxy error:', err);
    if (res && res.writeHead) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('API Proxy error: ' + err);
    }
  }
});

// Path for static files
const staticPath = path.join(__dirname, 'public');

// Custom middleware to inject USER_ID into index.html
app.use((req, res, next) => {
  if (req.path === '/' || req.path === '/index.html') {
    const indexPath = path.join(staticPath, 'index.html');
    try {
      let html = fs.readFileSync(indexPath, 'utf8');
      
      // Inject the USER_ID as a global variable with debugging info
      html = html.replace(
        '</head>',
        `<script>
          window.USER_ID = "${USER_ID}";
          window.BACKEND_URL = "${BACKEND_URL}";
          console.log("Injected USER_ID:", window.USER_ID);
          console.log("Backend URL:", window.BACKEND_URL);
        </script>
        </head>`
      );
      
      return res.send(html);
    } catch (err) {
      console.error('Error reading or modifying index.html:', err);
      return next();
    }
  }
  next();
});

// Add status endpoint for debugging
app.get('/status', (req, res) => {
  res.json({
    status: 'running',
    userId: USER_ID,
    backendUrl: BACKEND_URL,
    time: new Date().toISOString()
  });
});

// Proxy API requests to backend
app.use('/messages', apiProxy);

// Serve static files from the public directory
app.use(express.static(staticPath));

// Use proxy for websocket traffic - handle both /ws and /ws/{user_id} paths
app.use('/ws', wsProxy);

// For any GET request that doesn't match a static file,
// serve the index.html file (for SPA routing)
app.get('*', (req, res) => {
  res.sendFile(path.join(staticPath, 'index.html'));
});

// Create HTTP server
const server = http.createServer(app);

// Start the server
server.listen(PORT, () => {
  console.log(`User ${USER_ID} proxy server running on http://localhost:${PORT}`);
  console.log(`Proxying WebSocket requests to ${BACKEND_URL}`);
  console.log(`Proxying REST API requests to ${BACKEND_URL}`);
  console.log(`Serving static files from ${staticPath}`);
});

// Handle WebSocket upgrade explicitly with better error handling
server.on('upgrade', (req, socket, head) => {
  console.log(`Upgrade request received for: ${req.url}`);
  
  if (req.url.startsWith('/ws')) {
    console.log(`Upgrading WebSocket connection: ${req.url}`);
    try {
      wsProxy.upgrade(req, socket, head);
    } catch (err) {
      console.error('Error during WebSocket upgrade:', err);
      socket.end('HTTP/1.1 500 Internal Server Error\r\n\r\n');
    }
  } else {
    console.log(`Ignoring non-WebSocket upgrade request: ${req.url}`);
    socket.end('HTTP/1.1 400 Bad Request\r\n\r\n');
  }
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('Shutting down server...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});