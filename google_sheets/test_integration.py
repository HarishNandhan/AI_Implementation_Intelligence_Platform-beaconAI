#!/usr/bin/env python3
"""
Google Sheets Integration Test Utility
Integrated version of the test script for production use
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)

def test_google_sheets_integration() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Test Google Sheets integration and return detailed results
    
    Returns:
        Tuple of (success: bool, message: str, details: dict)
    """
    results = {
        'environment_setup': False,
        'credentials_valid': False,
        'dependencies_available': False,
        'connection_successful': False,
        'sheet_accessible': False,
        'can_write_data': False,
        'can_read_data': False,
        'service_account_email': None,
        'sheet_id': None,
        'total_rows': 0,
        'errors': []
    }
    
    try:
        # Test 1: Environment Setup
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "config/google_sheets_credentials.json")
        
        if not sheet_id:
            results['errors'].append("GOOGLE_SHEETS_ID not set")
            return False, "Environment setup failed", results
        
        if not os.path.exists(credentials_file):
            results['errors'].append(f"Credentials file not found: {credentials_file}")
            return False, "Credentials file missing", results
        
        results['environment_setup'] = True
        results['sheet_id'] = sheet_id
        
        # Test 2: Credentials File
        try:
            with open(credentials_file, 'r') as f:
                creds = json.load(f)
            
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            missing_fields = [field for field in required_fields if field not in creds]
            
            if missing_fields:
                results['errors'].append(f"Missing required fields: {missing_fields}")
                return False, "Invalid credentials file", results
            
            results['credentials_valid'] = True
            results['service_account_email'] = creds['client_email']
            
        except json.JSONDecodeError as e:
            results['errors'].append(f"Invalid JSON in credentials file: {e}")
            return False, "Credentials file corrupted", results
        
        # Test 3: Dependencies
        try:
            import gspread
            from google.oauth2.service_account import Credentials
            results['dependencies_available'] = True
        except ImportError as e:
            results['errors'].append(f"Missing dependencies: {e}")
            return False, "Dependencies not available", results
        
        # Test 4: Connection
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            
            credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
            client = gspread.authorize(credentials)
            results['connection_successful'] = True
            
            # Test 5: Sheet Access
            sheet = client.open_by_key(sheet_id).sheet1
            results['sheet_accessible'] = True
            
            # Test 6: Read Data
            all_values = sheet.get_all_values()
            results['can_read_data'] = True
            results['total_rows'] = len(all_values)
            
            # Test 7: Write Data (add a test entry)
            test_row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "test@integration.com",
                "Integration Test",
                "https://test.com",
                "Test",
                "integration_test.pdf",
                "Test", "Test", "Test", "Test", "Test", "Test",
                "Test", "Test", "Test", "Test", "Test", "Test",
                "127.0.0.1",
                "Integration Test Agent",
                "Integration Test"
            ]
            
            sheet.append_row(test_row)
            results['can_write_data'] = True
            
            return True, "All tests passed successfully", results
            
        except Exception as e:
            results['errors'].append(f"Google Sheets operation failed: {str(e)}")
            return False, f"Google Sheets error: {str(e)}", results
    
    except Exception as e:
        results['errors'].append(f"Unexpected error: {str(e)}")
        return False, f"Integration test failed: {str(e)}", results

def setup_sheet_headers_if_needed() -> Tuple[bool, str]:
    """
    Setup sheet headers if they don't exist
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "config/google_sheets_credentials.json")
        
        if not sheet_id or not os.path.exists(credentials_file):
            return False, "Environment not properly configured"
        
        # Connect to Google Sheets
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id).sheet1
        
        # Check if headers exist
        headers = sheet.row_values(1)
        
        if not headers or len(headers) < 10:  # Assume we need at least 10 columns
            # Setup headers
            new_headers = [
                'Timestamp',
                'Email',
                'Company Name',
                'Company Website',
                'Persona',
                'Report Filename',
                'C1 - Leadership Confidence',
                'C2 - AI Experimentation',
                'C3 - Strategic Direction',
                'A1 - Current Usage',
                'A2 - Governance',
                'A3 - Team Proactivity',
                'R1 - Employee Comfort',
                'R2 - Training Available',
                'R3 - Decision Making',
                'E1 - Business Model',
                'E2 - Trend Monitoring',
                'E3 - Roadmap',
                'IP Address',
                'User Agent',
                'Status'
            ]
            
            # Clear and add headers
            sheet.clear()
            sheet.append_row(new_headers)
            
            return True, f"Headers setup successfully ({len(new_headers)} columns)"
        else:
            return True, f"Headers already exist ({len(headers)} columns)"
    
    except Exception as e:
        return False, f"Failed to setup headers: {str(e)}"

def get_sheets_stats() -> Dict[str, Any]:
    """
    Get statistics about the Google Sheets data
    
    Returns:
        Dictionary with sheet statistics
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "config/google_sheets_credentials.json")
        
        if not sheet_id or not os.path.exists(credentials_file):
            return {"error": "Environment not configured", "total_leads": 0}
        
        # Connect to Google Sheets
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id).sheet1
        
        # Get all data
        all_values = sheet.get_all_values()
        
        stats = {
            "total_rows": len(all_values),
            "total_leads": len(all_values) - 1 if all_values else 0,  # Subtract header row
            "headers_count": len(all_values[0]) if all_values else 0,
            "sheet_title": sheet.title,
            "last_updated": datetime.now().isoformat(),
            "service_account": None
        }
        
        # Get service account info
        try:
            with open(credentials_file, 'r') as f:
                creds = json.load(f)
                stats["service_account"] = creds.get('client_email')
        except:
            pass
        
        return stats
    
    except Exception as e:
        return {"error": str(e), "total_leads": 0}