#!/usr/bin/env python3
"""
Test script for Mailgun client
Run this to test your Mailgun configuration
"""

import os
import sys
sys.path.append('..')

from mailgun_client import MailgunClient

def test_mailgun_connection():
    """Test Mailgun connection and configuration"""
    print("🧪 Testing Mailgun Connection...")
    print("=" * 50)
    
    try:
        # Initialize client
        client = MailgunClient()
        print(f"✅ Mailgun client initialized")
        print(f"📧 Sender: {client.sender_email}")
        print(f"🌐 Domain: {client.domain}")
        print(f"🔗 Base URL: {client.base_url}")
        
        # Test connection
        print("\n🔍 Testing API connection...")
        result = client.test_connection()
        
        if result["success"]:
            print("✅ Connection test successful!")
            print(f"📊 Domain info: {result.get('domain_info', {}).get('name', 'N/A')}")
        else:
            print("❌ Connection test failed!")
            print(f"Error: {result['message']}")
            
    except Exception as e:
        print(f"❌ Error initializing Mailgun client: {str(e)}")
        print("\n🔧 Check your environment variables:")
        print("- MAILGUN_API_KEY")
        print("- MAILGUN_DOMAIN") 
        print("- MAILGUN_BASE_URL")

def test_send_simple_email():
    """Test sending a simple email"""
    print("\n📧 Testing Simple Email Send...")
    print("=" * 50)
    
    # Get recipient email from user
    recipient = input("Enter your email address for testing: ").strip()
    
    if not recipient:
        print("❌ No email address provided. Skipping email test.")
        return
    
    try:
        client = MailgunClient()
        
        # Send test email
        result = client.send_email(
            to_email=recipient,
            subject="🧪 BeaconAI Mailgun Test Email",
            html_content="""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #0A3161;">🎉 Mailgun Test Successful!</h2>
                <p>If you're reading this, your Mailgun integration is working perfectly!</p>
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #FFA500;">✅ What this means:</h3>
                    <ul>
                        <li>Your API key is valid</li>
                        <li>Your domain is configured correctly</li>
                        <li>Email delivery is working</li>
                        <li>You're ready to send report emails!</li>
                    </ul>
                </div>
                <p style="color: #666; font-size: 12px;">
                    This is a test email from your BeaconAI application.
                </p>
            </body>
            </html>
            """,
            text_content="Mailgun Test Successful! Your email integration is working."
        )
        
        if result["success"]:
            print("✅ Test email sent successfully!")
            print(f"📧 Sent to: {recipient}")
            print(f"🆔 Mailgun ID: {result.get('mailgun_id', 'N/A')}")
            print("\n📬 Check your email inbox (and spam folder) for the test email.")
        else:
            print("❌ Failed to send test email!")
            print(f"Error: {result['message']}")
            
    except Exception as e:
        print(f"❌ Error sending test email: {str(e)}")

if __name__ == "__main__":
    print("🚀 BeaconAI Mailgun Test Suite")
    print("=" * 50)
    
    # Test 1: Connection
    test_mailgun_connection()
    
    # Test 2: Email sending (optional)
    print("\n" + "=" * 50)
    send_test = input("Do you want to send a test email? (y/n): ").strip().lower()
    
    if send_test in ['y', 'yes']:
        test_send_simple_email()
    else:
        print("⏭️  Skipping email send test.")
    
    print("\n🎯 Test completed!")
    print("If all tests passed, your Mailgun integration is ready!")