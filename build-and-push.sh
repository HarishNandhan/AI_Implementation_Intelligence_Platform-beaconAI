#!/bin/bash

# BeaconAI Docker Build and Push Script
# Usage: ./build-and-push.sh

set -e  # Exit on any error

DOCKER_USERNAME="harishnandhan02"
PROJECT_NAME="beaconai"

echo "🐳 BeaconAI Docker Build & Push Script"
echo "======================================"
echo "Docker Hub Username: $DOCKER_USERNAME"
echo "Project: $PROJECT_NAME"
echo ""

# Check if logged in to Docker Hub
echo "🔍 Checking Docker Hub login..."
if ! docker info | grep -q "Username: $DOCKER_USERNAME"; then
    echo "❌ Not logged in to Docker Hub. Please run: docker login"
    exit 1
fi
echo "✅ Docker Hub login verified"

# Navigate to deployment directory
cd deployment

echo ""
echo "🏗️ Building Docker Images..."
echo "=============================="

# Build Backend Image
echo "📦 Building backend image..."
docker build -f Dockerfile.backend -t $DOCKER_USERNAME/$PROJECT_NAME-backend:latest ..
echo "✅ Backend image built"

# Build Frontend Image
echo "📦 Building frontend image..."
docker build -f Dockerfile.frontend -t $DOCKER_USERNAME/$PROJECT_NAME-frontend:latest ..
echo "✅ Frontend image built"

# Build Simple Backend Image
echo "📦 Building simple backend image..."
docker build -f Dockerfile.simple -t $DOCKER_USERNAME/$PROJECT_NAME-simple:latest ..
echo "✅ Simple backend image built"

# Build Combined Image (optional)
echo "📦 Building combined image..."
docker build -f Dockerfile -t $DOCKER_USERNAME/$PROJECT_NAME-app:latest ..
echo "✅ Combined image built"

echo ""
echo "🚀 Pushing Images to Docker Hub..."
echo "=================================="

# Push Backend
echo "⬆️ Pushing backend image..."
docker push $DOCKER_USERNAME/$PROJECT_NAME-backend:latest
echo "✅ Backend image pushed"

# Push Frontend
echo "⬆️ Pushing frontend image..."
docker push $DOCKER_USERNAME/$PROJECT_NAME-frontend:latest
echo "✅ Frontend image pushed"

# Push Simple Backend
echo "⬆️ Pushing simple backend image..."
docker push $DOCKER_USERNAME/$PROJECT_NAME-simple:latest
echo "✅ Simple backend image pushed"

# Push Combined
echo "⬆️ Pushing combined image..."
docker push $DOCKER_USERNAME/$PROJECT_NAME-app:latest
echo "✅ Combined image pushed"

echo ""
echo "🎉 All images successfully built and pushed!"
echo "==========================================="
echo ""
echo "📋 Available Images:"
echo "   - $DOCKER_USERNAME/$PROJECT_NAME-backend:latest"
echo "   - $DOCKER_USERNAME/$PROJECT_NAME-frontend:latest"
echo "   - $DOCKER_USERNAME/$PROJECT_NAME-simple:latest"
echo "   - $DOCKER_USERNAME/$PROJECT_NAME-app:latest"
echo ""
echo "🚀 Deploy with:"
echo "   docker-compose -f docker-compose.prod.yml up -d"
echo "   OR"
echo "   docker-compose -f docker-compose.simple-prod.yml up -d"
echo ""
echo "🔗 Docker Hub: https://hub.docker.com/u/$DOCKER_USERNAME"