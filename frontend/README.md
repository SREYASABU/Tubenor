# Tubenor Frontend

A beautiful, minimalistic chat interface for interacting with your YouTube Analytics Assistant. Built with React and styled with YouTube's iconic color theme.

## 🎨 Features

- **YouTube-Themed Design**: Classic YouTube red, black, and white color scheme
- **Real-time Chat**: Interactive chat interface with typing indicators
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Example Queries**: Quick-start suggestions for common questions
- **Smooth Animations**: Polished user experience with subtle animations

## 🚀 Quick Start

### Using Docker (Recommended)

The easiest way to run the frontend is with Docker Compose from the root directory:

```bash
cd Tubentor
docker-compose up frontend
```

The app will be available at: **http://localhost:3000**

### Local Development

If you want to run the frontend locally for development:

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm start
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

## 📁 Project Structure

```
frontend/
├── public/
│   ├── index.html          # HTML template
│   └── manifest.json       # PWA manifest
├── src/
│   ├── components/
│   │   └── Chat.js         # Main chat component
│   ├── styles/
│   │   ├── index.css       # Global styles
│   │   ├── App.css         # App container styles
│   │   └── Chat.css        # Chat interface styles (YouTube theme)
│   ├── App.js              # Root component
│   └── index.js            # Entry point
├── Dockerfile              # Multi-stage Docker build
├── nginx.conf              # Nginx configuration
└── package.json            # Dependencies & scripts
```

## 🎨 YouTube Color Theme

The interface uses YouTube's official color palette:

- **Primary Red**: `#FF0000`
- **Dark Red**: `#CC0000` (hover states)
- **Background**: `#0f0f0f` (dark gray)
- **Surface**: `#212121` (lighter gray)
- **Text**: `#ffffff` (white)
- **Secondary Text**: `#aaaaaa` (gray)

## 🔌 API Integration

The frontend connects to the backend API at `/agents/general-query`. The nginx configuration automatically proxies API requests to the backend container.

### Example Request

```javascript
axios.post('/agents/general-query', null, {
  params: { query: 'How many views does my latest video have?' }
})
```

## 🐳 Docker Configuration

### Dockerfile

The frontend uses a multi-stage Docker build:

1. **Build Stage**: Node.js 18 Alpine - compiles React app
2. **Production Stage**: Nginx Alpine - serves static files

### Nginx Configuration

- Serves React app at port 80
- Proxies `/agents/*` requests to backend
- Supports React Router (SPA routing)
- Enables gzip compression
- Caches static assets

## 🔧 Configuration

### Environment Variables

The frontend can be configured using environment variables:

- `REACT_APP_API_URL`: Backend API URL (default: proxied via nginx)

### Backend Connection

In Docker Compose, the frontend connects to the backend via Docker network:
- Service name: `backend`
- Internal URL: `http://backend:8000`

## 📱 Responsive Design

The interface is fully responsive with breakpoints at:
- **Desktop**: Full-featured layout (> 768px)
- **Mobile**: Optimized touch-friendly interface (≤ 768px)

## 🎯 Usage Examples

The chat interface includes quick-start examples:
- "How many views does my latest video have?"
- "What are my top 5 videos?"
- "Show me my channel statistics"

Simply click an example to populate the input field, or type your own query.

## 🛠️ Development

### Available Scripts

- `npm start` - Run development server (port 3000)
- `npm run build` - Create production build
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Code Style

The project follows standard React best practices:
- Functional components with hooks
- CSS modules for styling
- Axios for API requests

## 🚢 Deployment

### Production Build

```bash
docker build -t tubentor-frontend .
docker run -p 3000:80 tubentor-frontend
```

### Docker Compose

```bash
docker-compose up -d frontend
```

## 📄 License

Part of the Tubentor project.

