from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    email_address: EmailStr
    filepath: str  # Path to PDF

class EmailResponse(BaseModel):
    status: str
    message: str
