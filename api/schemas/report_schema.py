from pydantic import BaseModel, EmailStr
from typing import Dict, Optional

class ReportRequest(BaseModel):
    company_name: str
    company_website: str
    persona: str
    insights: Dict[str, str]  # QuestionID → Insight text
    user_email: EmailStr  # Required email for sending report

class ReportResponse(BaseModel):
    status: str
    pdf_content: Optional[str] = None  # Base64 encoded PDF content
    filename: Optional[str] = None  # PDF filename
    filepath: Optional[str] = None  # File path (for backward compatibility)
    email_sent: Optional[bool] = None  # Whether email was sent
    email_status: Optional[str] = None  # Email sending status message
    mailgun_id: Optional[str] = None  # Mailgun message ID if email sent
