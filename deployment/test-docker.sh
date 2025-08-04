#!/bin/bash

# Test script for Docker setup
echo "🐳 Testing BeaconAI Docker Setup"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file from template..."
    cp .env.docker .env
    echo "✅ Please edit .env file with your actual API keys before running docker-compose"
fi

# Test Docker Compose syntax
echo "🔍 Validating docker-compose.yml..."
docker-compose config > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ docker-compose.yml is valid"
else
    echo "❌ docker-compose.yml has syntax errors"
    exit 1
fi

# Test Dockerfile syntax
echo "🔍 Testing Dockerfile.backend..."
docker build -f Dockerfile.backend -t test-backend .. --no-cache --quiet > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Dockerfile.backend builds successfully"
    docker rmi test-backend > /dev/null 2>&1
else
    echo "❌ Dockerfile.backend has build errors"
fi

echo "🔍 Testing Dockerfile.frontend..."
docker build -f Dockerfile.frontend -t test-frontend .. --no-cache --quiet > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Dockerfile.frontend builds successfully"
    docker rmi test-frontend > /dev/null 2>&1
else
    echo "❌ Dockerfile.frontend has build errors"
fi

echo "🎉 Docker setup validation complete!"
echo "📝 Next steps:"
echo "   1. Edit .env file with your API keys"
echo "   2. Run: docker-compose up --build"
echo "   3. Access backend: http://localhost:8000"
echo "   4. Access frontend: http://localhost:8501"