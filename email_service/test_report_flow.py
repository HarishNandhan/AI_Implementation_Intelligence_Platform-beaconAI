#!/usr/bin/env python3
"""
Test script for integrated Report + Email flow
Run this to test the complete report generation and email sending
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
REPORT_ENDPOINTS = {
    "generate": f"{BASE_URL}/report/generate",
    "generate_and_email": f"{BASE_URL}/report/generate-and-email",
    "download": f"{BASE_URL}/report/download"
}

# Sample test data
SAMPLE_REPORT_DATA = {
    "company_name": "TechCorp Solutions",
    "company_website": "https://example.com",
    "persona": "CTO",
    "insights": {
        "C1": "Very comfortable",
        "C2": "Highly engaged",
        "A1": "Fully aligned",
        "A2": "Strong support",
        "R1": "Well prepared",
        "R2": "Adequate resources",
        "E1": "Clear roadmap",
        "E2": "Established metrics"
    }
}

def test_api_health():
    """Test if the API is running"""
    print("🏥 Testing API Health...")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is running!")
            print(f"📊 Service: {data.get('service', 'Unknown')}")
            return True
        else:
            print(f"❌ API health check failed. Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {str(e)}")
        return False

def test_report_generation_only():
    """Test report generation without email"""
    print("\n📄 Testing Report Generation (No Email)...")
    print("=" * 60)
    
    try:
        # Test data without email
        test_data = SAMPLE_REPORT_DATA.copy()
        
        print("🔄 Generating report...")
        response = requests.post(
            REPORT_ENDPOINTS["generate"],
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # Report generation can take time
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Report generated successfully!")
            print(f"📄 File path: {data.get('filepath')}")
            print(f"📧 Email sent: {data.get('email_sent', 'N/A')}")
            print(f"💬 Email status: {data.get('email_status', 'N/A')}")
            return data.get('filepath')
        else:
            print(f"❌ Report generation failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return None

def test_report_generation_with_email():
    """Test report generation with email sending"""
    print("\n📧 Testing Report Generation + Email...")
    print("=" * 60)
    
    # Get recipient email from user
    recipient = input("Enter your email address for testing: ").strip()
    
    if not recipient:
        print("❌ No email address provided. Skipping email test.")
        return None
    
    try:
        # Test data with email
        test_data = SAMPLE_REPORT_DATA.copy()
        test_data["user_email"] = recipient
        
        print("🔄 Generating report and sending email...")
        print("⏳ This may take 30-60 seconds...")
        
        response = requests.post(
            REPORT_ENDPOINTS["generate"],
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=120  # Longer timeout for email sending
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Report generated successfully!")
            print(f"📄 File path: {data.get('filepath')}")
            print(f"📧 Email sent: {data.get('email_sent')}")
            print(f"💬 Email status: {data.get('email_status')}")
            print(f"🆔 Mailgun ID: {data.get('mailgun_id', 'N/A')}")
            
            if data.get('email_sent'):
                print("\n📬 Check your email inbox (and spam folder) for the report!")
            
            return data.get('filepath')
        else:
            print(f"❌ Report generation failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return None

def test_generate_and_email_endpoint():
    """Test the dedicated generate-and-email endpoint"""
    print("\n🚀 Testing Generate-and-Email Endpoint...")
    print("=" * 60)
    
    # Get recipient email from user
    recipient = input("Enter your email address for testing: ").strip()
    
    if not recipient:
        print("❌ No email address provided. Skipping test.")
        return None
    
    try:
        # Test data with email (required for this endpoint)
        test_data = SAMPLE_REPORT_DATA.copy()
        test_data["user_email"] = recipient
        
        print("🔄 Generating report and sending email (dedicated endpoint)...")
        print("⏳ This may take 30-60 seconds...")
        
        response = requests.post(
            REPORT_ENDPOINTS["generate_and_email"],
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Report generated and emailed successfully!")
            print(f"📄 File path: {data.get('filepath')}")
            print(f"📧 Email sent: {data.get('email_sent')}")
            print(f"💬 Email status: {data.get('email_status')}")
            print(f"🆔 Mailgun ID: {data.get('mailgun_id', 'N/A')}")
            print("\n📬 Check your email inbox (and spam folder) for the report!")
            return data.get('filepath')
        else:
            print(f"❌ Generate-and-email failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return None

def test_download_report(filepath):
    """Test downloading a generated report"""
    if not filepath:
        print("❌ No filepath provided for download test.")
        return
    
    print(f"\n⬇️ Testing Report Download...")
    print("=" * 60)
    
    try:
        # Extract filename from filepath
        filename = filepath.split('/')[-1] if '/' in filepath else filepath.split('\\')[-1]
        download_url = f"{REPORT_ENDPOINTS['download']}/{filename}"
        
        print(f"🔄 Downloading: {filename}")
        response = requests.get(download_url, timeout=30)
        
        if response.status_code == 200:
            print("✅ Report download successful!")
            print(f"📄 Content type: {response.headers.get('content-type', 'Unknown')}")
            print(f"📊 File size: {len(response.content)} bytes")
            
            # Optionally save the file locally for verification
            local_filename = f"test_download_{filename}"
            with open(local_filename, 'wb') as f:
                f.write(response.content)
            print(f"💾 Saved locally as: {local_filename}")
            
        else:
            print(f"❌ Download failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Download error: {str(e)}")

def main():
    """Main test function"""
    print("🚀 BeaconAI Report + Email Integration Test Suite")
    print("=" * 60)
    
    # Test 1: API Health
    if not test_api_health():
        print("\n❌ API is not running. Please start your FastAPI server first.")
        return
    
    # Test 2: Report Generation Only
    print("\n" + "=" * 60)
    test_basic = input("Test basic report generation (no email)? (y/n): ").strip().lower()
    
    filepath = None
    if test_basic in ['y', 'yes']:
        filepath = test_report_generation_only()
    
    # Test 3: Report Generation + Email
    print("\n" + "=" * 60)
    test_email = input("Test report generation with email? (y/n): ").strip().lower()
    
    if test_email in ['y', 'yes']:
        filepath = test_report_generation_with_email()
    
    # Test 4: Generate-and-Email Endpoint
    print("\n" + "=" * 60)
    test_dedicated = input("Test dedicated generate-and-email endpoint? (y/n): ").strip().lower()
    
    if test_dedicated in ['y', 'yes']:
        filepath = test_generate_and_email_endpoint()
    
    # Test 5: Download Report
    if filepath:
        print("\n" + "=" * 60)
        test_download = input("Test report download? (y/n): ").strip().lower()
        
        if test_download in ['y', 'yes']:
            test_download_report(filepath)
    
    print("\n🎯 Integration Test completed!")
    print("If all tests passed, your report + email integration is ready!")

if __name__ == "__main__":
    main()