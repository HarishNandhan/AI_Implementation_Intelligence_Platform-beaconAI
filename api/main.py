from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import intake, insight, report, email
import logging
import os

# ---------- App Setup ----------
app = FastAPI(
    title="BeaconAI Insight API",
    description="Backend API for AI Implementation Intelligence Platform",
    version="1.0.0"
)

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting BeaconAI Insight Platform...")

# ---------- CORS Middleware ----------
origins = [
    "http://localhost:3000",  # React frontend running locally
    "http://localhost:8501",  # Streamlit running locally
    "http://127.0.0.1:3000",  # Some setups need this
    "http://127.0.0.1:8501",  # Streamlit alternative
    "http://frontend:8501",   # Docker container communication
    "http://beaconai-frontend:8501",  # Docker compose service name
    "https://your-frontend-domain.com"  # Production frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Health Check ----------
@app.get("/", tags=["Health"])
def root():
    return {"status": "OK", "message": "BeaconAI Insight API is live 🎯"}

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for Docker containers and load balancers"""
    return {
        "status": "healthy", 
        "service": "BeaconAI Backend", 
        "version": "1.0.0",
        "environment": "docker" if os.getenv("DOCKER_ENV") else "local"
    }

# ---------- Register Routes ----------
app.include_router(intake.router, prefix="/intake", tags=["Intake"])
app.include_router(insight.router, prefix="/insight", tags=["Insight"])
app.include_router(report.router, prefix="/report", tags=["Report"])
app.include_router(email.router, prefix="/email", tags=["Email"])
