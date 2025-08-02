from fastapi import APIRouter, HTTPException
from api.schemas.report_schema import ReportRequest, ReportResponse
from reporting.pdf_builder import generate_pdf_report
from llm_engine.rag_engine import generate_solution_section, retrieve_context
from llm_engine.prompt_template import build_prompt
from llm_engine.llama_client import generate_llama_response
from care.question_bank import CARE_QUESTIONS
from scraper.selenium_scraper import scrape_company_website
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=ReportResponse)
def generate_report(data: ReportRequest):
    """
    Generates a branded PDF report based on the insights and company info.
    Includes a final BeaconAI solution section tailored to the client's challenges.
    """
    try:
        logger.info(f"[REPORT] Generating report for: {data.company_name} ({data.persona})")

        formatted_insights = {}

        # Step 1: Generate individual insights per CARE question
        for qid, answer in data.insights.items():
            question_text = CARE_QUESTIONS[qid]["question"]
            category = qid[0]  # C, A, R, or E

            rag_context = "\n".join(retrieve_context(question_text))

            prompt = build_prompt(
                persona=data.persona,
                company_name=data.company_name,
                category=category,
                question=question_text,
                answer=answer,
                company_summary="",
                rag_context=rag_context
            )

            insight = generate_llama_response(prompt)

            formatted_insights[qid] = {
                "question": question_text,
                "answer": answer,
                "insight": insight
            }

        # Step 2: Generate final BeaconAI solution summary
        all_insight_texts = [v["insight"] for v in formatted_insights.values()]
        solution_summary = generate_solution_section(all_insight_texts)

        # Step 3: Generate the PDF report
        filepath = generate_pdf_report(
            company_name=data.company_name,
            persona=data.persona,
            insights=formatted_insights,
            solution_section=solution_summary
        )

        return ReportResponse(status="success", filepath=filepath)

    except Exception as e:
        logger.error(f"[REPORT ERROR] {e}")
        raise HTTPException(status_code=500, detail="Failed to generate report.")


