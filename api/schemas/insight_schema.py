from pydantic import BaseModel
from typing import Optional

# Request model for insight generation
class InsightRequest(BaseModel):
    persona: str
    company_name: str
    category: str
    question: str
    answer: str
    company_summary: Optional[str] = ""  # Optional context from RAG or scraper

# Response model for returning the generated insight
class InsightResponse(BaseModel):
    status: str
    persona: str
    insight: str
