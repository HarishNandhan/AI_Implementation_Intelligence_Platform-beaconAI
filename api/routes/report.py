from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from api.schemas.report_schema import ReportRequest, ReportResponse
from reporting.pdf_builder import generate_pdf_report, generate_pdf_to_buffer
from llm_engine.rag_engine import generate_solution_section, retrieve_context
from llm_engine.prompt_template import build_prompt
from llm_engine.llama_client import generate_llama_response
from care.question_bank import CARE_QUESTIONS
from scraper.selenium_scraper import scrape_company_website
from email_service.mailgun_client import MailgunClient
from google_sheets.sheets_client import sheets_client
import logging
import os
import base64

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=ReportResponse)
def generate_report(data: ReportRequest, request: Request):
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

        # Step 3: Generate PDF Report in Memory
        from io import BytesIO
        pdf_buffer = BytesIO()
        
        # Generate PDF directly to buffer
        pdf_content = generate_pdf_to_buffer(
            company_name=data.company_name,
            persona=data.persona,
            insights=formatted_insights,
            solution_section=solution_summary
        )
        
        # Create filename
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data.company_name.replace(' ', '_')}_{data.persona}_{timestamp}.pdf"

        # Step 4: Store Lead Information in Google Sheets (Optional)
        try:
            lead_data = {
                'email': data.user_email,
                'company_name': data.company_name,
                'company_website': data.company_website,
                'persona': data.persona,
                'report_filename': filename,
                'insights': data.insights,
                'ip_address': request.client.host if request.client else 'unknown',
                'user_agent': request.headers.get('user-agent', 'unknown')
            }
            
            # Save to Google Sheets (don't fail if this doesn't work)
            sheets_success = sheets_client.add_lead(lead_data)
            if sheets_success:
                logger.info(f"[SHEETS] Lead saved to Google Sheets: {data.user_email}")
            else:
                logger.warning(f"[SHEETS] Failed to save lead to Google Sheets: {data.user_email}")
        except Exception as sheets_error:
            logger.warning(f"[SHEETS] Google Sheets error: {str(sheets_error)}")

        # Step 5: Email Sending (Optional - graceful fallback if not configured)
        email_sent = False
        email_status = "Download available"
        mailgun_id = None
        
        # Try to send email if Mailgun is configured
        try:
            # Check if Mailgun is configured
            mailgun_api_key = os.getenv("MAILGUN_API_KEY")
            mailgun_domain = os.getenv("MAILGUN_DOMAIN")
            
            # Debug logging
            logger.info(f"[REPORT] Mailgun config check:")
            logger.info(f"  API Key: {'SET' if mailgun_api_key else 'NOT SET'} (length: {len(mailgun_api_key) if mailgun_api_key else 0})")
            logger.info(f"  Domain: {mailgun_domain}")
            logger.info(f"  API Key is placeholder: {mailgun_api_key == 'your_mailgun_api_key_here'}")
            
            if mailgun_api_key and mailgun_domain and mailgun_api_key != "your_mailgun_api_key_here":
                logger.info(f"[REPORT] Attempting to send email to: {data.user_email}")
                try:
                    mailgun_client = MailgunClient()
                except ValueError as config_error:
                    logger.error(f"[REPORT] Mailgun configuration error: {str(config_error)}")
                    email_status = f"Email configuration error: {str(config_error)} - Download available"
                    mailgun_client = None
                
                if mailgun_client:
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
                        email_status = f"Email sending failed: {email_result['message']} - Download available"
                        logger.warning(f"[REPORT] Email sending failed: {email_result['message']}")
                else:
                    email_status = "Email configuration error - Download available"
            else:
                email_status = "Email not configured - Download available"
                logger.info(f"[REPORT] Mailgun not configured, email capture only: {data.user_email}")
                
        except Exception as email_error:
            email_status = f"Email sending error: {str(email_error)} - Download available"
            logger.error(f"[REPORT] Email sending error: {str(email_error)}")

        # Return response with PDF content for direct download        
        return ReportResponse(
            status="success",
            pdf_content=base64.b64encode(pdf_content).decode('utf-8'),
            filename=filename,
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

@router.get("/leads/count")
def get_leads_count():
    """Get total number of leads captured in Google Sheets"""
    try:
        count = sheets_client.get_leads_count()
        return {"total_leads": count, "source": "google_sheets"}
    except Exception as e:
        logger.error(f"[LEADS ERROR] {e}")
        raise HTTPException(status_code=500, detail="Failed to get leads count")

@router.post("/sheets/setup")
def setup_sheets_headers():
    """Setup headers in Google Sheets (run once)"""
    try:
        success = sheets_client.setup_sheet_headers()
        if success:
            return {"status": "success", "message": "Google Sheets headers setup successfully"}
        else:
            return {"status": "error", "message": "Failed to setup Google Sheets headers"}
    except Exception as e:
        logger.error(f"[SHEETS SETUP ERROR] {e}")
        raise HTTPException(status_code=500, detail="Failed to setup Google Sheets headers")

@router.post("/test")
def test_endpoint():
    """Simple test endpoint to check if backend is working"""
    return {"status": "success", "message": "Backend is working"}

@router.post("/test-pdf")
def test_pdf_generation():
    """Test PDF generation without email or sheets"""
    try:
        
        # Simple test data
        test_insights = {
            "C1": {
                "question": "Test question",
                "answer": "Test answer", 
                "insight": "Test insight"
            }
        }
        
        # Generate PDF
        pdf_content = generate_pdf_to_buffer(
            company_name="Test Company",
            persona="CTO",
            insights=test_insights,
            solution_section="Test solution"
        )
        
        return {
            "status": "success",
            "pdf_size": len(pdf_content),
            "message": "PDF generated successfully"
        }
        
    except Exception as e:
        logger.error(f"[TEST PDF ERROR] {e}")
        return {"status": "error", "message": str(e)}

@router.post("/test-email")
def test_email_sending():
    """Test email sending functionality"""
    try:
        # Check if Mailgun is configured
        mailgun_api_key = os.getenv("MAILGUN_API_KEY")
        mailgun_domain = os.getenv("MAILGUN_DOMAIN")
        
        if not mailgun_api_key or mailgun_api_key == "your_mailgun_api_key_here":
            return {"status": "error", "message": "Mailgun API key not configured"}
        
        if not mailgun_domain or mailgun_domain == "your_domain.com":
            return {"status": "error", "message": "Mailgun domain not configured"}
        
        # Try to initialize Mailgun client
        try:
            mailgun_client = MailgunClient()
        except ValueError as config_error:
            return {"status": "error", "message": f"Mailgun configuration error: {str(config_error)}"}
        
        # Test connection
        connection_test = mailgun_client.test_connection()
        
        return {
            "status": "success" if connection_test["success"] else "error",
            "message": connection_test["message"],
            "mailgun_configured": True,
            "api_key_set": bool(mailgun_api_key and mailgun_api_key != "your_mailgun_api_key_here"),
            "domain_set": bool(mailgun_domain and mailgun_domain != "your_domain.com")
        }
        
    except Exception as e:
        logger.error(f"[TEST EMAIL ERROR] {e}")
        return {"status": "error", "message": str(e)}





