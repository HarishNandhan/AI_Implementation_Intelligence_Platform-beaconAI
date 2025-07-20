import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
from dotenv import load_dotenv

load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "insights@beaconai.com")

def send_email_with_attachment(to_email: str, filepath: str):
    if not SENDGRID_API_KEY:
        raise ValueError("Missing SendGrid API key.")

    with open(filepath, "rb") as f:
        data = f.read()
        encoded_file = base64.b64encode(data).decode()

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject="Your AI Readiness Report – BeaconAI",
        html_content="""
            <p>Hello,</p>
            <p>Attached is your personalized AI Readiness Report from BeaconAI.</p>
            <p>Thank you for using our platform!</p>
        """
    )

    attachment = Attachment()
    attachment.file_content = FileContent(encoded_file)
    attachment.file_type = FileType("application/pdf")
    attachment.file_name = FileName(os.path.basename(filepath))
    attachment.disposition = Disposition("attachment")
    message.attachment = attachment

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)
