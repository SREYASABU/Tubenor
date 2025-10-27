#!/bin/bash

# Tubenor - Quick Start Script

echo "🎬 Starting Tubenor - YouTube Analytics Assistant"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env file not found!"
    echo "   Please create backend/.env with your YouTube API credentials."
    echo ""
    echo "   Example:"
    echo "   DATABASE_URL=postgresql://tubentor:tubentor_password@tubentor-db:5432/tubentor_db"
    echo "   YT_CLIENT_ID=your_client_id"
    echo "   YT_CLIENT_SECRET=your_client_secret"
    echo "   YT_REFRESH_TOKEN=your_refresh_token"
    echo ""
    read -p "Do you want to continue anyway? (y/N): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🔨 Building containers..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Tubenor is running!"
    echo ""
    echo "📱 Frontend:  http://localhost:3000"
    echo "🔌 Backend:   http://localhost:8000"
    echo "📊 API Docs:  http://localhost:8000/docs"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop:      docker-compose down"
else
    echo ""
    echo "❌ Failed to start services. Check logs with: docker-compose logs"
    exit 1
fi

