#!/usr/bin/env python3
"""
Test script for Email API endpoints
Run this to test your FastAPI email endpoints
"""

import requests
import json
import os

# Configuration
BASE_URL = "http://localhost:8000"  # Change this if your API runs on different port
EMAIL_ENDPOINTS = {
    "test_connection": f"{BASE_URL}/email/test-connection",
    "send_test": f"{BASE_URL}/email/send-test", 
    "send_report": f"{BASE_URL}/email/send-report"
}

def test_api_health():
    """Test if the API is running"""
    print("🏥 Testing API Health...")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is running!")
            print(f"📊 Service: {data.get('service', 'Unknown')}")
            print(f"🔢 Version: {data.get('version', 'Unknown')}")
            print(f"🌍 Environment: {data.get('environment', 'Unknown')}")
            return True
        else:
            print(f"❌ API health check failed. Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {str(e)}")
        print("💡 Make sure your FastAPI server is running on http://localhost:8000")
        return False

def test_email_connection():
    """Test Mailgun connection via API"""
    print("\n🔌 Testing Email Connection...")
    print("=" * 50)
    
    try:
        response = requests.post(EMAIL_ENDPOINTS["test_connection"], timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("connection_test"):
                print("✅ Email connection test successful!")
                print(f"📧 Status: {data.get('status')}")
                print(f"💬 Message: {data.get('message')}")
                return True
            else:
                print("❌ Email connection test failed!")
                print(f"💬 Message: {data.get('message')}")
                return False
        else:
            print(f"❌ API request failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return False

def test_send_email():
    """Test sending a test email via API"""
    print("\n📧 Testing Email Sending...")
    print("=" * 50)
    
    # Get recipient email from user
    recipient = input("Enter your email address for testing: ").strip()
    
    if not recipient:
        print("❌ No email address provided. Skipping email test.")
        return False
    
    try:
        payload = {
            "email_address": recipient
        }
        
        response = requests.post(
            EMAIL_ENDPOINTS["send_test"], 
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Test email sent successfully!")
            print(f"📧 Sent to: {recipient}")
            print(f"💬 Message: {data.get('message')}")
            print(f"🆔 Mailgun ID: {data.get('mailgun_id', 'N/A')}")
            print("\n📬 Check your email inbox (and spam folder) for the test email.")
            return True
        else:
            print(f"❌ Failed to send test email. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return False

def test_report_email():
    """Test sending a report email (requires PDF file)"""
    print("\n📄 Testing Report Email...")
    print("=" * 50)
    
    # Check if there's a sample PDF file
    sample_pdf_path = "../generated_reports"
    pdf_files = []
    
    if os.path.exists(sample_pdf_path):
        pdf_files = [f for f in os.listdir(sample_pdf_path) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found in generated_reports folder.")
        print("💡 Generate a report first using the main application, then run this test.")
        return False
    
    # Use the first PDF file found
    pdf_file = pdf_files[0]
    pdf_path = os.path.join(sample_pdf_path, pdf_file)
    
    print(f"📄 Found PDF file: {pdf_file}")
    
    # Get recipient email
    recipient = input("Enter your email address for report testing: ").strip()
    
    if not recipient:
        print("❌ No email address provided. Skipping report test.")
        return False
    
    try:
        payload = {
            "email_address": recipient,
            "company_name": "Test Company",
            "persona": "CTO",
            "filepath": pdf_path
        }
        
        response = requests.post(
            EMAIL_ENDPOINTS["send_report"],
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Report email sent successfully!")
            print(f"📧 Sent to: {recipient}")
            print(f"💬 Message: {data.get('message')}")
            print(f"🆔 Mailgun ID: {data.get('mailgun_id', 'N/A')}")
            print("\n📬 Check your email for the report with PDF attachment.")
            return True
        else:
            print(f"❌ Failed to send report email. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 BeaconAI Email API Test Suite")
    print("=" * 50)
    
    # Test 1: API Health
    if not test_api_health():
        print("\n❌ API is not running. Please start your FastAPI server first.")
        return
    
    # Test 2: Email Connection
    if not test_email_connection():
        print("\n❌ Email connection failed. Check your Mailgun configuration.")
        return
    
    # Test 3: Send Test Email
    print("\n" + "=" * 50)
    send_test = input("Do you want to send a test email? (y/n): ").strip().lower()
    
    if send_test in ['y', 'yes']:
        test_send_email()
    
    # Test 4: Send Report Email
    print("\n" + "=" * 50)
    send_report = input("Do you want to test report email sending? (y/n): ").strip().lower()
    
    if send_report in ['y', 'yes']:
        test_report_email()
    
    print("\n🎯 API Test completed!")
    print("If all tests passed, your email API integration is ready!")

if __name__ == "__main__":
    main()