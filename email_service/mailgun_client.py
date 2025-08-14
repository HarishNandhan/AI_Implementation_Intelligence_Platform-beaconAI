import os
import requests
import base64
import logging
from typing import Optional, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MailgunClient:
    """
    Mailgun email client for sending emails with PDF attachments
    """
    
    def __init__(self):
        """Initialize Mailgun client with configuration"""
        self.api_key = os.getenv("MAILGUN_API_KEY")
        self.domain = os.getenv("MAILGUN_DOMAIN") 
        self.base_url = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net/v3")
        self.sender_email = os.getenv("SENDER_EMAIL", "harish@beaconai.ai")
        self.sender_name = os.getenv("SENDER_NAME", "Harish - beaconAI Team")
        
        # Validate configuration
        if not self.api_key or self.api_key == "your_mailgun_api_key_here":
            raise ValueError("MAILGUN_API_KEY environment variable is required and must be set to a valid API key")
        if not self.domain or self.domain == "your_domain.com":
            raise ValueError("MAILGUN_DOMAIN environment variable is required and must be set to a valid domain")
        
        logger.info(f"Mailgun client initialized for domain: {self.domain}")
    
    def send_email(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str, 
        text_content: Optional[str] = None,
        attachments: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Send email via Mailgun API
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            html_content: HTML email content
            text_content: Plain text email content (optional)
            attachments: List of attachment dictionaries (optional)
            
        Returns:
            Dictionary with success status and response details
        """
        try:
            # Prepare email data
            email_data = {
                "from": f"{self.sender_name} <{self.sender_email}>",
                "to": to_email,
                "subject": subject,
                "html": html_content
            }
            
            # Add text content if provided
            if text_content:
                email_data["text"] = text_content
            
            # Prepare files for attachments
            files = []
            if attachments:
                for attachment in attachments:
                    files.append((
                        "attachment",
                        (attachment["filename"], attachment["content"], attachment["content_type"])
                    ))
            
            # Send email via Mailgun API
            response = requests.post(
                f"{self.base_url}/{self.domain}/messages",
                auth=("api", self.api_key),
                data=email_data,
                files=files if files else None,
                timeout=30
            )
            
            # Handle response
            if response.status_code == 200:
                logger.info(f"Email sent successfully to {to_email}")
                return {
                    "success": True,
                    "message": "Email sent successfully",
                    "mailgun_id": response.json().get("id"),
                    "status_code": response.status_code
                }
            else:
                logger.error(f"Failed to send email to {to_email}. Status: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return {
                    "success": False,
                    "message": f"Failed to send email: {response.text}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout sending email to {to_email}")
            return {
                "success": False,
                "message": "Email sending timed out",
                "status_code": 408
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error sending email to {to_email}: {str(e)}")
            return {
                "success": False,
                "message": f"Request error: {str(e)}",
                "status_code": 500
            }
        except Exception as e:
            logger.error(f"Unexpected error sending email to {to_email}: {str(e)}")
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}",
                "status_code": 500
            }
    
    def send_report_email(
        self, 
        recipient_email: str, 
        company_name: str, 
        persona: str,
        pdf_content: bytes, 
        pdf_filename: str
    ) -> Dict[str, Any]:
        """
        Send AI readiness report email with PDF attachment
        
        Args:
            recipient_email: Recipient's email address
            company_name: Company name for personalization
            persona: User's role (CTO, CEO, etc.)
            pdf_content: PDF file content as bytes
            pdf_filename: Name of the PDF file
            
        Returns:
            Dictionary with success status and response details
        """
        try:
            # Create email subject
            subject = f"Your AI Readiness Assessment Report - {company_name}"
            
            # Create HTML email content
            html_content = self._create_report_email_html(
                recipient_email, 
                company_name, 
                persona
            )
            
            # Create text version
            text_content = self._create_report_email_text(
                recipient_email, 
                company_name, 
                persona
            )
            
            # Prepare PDF attachment
            attachments = [{
                "filename": pdf_filename,
                "content": pdf_content,
                "content_type": "application/pdf"
            }]
            
            # Send email
            result = self.send_email(
                to_email=recipient_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                attachments=attachments
            )
            
            logger.info(f"Report email sent to {recipient_email} for {company_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error sending report email: {str(e)}")
            return {
                "success": False,
                "message": f"Error sending report email: {str(e)}",
                "status_code": 500
            }
    
    def _create_report_email_html(self, recipient_email: str, company_name: str, persona: str) -> str:
        """Create HTML email template for report delivery"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your AI Readiness Report</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 0;">
                
                <!-- Header -->
                <div style="background-color: #0A3161; color: white; padding: 30px 40px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: bold;">beaconAI</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">AI Implementation Intelligence Platform</p>
                </div>
                
                <!-- Amber accent line -->
                <div style="background-color: #FFA500; height: 5px;"></div>
                
                <!-- Main content -->
                <div style="padding: 40px;">
                    <h2 style="color: #0A3161; margin-top: 0; font-size: 24px;">Your AI Readiness Assessment Report</h2>
                    
                    <p style="font-size: 16px; margin-bottom: 20px;">Dear {persona},</p>
                    
                    <p style="font-size: 16px; margin-bottom: 20px;">
                        Thank you for completing the beaconAI AI Readiness Assessment for <strong>{company_name}</strong>. 
                        Your personalized report is now ready and attached to this email.
                    </p>
                    
                    <div style="background-color: #f8f9fa; border-left: 4px solid #FFA500; padding: 20px; margin: 30px 0;">
                        <h3 style="color: #0A3161; margin-top: 0; font-size: 18px;">📊 What's Inside Your Report:</h3>
                        <ul style="margin: 15px 0; padding-left: 20px;">
                            <li style="margin-bottom: 8px;">Comprehensive CARE framework analysis</li>
                            <li style="margin-bottom: 8px;">Strategic insights tailored to your organization</li>
                            <li style="margin-bottom: 8px;">Actionable recommendations for AI implementation</li>
                            <li style="margin-bottom: 8px;">Next steps for your AI transformation journey</li>
                        </ul>
                    </div>
                    
                    <p style="font-size: 16px; margin-bottom: 30px;">
                        The attached PDF contains detailed insights based on your responses, along with strategic 
                        recommendations to accelerate your AI adoption journey.
                    </p>
                    
                    <!-- Call-to-action buttons -->
                    <div style="text-align: center; margin: 40px 0;">
                        <a href="https://app.usemotion.com/meet/dalemyska/linkedin" 
                           style="display: inline-block; background-color: #FFA500; color: white; padding: 15px 30px; 
                                  text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px; margin: 10px;">
                            📅 Schedule Strategy Session
                        </a>
                        <br>
                        <a href="https://www.beaconai.ai" 
                           style="display: inline-block; background-color: #008080; color: white; padding: 15px 30px; 
                                  text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px; margin: 10px;">
                            🌐 Learn More About beaconAI
                        </a>
                    </div>
                    
                    <div style="background-color: #e8f4f8; border-radius: 8px; padding: 25px; margin: 30px 0;">
                        <h3 style="color: #0A3161; margin-top: 0; font-size: 18px;">🚀 Ready to Transform Your AI Strategy?</h3>
                        <p style="margin-bottom: 15px;">
                            Our team is ready to help you implement these insights and accelerate your AI transformation.
                        </p>
                        <p style="margin-bottom: 0;">
                            <strong>Next Steps:</strong> Schedule a complimentary strategy session to discuss your 
                            specific AI implementation roadmap.
                        </p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background-color: #0A3161; color: white; padding: 30px 40px; text-align: center;">
                    <h3 style="margin: 0 0 20px 0; font-size: 18px;">Contact BeaconAI</h3>
                    <p style="margin: 5px 0; font-size: 14px;">
                        📧 Email: <a href="mailto:info@beaconai.ai" style="color: #FFA500;">info@beaconai.ai</a>
                    </p>
                    <p style="margin: 5px 0; font-size: 14px;">
                        📞 Phone: <a href="tel:+13038774292" style="color: #FFA500;">+1 (303) 877-4292</a>
                    </p>
                    <p style="margin: 5px 0; font-size: 14px;">
                        🌐 Website: <a href="https://www.beaconai.ai" style="color: #FFA500;">www.beaconai.ai</a>
                    </p>
                    <p style="margin: 20px 0 0 0; font-size: 12px; opacity: 0.8;">
                        © 2025 beaconAI. All rights reserved.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_report_email_text(self, recipient_email: str, company_name: str, persona: str) -> str:
        """Create plain text email template for report delivery"""
        return f"""
Your AI Readiness Assessment Report - {company_name}

Dear {persona},

Thank you for completing the beaconAI AI Readiness Assessment for {company_name}. Your personalized report is now ready and attached to this email.

WHAT'S INSIDE YOUR REPORT:
• Comprehensive CARE framework analysis
• Strategic insights tailored to your organization  
• Actionable recommendations for AI implementation
• Next steps for your AI transformation journey

The attached PDF contains detailed insights based on your responses, along with strategic recommendations to accelerate your AI adoption journey.

READY TO TRANSFORM YOUR AI STRATEGY?
Our team is ready to help you implement these insights and accelerate your AI transformation.

NEXT STEPS:
Schedule a complimentary strategy session to discuss your specific AI implementation roadmap.

CONTACT BEACONAI:
📧 Email: info@beaconai.ai
📞 Phone: +1 (303) 877-4292  
🌐 Website: www.beaconai.ai
📅 Schedule Session: https://app.usemotion.com/meet/dalemyska/linkedin

© 2024 BeaconAI. All rights reserved.
        """
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Mailgun connection and configuration
        
        Returns:
            Dictionary with connection test results
        """
        try:
            # Test API connection by getting domain info
            response = requests.get(
                f"{self.base_url}/domains/{self.domain}",
                auth=("api", self.api_key),
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Mailgun connection test successful")
                return {
                    "success": True,
                    "message": "Mailgun connection successful",
                    "domain_info": response.json()
                }
            else:
                logger.error(f"Mailgun connection test failed. Status: {response.status_code}")
                return {
                    "success": False,
                    "message": f"Connection test failed: {response.text}",
                    "status_code": response.status_code
                }
                
        except Exception as e:
            logger.error(f"Mailgun connection test error: {str(e)}")
            return {
                "success": False,
                "message": f"Connection test error: {str(e)}"
            }