# Tubentor

YouTube analytics assistant.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- YouTube OAuth credentials

### Setup

1. **Create `backend/.env`:**
```env
DATABASE_URL=postgresql://tubenor:tubenor_password@tubenor-db:5432/tubenor_db
POSTGRES_USER=tubenor
POSTGRES_PASSWORD=tubenor_password
POSTGRES_DB=tubenor_db

YT_CLIENT_ID=your_client_id.apps.googleusercontent.com
YT_CLIENT_SECRET=your_client_secret
OAUTH_REDIRECT_URI=http://localhost:3000/oauth/callback
ALLOWED_ORIGINS=http://localhost:3000
```

2. **Start the application:**
```bash
docker-compose up --build
```

3. **Access:** http://localhost:3000

## Tech Stack

- **Frontend:** React 18, Nginx
- **Backend:** FastAPI, Google ADK, Gemini 2.0
- **Database:** PostgreSQL 17
- **APIs:** YouTube Data API v3, YouTube Analytics API v2

## License

MIT
