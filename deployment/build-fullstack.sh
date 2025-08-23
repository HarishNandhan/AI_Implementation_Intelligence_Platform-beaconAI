#!/bin/bash

# Build script for BeaconAI Full-stack Docker Image

echo "🚀 Building BeaconAI Full-stack Docker Image (Frontend + Backend)..."

# Set variables
IMAGE_NAME="harishnandhan02/beaconai-fullstack"
TAG="latest"
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

# Build the Docker image
echo "📦 Building Docker image: ${FULL_IMAGE_NAME}"
docker build -f deployment/Dockerfile.fullstack -t ${FULL_IMAGE_NAME} .

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
    echo "docker run -p 8080:8080 -p 8000:8000 \\"
    echo "  -e DOCKER_ENV=true \\"
    echo "  -e HF_TOKEN=your_hf_token \\"
    echo "  -e BACKEND_URL=http://localhost:8000 \\"
    echo "  ${FULL_IMAGE_NAME}"
else
    echo "❌ Docker build failed!"
    exit 1
fi