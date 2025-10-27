@echo off
REM Tubenor - Quick Start Script for Windows

echo 🎬 Starting Tubenor - YouTube Analytics Assistant
echo.

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if .env file exists
if not exist "backend\.env" (
    echo ⚠️  Warning: backend\.env file not found!
    echo    Please create backend\.env with your YouTube API credentials.
    echo.
    echo    Example:
    echo    DATABASE_URL=postgresql://tubentor:tubentor_password@tubentor-db:5432/tubentor_db
    echo    YT_CLIENT_ID=your_client_id
    echo    YT_CLIENT_SECRET=your_client_secret
    echo    YT_REFRESH_TOKEN=your_refresh_token
    echo.
    set /p confirm="Do you want to continue anyway? (y/N): "
    if /i not "%confirm%"=="y" exit /b 1
)

echo 🔨 Building containers...
docker-compose build

echo.
echo 🚀 Starting services...
docker-compose up -d

echo.
echo ⏳ Waiting for services to be healthy...
timeout /t 5 /nobreak >nul

echo.
echo ✅ Tubenor is running!
echo.
echo 📱 Frontend:  http://localhost:3000
echo 🔌 Backend:   http://localhost:8000
echo 📊 API Docs:  http://localhost:8000/docs
echo.
echo To view logs: docker-compose logs -f
echo To stop:      docker-compose down

