# BeaconAI Deployment Guide

This folder contains all the necessary files for deploying the BeaconAI application using Docker.

## Files Overview

- **`Dockerfile.backend`** - Backend-only container (FastAPI + Uvicorn)
- **`Dockerfile.frontend`** - Frontend-only container (Streamlit)
- **`Dockerfile`** - Combined container (both backend and frontend)
- **`docker-compose.yml`** - Multi-container orchestration
- **`.env.docker`** - Environment variables template
- **`.dockerignore`** - Files to exclude from Docker build

## Deployment Options

### Option 1: Multi-Container with Docker Compose (Recommended for Development)

1. **Setup environment:**
   ```bash
   cd deployment
   copy .env.docker .env
   # Edit .env with your actual API keys
   ```

2. **Build and run:**
   ```bash
   docker-compose up --build
   ```

3. **Access:**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

### Option 2: Single Container (Good for Cloud Deployment)

1. **Build:**
   ```bash
   cd deployment
   docker build -f Dockerfile -t beaconai:latest ..
   ```

2. **Run:**
   ```bash
   docker run -p 8000:8000 -p 8501:8501 \
     -e HF_TOKEN=your_token \
     -e SENDGRID_API_KEY=your_key \
     beaconai:latest
   ```

### Option 3: Separate Containers

**Backend only:**
```bash
docker build -f Dockerfile.backend -t beaconai-backend ..
docker run -p 8000:8000 beaconai-backend
```

**Frontend only:**
```bash
docker build -f Dockerfile.frontend -t beaconai-frontend ..
docker run -p 8501:8501 -e BACKEND_URL=http://your-backend-url beaconai-frontend
```

## Environment Variables

Required environment variables:
- `HF_TOKEN` - Your Hugging Face API token
- `SENDGRID_API_KEY` - Your SendGrid API key
- `SENDER_EMAIL` - Email address for sending reports
- `BACKEND_URL` - Backend URL for frontend (in multi-container setup)

## Cloud Deployment

### AWS ECS
Use `Dockerfile.backend` and `Dockerfile.frontend` for separate services.

### Render/Railway
Use the main `Dockerfile` for single-container deployment.

### Docker Hub
Push images for use in cloud platforms:
```bash
docker build -f Dockerfile.backend -t yourusername/beaconai-backend ..
docker push yourusername/beaconai-backend
```

## Troubleshooting

1. **Port conflicts:** Change ports in docker-compose.yml if 8000/8501 are in use
2. **Chrome issues:** The Selenium scraper requires Chrome, which is installed in the containers
3. **Volume permissions:** Ensure generated_reports folder has proper permissions
4. **Health checks:** Services include health checks for monitoring

## Production Considerations

- Use environment-specific .env files
- Set up proper logging and monitoring
- Configure SSL/TLS for HTTPS
- Use secrets management for API keys
- Set up backup for generated reports
- Configure auto-scaling based on load