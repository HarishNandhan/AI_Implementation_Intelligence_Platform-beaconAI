from fastapi import APIRouter, HTTPException
from api.schemas.insight_schema import InsightRequest, InsightResponse
from llm_engine.prompt_template import build_prompt
from llm_engine.llama_client import generate_llama_response
from llm_engine.rag_engine import retrieve_context  # ✅ NEW
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=InsightResponse)
def generate_insight(data: InsightRequest):
    try:
        logger.info(f"[INSIGHT] Generating insight for {data.persona} at {data.company_name}")

        # ✅ Step 1: Retrieve top-k chunks using question as query
        rag_chunks = retrieve_context(data.question)
        rag_context = "\n".join(rag_chunks) if rag_chunks else ""

        # ✅ Step 2: Build a prompt including retrieved RAG context
        prompt = build_prompt(
            persona=data.persona,
            company_name=data.company_name,
            category=data.category,
            question=data.question,
            answer=data.answer,
            company_summary=data.company_summary,
            rag_context=rag_context  # ✅ Injected
        )

        # Step 3: Generate insight using LLM
        insight_text = generate_llama_response(prompt)

        return InsightResponse(
            status="success",
            persona=data.persona,
            insight=insight_text.strip()
        )

    except Exception as e:
        logger.error(f"[INSIGHT ERROR] {e}")
        raise HTTPException(status_code=500, detail="Insight generation failed.")
