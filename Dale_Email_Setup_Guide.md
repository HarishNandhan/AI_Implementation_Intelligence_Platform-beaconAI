# Dale's Email Setup Guide for BeaconAI Reports
## Complete Step-by-Step Process

### Overview
We need to set up automated email sending from `dale@beaconai.ai` for AI readiness assessment reports. This requires configuring Mailgun (email service) with your beaconai.ai domain.

---

## PHASE 1: Pre-Setup Verification (5 minutes)

### Step 1: Verify Domain Control
- [ ] Confirm you have admin access to beaconai.ai domain DNS settings
- [ ] Know your domain registrar/DNS provider (GoDaddy, Cloudflare, Namecheap, etc.)
- [ ] Can access DNS management panel

### Step 2: Email Account Setup
- [ ] Ensure `dale@beaconai.ai` email account exists and is working
- [ ] Test sending/receiving emails from this address
- [ ] If not set up, create it through your email hosting provider

---

## PHASE 2: Mailgun Account Setup (10 minutes)

### Step 3: Create/Access Mailgun Account
- [ ] Go to https://www.mailgun.com
- [ ] Sign up for new account OR log into existing account
- [ ] Choose the appropriate plan:
  - **Free tier**: 5,000 emails/month (good for testing)
  - **Flex plan**: $8/month for 50,000 emails (recommended for production)

### Step 4: Account Verification
- [ ] Verify your email address
- [ ] Complete phone verification if required
- [ ] Add payment method (even for free tier, card required for domain verification)

---

## PHASE 3: Domain Configuration (15-20 minutes)

### Step 5: Add Domain to Mailgun
1. [ ] In Mailgun dashboard, click **"Domains"** in left sidebar
2. [ ] Click **"Add New Domain"**
3. [ ] Enter: `beaconai.ai` (NOT mg.beaconai.ai or mail.beaconai.ai)
4. [ ] Select **"US"** region (unless you prefer EU)
5. [ ] Click **"Add Domain"**

### Step 6: Get DNS Records
After adding domain, Mailgun will show DNS records to add. **COPY THESE EXACTLY:**

**You'll see something like:**
```
TXT Record:
Name: beaconai.ai
Value: v=spf1 include:mailgun.org ~all

TXT Record (DKIM):
Name: k1._domainkey.beaconai.ai
Value: k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC... (long key)

CNAME Record:
Name: email.beaconai.ai
Value: mailgun.org

MX Records:
Name: beaconai.ai
Value: mxa.mailgun.org (Priority: 10)
Value: mxb.mailgun.org (Priority: 10)
```

### Step 7: Add DNS Records
**Go to your DNS provider and add each record:**

1. [ ] **SPF Record (TXT)**:
   - Type: TXT
   - Name: @ (or beaconai.ai)
   - Value: `v=spf1 include:mailgun.org ~all`

2. [ ] **DKIM Record (TXT)**:
   - Type: TXT
   - Name: `k1._domainkey` (or full: k1._domainkey.beaconai.ai)
   - Value: [Copy the long DKIM key from Mailgun]

3. [ ] **CNAME Record**:
   - Type: CNAME
   - Name: `email`
   - Value: `mailgun.org`

4. [ ] **MX Records** (Add both):
   - Type: MX
   - Name: @ (or beaconai.ai)
   - Value: `mxa.mailgun.org`
   - Priority: 10
   
   - Type: MX
   - Name: @ (or beaconai.ai)
   - Value: `mxb.mailgun.org`
   - Priority: 10

### Step 8: Wait for DNS Propagation
- [ ] DNS changes can take 15 minutes to 48 hours
- [ ] Check status in Mailgun dashboard (will show "Verified" when ready)
- [ ] You can use https://mxtoolbox.com to check DNS propagation

---

## PHASE 4: API Key Generation (5 minutes)

### Step 9: Generate API Key
1. [ ] In Mailgun dashboard, go to **"Settings"** → **"API Keys"**
2. [ ] Find **"Private API key"** section
3. [ ] Click **"Copy"** to copy the API key
4. [ ] **IMPORTANT**: This key starts with `key-` followed by random characters
5. [ ] Save this key securely - you'll share it with your intern

### Step 10: Note Domain Information
- [ ] Go back to **"Domains"** section
- [ ] Click on `beaconai.ai`
- [ ] Note the **"Domain Name"**: should be exactly `beaconai.ai`
- [ ] Ensure status shows **"Active"** and **"Verified"**

---

## PHASE 5: Testing & Handoff (10 minutes)

### Step 11: Test Email Sending
1. [ ] In Mailgun dashboard, go to **"Logs"** → **"Send Test Email"**
2. [ ] Send test email from `dale@beaconai.ai` to your personal email
3. [ ] Verify email arrives and shows correct sender

### Step 12: Provide Credentials to Intern
**Share these details with your intern:**

```
MAILGUN_API_KEY=key-[your-actual-api-key-here]
MAILGUN_DOMAIN=beaconai.ai
MAILGUN_BASE_URL=https://api.mailgun.net/v3
SENDER_EMAIL=dale@beaconai.ai
SENDER_NAME=Dale - BeaconAI
```

### Step 13: Grant Dashboard Access (Optional)
- [ ] In Mailgun, go to **"Account"** → **"Users"**
- [ ] Add your intern's email with **"Member"** role
- [ ] This allows them to monitor email delivery and troubleshoot

---

## TROUBLESHOOTING CHECKLIST

### If Domain Verification Fails:
- [ ] Double-check all DNS records are exactly as Mailgun specified
- [ ] Ensure no extra spaces or characters in DNS values
- [ ] Wait longer (DNS can take up to 48 hours)
- [ ] Use DNS checker tools to verify records are live

### If Emails Don't Send:
- [ ] Verify API key is correct and starts with `key-`
- [ ] Ensure domain status is "Active" and "Verified"
- [ ] Check Mailgun logs for error messages
- [ ] Verify sender email `dale@beaconai.ai` exists and works

### Common DNS Provider Instructions:
- **Cloudflare**: DNS → Records → Add record
- **GoDaddy**: DNS Management → Add Record
- **Namecheap**: Advanced DNS → Add New Record
- **AWS Route 53**: Hosted zones → Create record

---

## FINAL CHECKLIST

Before ending the call, verify:
- [ ] Domain shows "Verified" in Mailgun
- [ ] Test email sent successfully
- [ ] API key copied and shared
- [ ] All DNS records added correctly
- [ ] Intern has all necessary credentials

---

## POST-SETUP

After setup is complete:
1. Your intern will update the application configuration
2. They'll run tests to ensure emails send properly
3. The system will automatically send AI assessment reports from `dale@beaconai.ai`
4. You can monitor email delivery in the Mailgun dashboard

**Estimated Total Time: 45-60 minutes**

---

## CONTACT INFO

If you encounter issues during setup:
- Mailgun Support: https://help.mailgun.com
- DNS Help: Contact your domain registrar's support
- Your intern can help troubleshoot technical issues after basic setup is complete