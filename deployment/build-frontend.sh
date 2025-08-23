#!/bin/bash

# Build script for BeaconAI Frontend Docker Image

echo "🚀 Building BeaconAI Frontend Docker Image..."

# Set variables
IMAGE_NAME="harishnandhan02/beaconai-frontend"
TAG="latest"
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

# Build the Docker image
echo "📦 Building Docker image: ${FULL_IMAGE_NAME}"
docker build -f deployment/Dockerfile.frontend -t ${FULL_IMAGE_NAME} .

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo "📋 Image details:"
    docker images ${IMAGE_NAME}
    
    echo ""
    echo "🔄 To push to Docker Hub, run:"
    echo "docker push ${FULL_IMAGE_NAME}"
    
    echo ""
    echo "🧪 To test locally, run:"
    echo "docker run -p 8080:8080 -e BACKEND_URL=http://your-backend-url ${FULL_IMAGE_NAME}"
else
    echo "❌ Docker build failed!"
    exit 1
fi