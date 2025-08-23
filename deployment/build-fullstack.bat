@echo off
REM Build script for BeaconAI Full-stack Docker Image (Windows)

echo 🚀 Building BeaconAI Full-stack Docker Image (Frontend + Backend)...

REM Set variables
set IMAGE_NAME=harishnandhan02/beaconai-fullstack
set TAG=latest
set FULL_IMAGE_NAME=%IMAGE_NAME%:%TAG%

REM Build the Docker image
echo 📦 Building Docker image: %FULL_IMAGE_NAME%
docker build -f deployment/Dockerfile.fullstack -t %FULL_IMAGE_NAME% .

REM Check if build was successful
if %ERRORLEVEL% EQU 0 (
    echo ✅ Docker image built successfully!
    echo 📋 Image details:
    docker images %IMAGE_NAME%
    
    echo.
    echo 🔄 To push to Docker Hub, run:
    echo docker push %FULL_IMAGE_NAME%
    
    echo.
    echo 🧪 To test locally, run:
    echo docker run -p 8080:8080 -p 8000:8000 ^
    echo   -e DOCKER_ENV=true ^
    echo   -e HF_TOKEN=your_hf_token ^
    echo   -e BACKEND_URL=http://localhost:8000 ^
    echo   %FULL_IMAGE_NAME%
) else (
    echo ❌ Docker build failed!
    exit /b 1
)