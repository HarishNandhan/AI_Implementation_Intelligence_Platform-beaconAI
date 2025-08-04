from pydantic import BaseModel, EmailStr
from typing import Optional

class EmailRequest(BaseModel):
    email_address: EmailStr
    company_name: str
    persona: str
    filepath: str  # Path to PDF file
    
class EmailResponse(BaseModel):
    status: str
    message: str
    mailgun_id: Optional[str] = None
    
class EmailTestRequest(BaseModel):
    email_address: EmailStr
    
class EmailTestResponse(BaseModel):
    status: str
    message: str
    connection_test: bool
