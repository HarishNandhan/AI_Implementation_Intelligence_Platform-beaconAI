from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import intake, insight, report, email
import logging

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
    "http://localhost:8501",  # Optional: if using Streamlit
    "http://127.0.0.1:3000",  # Some setups need this
    "https://your-frontend-domain.com"  # Leave for future use
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
def health_check():
    return {"status": "OK", "message": "BeaconAI Insight API is live 🎯"}

# ---------- Register Routes ----------
app.include_router(intake.router, prefix="/intake", tags=["Intake"])
app.include_router(insight.router, prefix="/insight", tags=["Insight"])
app.include_router(report.router, prefix="/report", tags=["Report"])
app.include_router(email.router, prefix="/email", tags=["Email"])
