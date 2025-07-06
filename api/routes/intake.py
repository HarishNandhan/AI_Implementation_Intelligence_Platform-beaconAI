from fastapi import APIRouter, HTTPException
from api.schemas.intake_schema import IntakeRequest, IntakeResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/submit", response_model=IntakeResponse)
def submit_intake(data: IntakeRequest):
    """
    Accepts the company intake form (company info + persona + CARE answers).
    """
    try:
        logger.info(f"[INTAKE] Received submission from: {data.company_info.company_name}")

        # For now, return success message (next: store it, pass to LLM, etc.)
        return {
            "status": "success",
            "message": f"Intake received for {data.company_info.company_name}",
            "submitted_data": data
        }

    except Exception as e:
        logger.error(f"[INTAKE ERROR] {e}")
        raise HTTPException(status_code=500, detail="Failed to process intake form.")
