from fastapi import APIRouter, HTTPException
from api.schemas.email_schema import EmailRequest, EmailResponse, EmailTestRequest, EmailTestResponse
from email_service.mailgun_client import MailgunClient
import logging
import os

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/send-report", response_model=EmailResponse)
async def send_report_email(data: EmailRequest):
    """
    Sends the AI Readiness Report PDF to the user's email via Mailgun.
    
    Args:
        data: EmailRequest containing recipient email, company info, and PDF path
        
    Returns:
        EmailResponse with success/failure status and Mailgun message ID
    """
    try:
        logger.info(f"[EMAIL] Sending report to: {data.email_address} for {data.company_name}")
        
        # Initialize Mailgun client
        mailgun_client = MailgunClient()
        
        # Check if PDF file exists
        if not os.path.exists(data.filepath):
            logger.error(f"[EMAIL] PDF file not found: {data.filepath}")
            raise HTTPException(status_code=404, detail="PDF file not found")
        
        # Read PDF file
        with open(data.filepath, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        # Extract filename from path
        filename = os.path.basename(data.filepath)
        
        # Send email with PDF attachment
        result = mailgun_client.send_report_email(
            recipient_email=data.email_address,
            company_name=data.company_name,
            persona=data.persona,
            pdf_content=pdf_content,
            pdf_filename=filename
        )
        
        if result["success"]:
            logger.info(f"[EMAIL] Successfully sent report to {data.email_address}")
            return EmailResponse(
                status="success",
                message=f"Report sent successfully to {data.email_address}",
                mailgun_id=result.get("mailgun_id")
            )
        else:
            logger.error(f"[EMAIL] Failed to send report: {result['message']}")
            raise HTTPException(
                status_code=result.get("status_code", 500),
                detail=f"Failed to send email: {result['message']}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[EMAIL ERROR] Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@router.post("/test-connection", response_model=EmailTestResponse)
async def test_email_connection():
    """
    Test Mailgun connection and configuration.
    
    Returns:
        EmailTestResponse with connection test results
    """
    try:
        logger.info("[EMAIL] Testing Mailgun connection")
        
        # Initialize Mailgun client
        mailgun_client = MailgunClient()
        
        # Test connection
        result = mailgun_client.test_connection()
        
        if result["success"]:
            logger.info("[EMAIL] Mailgun connection test successful")
            return EmailTestResponse(
                status="success",
                message="Mailgun connection successful",
                connection_test=True
            )
        else:
            logger.error(f"[EMAIL] Mailgun connection test failed: {result['message']}")
            return EmailTestResponse(
                status="error",
                message=f"Connection test failed: {result['message']}",
                connection_test=False
            )
            
    except Exception as e:
        logger.error(f"[EMAIL] Connection test error: {str(e)}")
        return EmailTestResponse(
            status="error",
            message=f"Connection test error: {str(e)}",
            connection_test=False
        )

@router.post("/send-test", response_model=EmailResponse)
async def send_test_email(data: EmailTestRequest):
    """
    Send a test email to verify Mailgun integration.
    
    Args:
        data: EmailTestRequest containing recipient email
        
    Returns:
        EmailResponse with test email results
    """
    try:
        logger.info(f"[EMAIL] Sending test email to: {data.email_address}")
        
        # Initialize Mailgun client
        mailgun_client = MailgunClient()
        
        # Send test email
        result = mailgun_client.send_email(
            to_email=data.email_address,
            subject="🧪 BeaconAI Email Test - Integration Working!",
            html_content="""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #0A3161; color: white; padding: 30px; text-align: center;">
                    <h1 style="margin: 0;">🎉 BeaconAI Email Test</h1>
                    <p style="margin: 10px 0 0 0;">Email Integration Successful!</p>
                </div>
                <div style="background-color: #FFA500; height: 5px;"></div>
                <div style="padding: 30px;">
                    <h2 style="color: #0A3161;">✅ Integration Test Successful!</h2>
                    <p>If you're reading this email, your Mailgun integration is working perfectly!</p>
                    <div style="background-color: #f0f8ff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #FFA500; margin-top: 0;">What this confirms:</h3>
                        <ul>
                            <li>✅ Mailgun API connection is working</li>
                            <li>✅ Email templates are rendering correctly</li>
                            <li>✅ Your domain configuration is valid</li>
                            <li>✅ Ready to send AI readiness reports!</li>
                        </ul>
                    </div>
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        This is a test email from your BeaconAI application's email service.
                    </p>
                </div>
                <div style="background-color: #0A3161; color: white; padding: 20px; text-align: center;">
                    <p style="margin: 0; font-size: 12px;">© 2024 BeaconAI. All rights reserved.</p>
                </div>
            </body>
            </html>
            """,
            text_content="BeaconAI Email Test - Integration Working! If you're reading this, your Mailgun integration is successful."
        )
        
        if result["success"]:
            logger.info(f"[EMAIL] Test email sent successfully to {data.email_address}")
            return EmailResponse(
                status="success",
                message=f"Test email sent successfully to {data.email_address}",
                mailgun_id=result.get("mailgun_id")
            )
        else:
            logger.error(f"[EMAIL] Failed to send test email: {result['message']}")
            raise HTTPException(
                status_code=result.get("status_code", 500),
                detail=f"Failed to send test email: {result['message']}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[EMAIL] Test email error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send test email: {str(e)}")
