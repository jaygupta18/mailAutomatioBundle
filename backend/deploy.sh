#!/bin/bash

# Gmail Backend Deployment Script
# This script helps deploy the Gmail automation backend

set -e

echo "🚀 Gmail Backend Deployment Script"
echo "=================================="

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

# Check for required files
echo "📋 Checking required files..."

if [ ! -f "credentials.json" ]; then
    echo "❌ credentials.json not found. Please download from Google Cloud Console."
    echo "   See credentials.example for the expected format."
    exit 1
fi

if [ ! -f "config.py" ]; then
    echo "❌ config.py not found. Please create from config.example.py"
    echo "   Make sure to add your GEMINI_API_KEY"
    exit 1
fi

echo "✅ All required files found"

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting the application..."
docker-compose up -d

echo "⏳ Waiting for application to start..."
sleep 10

# Health check
echo "🏥 Performing health check..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "🌐 Backend is available at: http://localhost:5000"
    echo "📊 Health check: http://localhost:5000/health"
else
    echo "❌ Health check failed. Check the logs:"
    docker-compose logs
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📝 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop app:  docker-compose down"
echo "   Restart:   docker-compose restart"
echo ""
