import os
import json
from datetime import datetime
from typing import Dict, Any, List
import logging

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

logger = logging.getLogger(__name__)

class GoogleSheetsClient:
    """Google Sheets client using service account credentials"""
    
    def __init__(self):
        self.sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        self.credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "config/google_sheets_credentials.json")
        
        # Debug logging
        logger.info(f"Google Sheets initialization:")
        logger.info(f"  Sheet ID: {self.sheet_id}")
        logger.info(f"  Credentials file: {self.credentials_file}")
        logger.info(f"  GSPREAD available: {GSPREAD_AVAILABLE}")
        
        if not GSPREAD_AVAILABLE:
            logger.warning("gspread not installed. Install with: pip install gspread google-auth")
            self.enabled = False
            return
        
        if not self.sheet_id or not self.credentials_file:
            logger.warning("Google Sheets ID or credentials file not configured")
            self.enabled = False
            return
        
        # Handle Docker environment paths
        if os.getenv("DOCKER_ENV") and not os.path.isabs(self.credentials_file):
            self.credentials_file = os.path.join("/app", self.credentials_file)
            logger.info(f"  Docker path adjusted to: {self.credentials_file}")
        
        if not os.path.exists(self.credentials_file):
            logger.warning(f"Google Sheets credentials file not found: {self.credentials_file}")
            # List directory contents for debugging
            cred_dir = os.path.dirname(self.credentials_file)
            if os.path.exists(cred_dir):
                files = os.listdir(cred_dir)
                logger.warning(f"Files in {cred_dir}: {files}")
            else:
                logger.warning(f"Directory {cred_dir} does not exist")
            self.enabled = False
            return
        
        try:
            # Setup credentials and client
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            
            credentials = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=scopes
            )
            
            self.client = gspread.authorize(credentials)
            self.sheet = self.client.open_by_key(self.sheet_id).sheet1
            
            self.enabled = True
            logger.info("Google Sheets client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets client: {str(e)}")
            self.enabled = False
    
    def add_lead(self, lead_data: Dict[str, Any]) -> bool:
        """Add lead information to Google Sheets"""
        if not self.enabled:
            logger.warning("Google Sheets not enabled, skipping lead storage")
            return False
        
        try:
            # Prepare row data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create row with lead information
            row_values = [
                timestamp,
                lead_data.get('email', ''),
                lead_data.get('company_name', ''),
                lead_data.get('company_website', ''),
                lead_data.get('persona', ''),
                lead_data.get('report_filename', ''),
                # Add CARE answers
                lead_data.get('insights', {}).get('C1', ''),
                lead_data.get('insights', {}).get('C2', ''),
                lead_data.get('insights', {}).get('C3', ''),
                lead_data.get('insights', {}).get('A1', ''),
                lead_data.get('insights', {}).get('A2', ''),
                lead_data.get('insights', {}).get('A3', ''),
                lead_data.get('insights', {}).get('R1', ''),
                lead_data.get('insights', {}).get('R2', ''),
                lead_data.get('insights', {}).get('R3', ''),
                lead_data.get('insights', {}).get('E1', ''),
                lead_data.get('insights', {}).get('E2', ''),
                lead_data.get('insights', {}).get('E3', ''),
                lead_data.get('ip_address', ''),
                lead_data.get('user_agent', ''),
                'Report Generated'  # Status
            ]
            
            # Add row to Google Sheets
            self.sheet.append_row(row_values)
            
            logger.info(f"Lead added to Google Sheets: {lead_data.get('email')}")
            return True
                
        except Exception as e:
            logger.error(f"Error adding lead to Google Sheets: {str(e)}")
            return False
    
    def setup_sheet_headers(self) -> bool:
        """Setup headers in the Google Sheet (run once)"""
        if not self.enabled:
            return False
        
        try:
            headers = [
                'Timestamp',
                'Email',
                'Company Name',
                'Company Website',
                'Persona',
                'Report Filename',
                'C1 - Current State',
                'C2 - Data Infrastructure',
                'C3 - Technology Stack',
                'A1 - Team Readiness',
                'A2 - Skills Assessment',
                'A3 - Change Management',
                'R1 - Risk Assessment',
                'R2 - Compliance',
                'R3 - Security',
                'E1 - Leadership Support',
                'E2 - Budget Allocation',
                'E3 - Strategic Alignment',
                'IP Address',
                'User Agent',
                'Status'
            ]
            
            # Clear existing content and add headers
            self.sheet.clear()
            self.sheet.append_row(headers)
            
            logger.info("Google Sheets headers setup successfully")
            return True
                
        except Exception as e:
            logger.error(f"Error setting up sheet headers: {str(e)}")
            return False
    
    def get_leads_count(self) -> int:
        """Get total number of leads in sheet"""
        if not self.enabled:
            return 0
        
        try:
            all_values = self.sheet.get_all_values()
            return len(all_values) - 1 if all_values else 0  # Subtract header row
        except Exception as e:
            logger.error(f"Error getting leads count: {str(e)}")
            return 0

# Global instance
sheets_client = GoogleSheetsClient()