from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from api.schemas.report_schema import ReportRequest, ReportResponse
from reporting.pdf_builder import generate_pdf_report
from llm_engine.rag_engine import generate_solution_section, retrieve_context
from llm_engine.prompt_template import build_prompt
from llm_engine.llama_client import generate_llama_response
from care.question_bank import CARE_QUESTIONS
from scraper.selenium_scraper import scrape_company_website
from email_service.mailgun_client import MailgunClient
import logging
import os

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=ReportResponse)
def generate_report(data: ReportRequest):
    """
    Generates a branded PDF report based on the insights and company info.
    Includes web-scraped company context and a BeaconAI solution section.
    """
    try:
        logger.info(f"[REPORT] Generating report for: {data.company_name} ({data.persona})")

        # Step 0: Scrape Company Website Content
        logger.info(f"[SCRAPER] Extracting content from: {data.company_website}")
        company_context_text = scrape_company_website(data.company_website)

        formatted_insights = {}

        # Step 1: Generate insights for each CARE question
        for qid, answer in data.insights.items():
            question_text = CARE_QUESTIONS[qid]["question"]
            category = qid[0]  # C, A, R, or E

            # Retrieve RAG chunks from knowledge base
            retrieved_chunks = retrieve_context(question_text)
            rag_context = f"{company_context_text}\n" + "\n".join(retrieved_chunks)

            # Build and send prompt to LLM
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

        # Step 2: Generate final BeaconAI Solution Summary
        all_insight_texts = [v["insight"] for v in formatted_insights.values()]
        solution_summary = generate_solution_section(all_insight_texts, company_context_text)

        # Step 3: Generate PDF Report
        filepath = generate_pdf_report(
            company_name=data.company_name,
            persona=data.persona,
            insights=formatted_insights,
            solution_section=solution_summary
        )

        # Step 4: Send Email (if email address provided)
        email_sent = False
        email_status = None
        mailgun_id = None
        
        if data.user_email:
            try:
                logger.info(f"[REPORT] Sending email to: {data.user_email}")
                
                # Initialize Mailgun client
                mailgun_client = MailgunClient()
                
                # Read PDF file for email attachment
                with open(filepath, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                
                # Extract filename from path
                filename = os.path.basename(filepath)
                
                # Send email with PDF attachment
                email_result = mailgun_client.send_report_email(
                    recipient_email=data.user_email,
                    company_name=data.company_name,
                    persona=data.persona,
                    pdf_content=pdf_content,
                    pdf_filename=filename
                )
                
                if email_result["success"]:
                    email_sent = True
                    email_status = f"Report sent successfully to {data.user_email}"
                    mailgun_id = email_result.get("mailgun_id")
                    logger.info(f"[REPORT] Email sent successfully to {data.user_email}")
                else:
                    email_sent = False
                    email_status = f"Failed to send email: {email_result['message']}"
                    logger.error(f"[REPORT] Email sending failed: {email_result['message']}")
                    
            except Exception as email_error:
                email_sent = False
                email_status = f"Email sending error: {str(email_error)}"
                logger.error(f"[REPORT] Email sending error: {str(email_error)}")
                # Don't fail the entire request if email fails
        else:
            logger.info("[REPORT] No email address provided, skipping email sending")

        return ReportResponse(
            status="success", 
            filepath=filepath,
            email_sent=email_sent,
            email_status=email_status,
            mailgun_id=mailgun_id
        )

    except Exception as e:
        logger.error(f"[REPORT ERROR] {e}")
        raise HTTPException(status_code=500, detail="Failed to generate report.")

@router.post("/generate-and-email", response_model=ReportResponse)
def generate_and_email_report(data: ReportRequest):
    """
    Generates a PDF report and automatically emails it to the user.
    This endpoint requires user_email to be provided.
    """
    try:
        # Validate that email is provided
        if not data.user_email:
            raise HTTPException(
                status_code=400, 
                detail="Email address is required for this endpoint"
            )
        
        logger.info(f"[REPORT] Generating and emailing report for: {data.company_name} ({data.persona}) to {data.user_email}")

        # Step 0: Scrape Company Website Content
        logger.info(f"[SCRAPER] Extracting content from: {data.company_website}")
        company_context_text = scrape_company_website(data.company_website)

        formatted_insights = {}

        # Step 1: Generate insights for each CARE question
        for qid, answer in data.insights.items():
            question_text = CARE_QUESTIONS[qid]["question"]
            category = qid[0]  # C, A, R, or E

            # Retrieve RAG chunks from knowledge base
            retrieved_chunks = retrieve_context(question_text)
            rag_context = f"{company_context_text}\n" + "\n".join(retrieved_chunks)

            # Build and send prompt to LLM
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

        # Step 2: Generate final BeaconAI Solution Summary
        all_insight_texts = [v["insight"] for v in formatted_insights.values()]
        solution_summary = generate_solution_section(all_insight_texts, company_context_text)

        # Step 3: Generate PDF Report
        filepath = generate_pdf_report(
            company_name=data.company_name,
            persona=data.persona,
            insights=formatted_insights,
            solution_section=solution_summary
        )

        # Step 4: Send Email (Required for this endpoint)
        try:
            logger.info(f"[REPORT] Sending email to: {data.user_email}")
            
            # Initialize Mailgun client
            mailgun_client = MailgunClient()
            
            # Read PDF file for email attachment
            with open(filepath, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
            
            # Extract filename from path
            filename = os.path.basename(filepath)
            
            # Send email with PDF attachment
            email_result = mailgun_client.send_report_email(
                recipient_email=data.user_email,
                company_name=data.company_name,
                persona=data.persona,
                pdf_content=pdf_content,
                pdf_filename=filename
            )
            
            if email_result["success"]:
                logger.info(f"[REPORT] Email sent successfully to {data.user_email}")
                return ReportResponse(
                    status="success", 
                    filepath=filepath,
                    email_sent=True,
                    email_status=f"Report sent successfully to {data.user_email}",
                    mailgun_id=email_result.get("mailgun_id")
                )
            else:
                logger.error(f"[REPORT] Email sending failed: {email_result['message']}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Report generated but email failed: {email_result['message']}"
                )
                
        except Exception as email_error:
            logger.error(f"[REPORT] Email sending error: {str(email_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Report generated but email failed: {str(email_error)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[REPORT ERROR] {e}")
        raise HTTPException(status_code=500, detail="Failed to generate and email report.")


@router.get("/download/{filename}")
def download_report(filename: str):
    """
    Download endpoint for PDF reports - needed for Docker containers
    where frontend can't access backend filesystem directly
    """
    try:
        # Construct the full file path - use absolute path in Docker
        if os.getenv("DOCKER_ENV"):
            file_path = os.path.join("/app/generated_reports", filename)
        else:
            file_path = os.path.join("generated_reports", filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"[DOWNLOAD] File not found: {file_path}")
            # List available files for debugging
            reports_dir = "/app/generated_reports" if os.getenv("DOCKER_ENV") else "generated_reports"
            if os.path.exists(reports_dir):
                available_files = os.listdir(reports_dir)
                logger.error(f"[DOWNLOAD] Available files: {available_files}")
            raise HTTPException(status_code=404, detail=f"Report file not found: {filename}")
        
        # Validate file extension for security
        if not filename.lower().endswith('.pdf'):
            logger.error(f"[DOWNLOAD] Invalid file type: {filename}")
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        logger.info(f"[DOWNLOAD] Serving file: {file_path}")
        
        return FileResponse(
            path=file_path,
            media_type='application/pdf',
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[DOWNLOAD ERROR] {e}")
        raise HTTPException(status_code=500, detail="Failed to download report")
