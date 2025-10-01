@echo off
REM Gmail Backend Deployment Script for Windows
REM This script helps deploy the Gmail automation backend

echo 🚀 Gmail Backend Deployment Script
echo ==================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Check for required files
echo 📋 Checking required files...

if not exist "credentials.json" (
    echo ❌ credentials.json not found. Please download from Google Cloud Console.
    echo    See credentials.example for the expected format.
    pause
    exit /b 1
)

if not exist "config.py" (
    echo ❌ config.py not found. Please create from config.example.py
    echo    Make sure to add your GEMINI_API_KEY
    pause
    exit /b 1
)

echo ✅ All required files found

REM Build and start the application
echo 🔨 Building Docker image...
docker-compose build

echo 🚀 Starting the application...
docker-compose up -d

echo ⏳ Waiting for application to start...
timeout /t 10 /nobreak >nul

REM Health check
echo 🏥 Performing health check...
curl -f http://localhost:5000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Health check failed. Check the logs:
    docker-compose logs
    pause
    exit /b 1
) else (
    echo ✅ Application is running successfully!
    echo 🌐 Backend is available at: http://localhost:5000
    echo 📊 Health check: http://localhost:5000/health
)

echo.
echo 🎉 Deployment completed successfully!
echo.
echo 📝 Useful commands:
echo    View logs: docker-compose logs -f
echo    Stop app:  docker-compose down
echo    Restart:   docker-compose restart
echo.
pause
