from fastapi import APIRouter, HTTPException
from api.schemas.insight_schema import InsightRequest, InsightResponse
from llm_engine.prompt_template import build_prompt
from llm_engine.llama_client import generate_llama_response
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=InsightResponse)
def generate_insight(data: InsightRequest):
    """
    Generate a strategic insight based on persona, question, answer, and company info.
    """
    try:
        logger.info(f"[INSIGHT] Generating insight for {data.persona} at {data.company_name}")

        # 1. Build prompt using logic
        prompt = build_prompt(
            persona=data.persona,
            company_name=data.company_name,
            category=data.category,
            question=data.question,
            answer=data.answer,
            company_summary=data.company_summary
        )

        # 2. Send to LLAMA API and get response
        insight_text = generate_llama_response(prompt)

        return InsightResponse(
            status="success",
            persona=data.persona,
            insight=insight_text.strip()
        )

    except Exception as e:
        logger.error(f"[INSIGHT ERROR] {e}")
        raise HTTPException(status_code=500, detail="Insight generation failed.")
