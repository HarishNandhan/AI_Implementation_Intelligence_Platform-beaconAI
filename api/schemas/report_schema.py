from pydantic import BaseModel
from typing import Dict

class ReportRequest(BaseModel):
    company_name: str
    company_website: str
    persona: str
    insights: Dict[str, str]  # QuestionID → Insight text

class ReportResponse(BaseModel):
    status: str
    filepath: str
