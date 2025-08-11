#!/usr/bin/env python3
"""
Quick script to check Mailgun API key and find the correct one
"""

import os
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv('deployment/.env')

def test_api_key(api_key, description):
    """Test an API key against both US and EU regions"""
    print(f"\n=== Testing {description} ===")
    print(f"API Key: {api_key[:10]}...")
    
    regions = [
        ("US", "https://api.mailgun.net/v3"),
        ("EU", "https://api.eu.mailgun.net/v3")
    ]
    
    for region_name, base_url in regions:
        try:
            response = requests.get(
                f"{base_url}/domains",
                auth=("api", api_key),
                timeout=10
            )
            
            if response.status_code == 200:
                domains_data = response.json()
                domains = [d['name'] for d in domains_data.get('items', [])]
                print(f"✅ {region_name} region works!")
                print(f"   Available domains: {domains}")
                
                # Check if beaconai.ai is in the list
                if 'beaconai.ai' in domains:
                    print(f"   ✅ beaconai.ai domain found!")
                    return True, region_name, base_url
                else:
                    print(f"   ⚠️  beaconai.ai not found in this region")
            else:
                print(f"❌ {region_name} region failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {region_name} region error: {str(e)}")
    
    return False, None, None

def main():
    print("🔍 Mailgun API Key Checker")
    print("=" * 50)
    
    # Get current API key from environment
    current_key = os.getenv("MAILGUN_API_KEY")
    
    if current_key:
        success, region, base_url = test_api_key(current_key, "Current API Key from .env")
        
        if success:
            print(f"\n✅ SUCCESS! Your current API key works!")
            print(f"   Region: {region}")
            print(f"   Base URL: {base_url}")
            print(f"   Domain: beaconai.ai is available")
        else:
            print(f"\n❌ Current API key doesn't work or beaconai.ai domain not found")
            print("\n💡 Try these steps:")
            print("   1. Go to Mailgun dashboard")
            print("   2. Click 'Sending' → Select 'beaconai.ai' domain")
            print("   3. Look for 'Domain Settings' or 'API Keys'")
            print("   4. Copy the 'Private API key' for beaconai.ai domain")
    else:
        print("❌ No MAILGUN_API_KEY found in environment")
    
    # Allow manual testing of different keys
    print(f"\n" + "=" * 50)
    print("🧪 Manual API Key Testing")
    
    while True:
        test_key = input("\nEnter API key to test (or 'quit' to exit): ").strip()
        
        if test_key.lower() in ['quit', 'exit', 'q']:
            break
            
        if test_key:
            success, region, base_url = test_api_key(test_key, "Manual Test Key")
            
            if success:
                print(f"\n🎉 This API key works! Update your .env file:")
                print(f"   MAILGUN_API_KEY={test_key}")
                print(f"   MAILGUN_BASE_URL={base_url}")
                print(f"   MAILGUN_DOMAIN=beaconai.ai")
                break

if __name__ == "__main__":
    main()