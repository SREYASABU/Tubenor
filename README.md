# 🎬 Tubenor - YouTube Analytics Assistant

An AI-powered chat interface for analyzing and understanding your YouTube channel data through natural language queries. Built with Google ADK's SequentialAgent pattern for reliable, deterministic execution.

![YouTube Theme](https://img.shields.io/badge/Theme-YouTube-FF0000?style=for-the-badge&logo=youtube)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)

## ✨ Features

### 🤖 AI-Powered Assistant
- **Sequential Agent Architecture**: Uses Google ADK's SequentialAgent for deterministic execution
- **No Looping**: Each agent runs exactly once per query
- **Dynamic API Calls**: Automatically constructs YouTube API queries from natural language
- **Natural Language Responses**: Converts raw data into conversational insights

### 🎨 Beautiful UI
- **YouTube-Themed**: Iconic red, black, and white color scheme
- **Minimalistic Design**: Clean, modern interface
- **Responsive**: Works on desktop and mobile
- **Real-time Chat**: Interactive conversation with typing indicators

### 📊 YouTube Analytics
- **Channel Statistics**: Subscriber count, total views, video count
- **Video Analytics**: Views, likes, comments, watch time
- **Performance Metrics**: Top videos, engagement rates, trends
- **Search & Discovery**: Find videos, analyze traffic sources

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│  Frontend (React + Nginx)           │
│  Port: 3000                         │
└──────────────┬──────────────────────┘
               │ HTTP/REST
┌──────────────▼──────────────────────┐
│  Backend (FastAPI)                  │
│  Port: 8000                         │
│  ┌───────────────────────────────┐  │
│  │ SequentialAgent               │  │
│  │  ├─ API Executor Agent        │  │
│  │  │  (Fetches YouTube data)    │  │
│  │  └─ Response Generator Agent  │  │
│  │     (Creates NL response)     │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │ SQL
┌──────────────▼──────────────────────┐
│  PostgreSQL Database                │
│  Port: 5432                         │
└─────────────────────────────────────┘
```

### Agent Flow

```
User Query → SequentialAgent
              ├─ Step 1: API Executor Agent
              │  └─ Executes YouTube API call
              │  └─ Stores in state['api_response']
              │
              └─ Step 2: Response Generator Agent
                 └─ Reads state['api_response']
                 └─ Generates natural language response
                 └─ Returns to user
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- YouTube API credentials (OAuth 2.0)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd tub/Tubentor
```

### 2. Set Up Environment Variables

Create `backend/.env`:

```env
# Database Configuration
DATABASE_URL=postgresql://tubentor:tubentor_password@tubentor-db:5432/tubentor_db
POSTGRES_USER=tubentor
POSTGRES_PASSWORD=tubentor_password
POSTGRES_DB=tubentor_db

# YouTube API Credentials
YT_CLIENT_ID=your_client_id_here
YT_CLIENT_SECRET=your_client_secret_here
YT_REFRESH_TOKEN=your_refresh_token_here

# API Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Add Client Secrets

Place your YouTube OAuth credentials in:
```bash
Tubentor/temp_client_secrets.json
```

### 4. Launch with Docker Compose

```bash
docker-compose up --build
```

This will start:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: PostgreSQL on port 5432

### 5. Access the App

Open your browser to **http://localhost:3000** and start chatting with **Tubenor**!

## 📖 Usage Examples

### Getting Started

The chat interface provides example queries to get you started:

**Channel Overview:**
```
"Show me my channel statistics"
"How many videos have I posted?"
"What's my total subscriber count?"
```

**Video Performance:**
```
"How many views does my latest video have?"
"What are my top 5 videos?"
"Which video got the most comments this week?"
```

**Analytics & Trends:**
```
"Show me my daily views for the last month"
"Where is my traffic coming from?"
"What's my audience demographic?"
```

## 🛠️ Technology Stack

### Frontend
- **React 18**: Modern UI framework
- **Axios**: HTTP client
- **CSS3**: YouTube-themed styling
- **Nginx**: Production web server

### Backend
- **FastAPI**: High-performance Python web framework
- **Google ADK**: Agent Development Kit for LLM agents
- **Gemini 2.0 Flash**: Google's latest LLM
- **YouTube Data API v3**: Channel and video data
- **YouTube Analytics API v2**: Metrics and analytics

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **PostgreSQL 17**: Session and state storage

## 📁 Project Structure

```
Tubentor/
├── frontend/                 # React chat interface
│   ├── src/
│   │   ├── components/      # React components
│   │   │   └── Chat.js      # Main chat UI
│   │   ├── styles/          # YouTube-themed CSS
│   │   └── App.js
│   ├── Dockerfile           # Multi-stage build
│   ├── nginx.conf           # Nginx config with API proxy
│   └── package.json
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── agents/          # Agent system
│   │   │   ├── main_agent.py              # SequentialAgent
│   │   │   ├── sub_agents/
│   │   │   │   ├── query_to_apicall_agent/ # API Executor
│   │   │   │   └── response_analyzer_agent/ # Response Generator
│   │   │   └── guardrail.py               # Safety checks
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # YouTube API integration
│   │   └── database/        # PostgreSQL connection
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
│
├── docker-compose.yaml       # Multi-container setup
└── README.md                 # This file
```

## 🔧 Configuration

### Agent Model

The default model is **Gemini 2.0 Flash**. To change:

```python
# backend/app/agents/sub_agents/query_to_apicall_agent/agent.py
AGENT_MODEL = "gemini/gemini-2.0-flash"
```

### YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3 and YouTube Analytics API v2
4. Create OAuth 2.0 credentials
5. Download the credentials JSON
6. Use OAuth Playground to get refresh token
7. Add to `backend/.env`

### CORS Configuration

Update allowed origins in `backend/.env`:

```env
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## 🐳 Docker Commands

### Build and Start

```bash
docker-compose up --build
```

### Start in Background

```bash
docker-compose up -d
```

### View Logs

```bash
docker-compose logs -f
```

### Stop Services

```bash
docker-compose down
```

### Rebuild Single Service

```bash
docker-compose up --build frontend
```

## 📊 API Endpoints

### Main Endpoint

```
POST /agents/general-query?query={your_question}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/agents/general-query?query=How%20many%20views%20on%20my%20latest%20video?"
```

### Health Check

```
GET /health
```

### List Available Agents

```
GET /agents/list
```

## 🎯 Agent Behavior

### No Permission Requests

The agent never asks for permission - it executes immediately:

❌ **Before:** "I cannot retrieve... Do you want me to proceed?"

✅ **After:** Executes `channel_details` and returns the count

### Correct Query Selection

The agent chooses the right query type automatically:

- **Total video count** → `channel_details` (not `my_videos`)
- **Latest video** → `my_videos` with `max_results=1`
- **Top videos** → `analytics` with `dimensions="video"`

## 🔍 Troubleshooting

### Frontend Can't Connect to Backend

Check Docker network:
```bash
docker network inspect tubentor_tubentor-network
```

### YouTube API Errors

Verify credentials in `backend/.env`:
```bash
docker-compose exec backend env | grep YT_
```

### Agent Not Responding

Check backend logs:
```bash
docker-compose logs backend
```

## 📚 Documentation

- [Agent Architecture](backend/AGENT_ARCHITECTURE.md) - Detailed agent system design
- [Query Reference](backend/QUICK_QUERY_REFERENCE.md) - Supported queries
- [Usage Examples](backend/USAGE_EXAMPLES.md) - Common use cases

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Google ADK**: Sequential agent framework
- **YouTube API**: Data and analytics
- **FastAPI**: High-performance backend
- **React**: Modern UI framework

---

**Built with ❤️ using Google ADK Sequential Agents**
