from fastapi import APIRouter, HTTPException
from api.schemas.email_schema import EmailRequest, EmailResponse
from email_service.sendgrid_client import send_email_with_attachment
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/send", response_model=EmailResponse)
def send_report_email(data: EmailRequest):
    """
    Sends the AI Readiness Report PDF to the user's email.
    """
    try:
        logger.info(f"[EMAIL] Sending report to: {data.email_address}")
        send_email_with_attachment(data.email_address, data.filepath)

        return EmailResponse(
            status="success",
            message=f"Report sent to {data.email_address}"
        )

    except Exception as e:
        logger.error(f"[EMAIL ERROR] {e}")
        raise HTTPException(status_code=500, detail="Failed to send email.")
