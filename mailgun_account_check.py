#!/usr/bin/env python3
"""
Mailgun Account Status Checker
"""

import requests

def check_account_with_key(api_key):
    """Check account status with a given API key"""
    print(f"Testing API key: {api_key[:10]}...")
    
    # Test both regions
    regions = [
        ("US", "https://api.mailgun.net/v3"),
        ("EU", "https://api.eu.mailgun.net/v3")
    ]
    
    for region_name, base_url in regions:
        print(f"\n🌍 Testing {region_name} region...")
        
        try:
            # Test 1: Get account info
            response = requests.get(
                f"{base_url}/domains",
                auth=("api", api_key),
                timeout=10
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {region_name} region works!")
                
                domains = data.get('items', [])
                print(f"Total domains: {len(domains)}")
                
                for domain in domains:
                    name = domain.get('name', 'Unknown')
                    state = domain.get('state', 'Unknown')
                    created = domain.get('created_at', 'Unknown')
                    print(f"  - {name}: {state} (created: {created})")
                
                return True, region_name, base_url
                
            elif response.status_code == 401:
                print(f"❌ {region_name}: Invalid API key")
                print(f"Response: {response.text}")
            elif response.status_code == 402:
                print(f"❌ {region_name}: Payment required - account may be suspended")
                print(f"Response: {response.text}")
            elif response.status_code == 403:
                print(f"❌ {region_name}: Forbidden - account may be restricted")
                print(f"Response: {response.text}")
            else:
                print(f"❌ {region_name}: Unexpected error {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ {region_name}: Connection error - {str(e)}")
    
    return False, None, None

def main():
    print("🔍 Mailgun Account Status Checker")
    print("=" * 50)
    
    print("This will help diagnose your Mailgun account and API key issues.")
    print("\nPlease try these steps:")
    print("1. Go to Mailgun dashboard")
    print("2. Navigate to: Sending → Domains → beaconai.ai")
    print("3. Look for 'Settings' or 'API Keys' tab")
    print("4. Generate a NEW API key (don't use the old one)")
    print("5. Copy the complete new key and test it here")
    
    while True:
        print("\n" + "=" * 50)
        api_key = input("Enter your NEW API key (or 'quit' to exit): ").strip()
        
        if api_key.lower() in ['quit', 'exit', 'q']:
            break
        
        if not api_key:
            print("❌ Please enter an API key")
            continue
        
        success, region, base_url = check_account_with_key(api_key)
        
        if success:
            print(f"\n🎉 SUCCESS! Your API key works!")
            print(f"Region: {region}")
            print(f"Base URL: {base_url}")
            print("\n📝 Update your .env file with:")
            print(f"MAILGUN_API_KEY={api_key}")
            print(f"MAILGUN_BASE_URL={base_url}")
            print(f"MAILGUN_DOMAIN=beaconai.ai")
            break
        else:
            print(f"\n❌ This API key doesn't work either.")
            print("\n💡 Troubleshooting suggestions:")
            print("1. Make sure you're copying the 'Private API key' (not public)")
            print("2. Check if your Mailgun account is verified and active")
            print("3. Verify your payment method is valid")
            print("4. Contact Mailgun support if the issue persists")
            
            retry = input("\nTry another key? (y/n): ").strip().lower()
            if retry != 'y':
                break

if __name__ == "__main__":
    main()