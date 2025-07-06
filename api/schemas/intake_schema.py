from pydantic import BaseModel, HttpUrl
from typing import Dict, Optional

class CompanyInfo(BaseModel):
    company_name: str
    company_website: HttpUrl
    about_page_url: Optional[HttpUrl] = None

class UserInfo(BaseModel):
    persona: str
    custom_role: Optional[str] = None
    optional_description: Optional[str] = None
    optional_expectations: Optional[str] = None

class IntakeRequest(BaseModel):
    company_info: CompanyInfo
    user_info: UserInfo
    answers: Dict[str, str]  # CARE Question ID → Answer

class IntakeResponse(BaseModel):
    status: str
    message: str
    submitted_data: IntakeRequest
