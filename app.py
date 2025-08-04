import streamlit as st
import requests
import os
import re
from care.question_bank import CARE_QUESTIONS

st.set_page_config(
    page_title="BeaconAI Diagnostic", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Header with branding
st.markdown("""
<div style="background: linear-gradient(90deg, #0A3161 0%, #FFA500 100%); padding: 20px; border-radius: 10px; margin-bottom: 30px;">
    <h1 style="color: white; margin: 0; text-align: center;">🤖 BeaconAI – AI Readiness Diagnostic</h1>
    <p style="color: white; margin: 10px 0 0 0; text-align: center; opacity: 0.9;">
        Discover your organization's AI implementation readiness with our comprehensive CARE assessment
    </p>
</div>
""", unsafe_allow_html=True)

# Email validation function
def validate_email(email):
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Progress indicator function
def show_progress(step, total_steps, step_name):
    """Show progress indicator"""
    progress = step / total_steps
    st.progress(progress)
    st.markdown(f"**Step {step} of {total_steps}:** {step_name}")
    st.markdown("---")

# Initialize session state for email and download
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'email_validated' not in st.session_state:
    st.session_state.email_validated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'download_data' not in st.session_state:
    st.session_state.download_data = None
if 'filename' not in st.session_state:
    st.session_state.filename = ""
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False
if 'email_status' not in st.session_state:
    st.session_state.email_status = ""
if 'mailgun_id' not in st.session_state:
    st.session_state.mailgun_id = ""

# Show progress for form filling
if not st.session_state.report_generated:
    show_progress(1, 3, "Complete Assessment")

with st.form("care_form"):
    # Company Information
    st.subheader("🧩 Company Info")
    company_name = st.text_input("Company Name")
    company_website = st.text_input("Company Website")
    persona = st.selectbox("Who are you?", ["CTO", "CHRO", "CMO", "COO", "CEO", "Other"])

    # CARE Diagnostic Questions
    st.subheader("📋 CARE Diagnostic Questions")
    answers = {}
    for qid, qdata in CARE_QUESTIONS.items():
        st.markdown(f"**{qid}: {qdata['question']}**")
        selected = st.radio("Select an option:", qdata["options"], key=qid)
        answers[qid] = selected

    submitted = st.form_submit_button("🧾 Generate Insight Report", type="primary", use_container_width=True)

# -------------------------------
# Call Backend and Generate Report
# -------------------------------
if submitted:
    # Validate required fields
    if not company_name or not company_website:
        st.error("❌ Please fill in all required fields (Company Name and Website).")
    else:
        with st.spinner("Generating your personalized PDF report..."):
            try:
                # Get backend URL from environment variable or use default
                backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                
                # First, generate report without email to prepare for email collection
                response = requests.post(
                    f"{backend_url}/report/generate",
                    json={
                        "company_name": company_name,
                        "company_website": company_website,
                        "persona": persona,
                        "insights": answers
                        # No email yet - we'll collect it next
                    },
                    timeout=120  # Longer timeout for report generation
                )

                if response.status_code == 200:
                    data = response.json()
                    filepath = data["filepath"]

                    st.success("✅ Report generated successfully!")

                    # Extract filename from filepath
                    filename = filepath.split("/")[-1] if "/" in filepath else filepath.split("\\")[-1]
                    
                    # Get the download data for backup
                    download_url = f"{backend_url}/report/download/{filename}"
                    
                    try:
                        download_response = requests.get(download_url)
                        if download_response.status_code == 200:
                            # Store data in session state
                            st.session_state.report_generated = True
                            st.session_state.download_data = download_response.content
                            st.session_state.filename = filename
                            st.session_state.email_validated = False  # Reset email validation
                            st.session_state.email_sent = False  # Reset email status
                            st.session_state.email_status = ""
                            st.session_state.mailgun_id = ""
                            
                            # Store form data for email sending
                            st.session_state.company_name = company_name
                            st.session_state.company_website = company_website
                            st.session_state.persona = persona
                            st.session_state.answers = answers
                            
                            st.info("📧 Please provide your email address to receive and download the report.")
                            
                        else:
                            st.error(f"❌ Could not prepare the PDF file. Status: {download_response.status_code}")
                            st.error(f"Error details: {download_response.text}")
                    except Exception as download_error:
                        st.error(f"❌ Report preparation failed: {download_error}")

                else:
                    st.error(f"❌ Report generation failed. Status: {response.status_code}")
                    if response.text:
                        st.error(f"Error details: {response.text}")

            except requests.exceptions.Timeout:
                st.error("❌ Report generation timed out. Please try again.")
            except Exception as e:
                st.error(f"❌ Could not connect to the backend: {e}")

# -------------------------------
# Email Collection Modal
# -------------------------------
if st.session_state.report_generated and not st.session_state.email_validated:
    show_progress(2, 3, "Provide Email Address")
    st.subheader("📧 Email Required for Download")
    
    with st.container():
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #0A3161;">
            <h4 style="color: #0A3161; margin-top: 0;">🔒 Secure Download Access</h4>
            <p style="margin-bottom: 0;">To download your personalized AI readiness report, please provide your email address. 
            This helps us:</p>
            <ul style="margin: 10px 0;">
                <li>Send you additional AI insights and resources</li>
                <li>Notify you about relevant AI implementation opportunities</li>
                <li>Provide follow-up consultation scheduling</li>
            </ul>
            <p style="margin-bottom: 0; font-size: 0.9em; color: #666;">
                <em>We respect your privacy and will never share your email with third parties.</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Email input form
        with st.form("email_form"):
            email_input = st.text_input(
                "Email Address *", 
                placeholder="your.email@company.com",
                help="Enter a valid email address to receive your report"
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col2:
                email_submitted = st.form_submit_button("🔓 Unlock Download", use_container_width=True)
        
        if email_submitted:
            if not email_input:
                st.error("❌ Please enter your email address.")
            elif not validate_email(email_input):
                st.error("❌ Please enter a valid email address (e.g., name@company.com)")
            else:
                # Email is valid, now send the report via email
                with st.spinner("📧 Sending report to your email..."):
                    try:
                        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                        
                        # Send email using the generate-and-email endpoint
                        email_response = requests.post(
                            f"{backend_url}/report/generate-and-email",
                            json={
                                "company_name": st.session_state.company_name,
                                "company_website": st.session_state.company_website,
                                "persona": st.session_state.persona,
                                "insights": st.session_state.answers,
                                "user_email": email_input
                            },
                            timeout=120
                        )
                        
                        if email_response.status_code == 200:
                            email_data = email_response.json()
                            
                            # Update session state with email results
                            st.session_state.user_email = email_input
                            st.session_state.email_validated = True
                            st.session_state.email_sent = email_data.get("email_sent", False)
                            st.session_state.email_status = email_data.get("email_status", "")
                            st.session_state.mailgun_id = email_data.get("mailgun_id", "")
                            
                            st.success("✅ Email sent successfully!")
                            st.rerun()
                            
                        else:
                            st.error(f"❌ Failed to send email. Status: {email_response.status_code}")
                            st.error(f"Details: {email_response.text}")
                            
                            # Still allow download even if email fails
                            st.session_state.user_email = email_input
                            st.session_state.email_validated = True
                            st.session_state.email_sent = False
                            st.session_state.email_status = "Email sending failed, but download is available"
                            
                            st.warning("⚠️ Email sending failed, but you can still download the report below.")
                            st.rerun()
                            
                    except requests.exceptions.Timeout:
                        st.error("❌ Email sending timed out. You can still download the report below.")
                        st.session_state.user_email = email_input
                        st.session_state.email_validated = True
                        st.session_state.email_sent = False
                        st.session_state.email_status = "Email timeout, download available"
                        st.rerun()
                        
                    except Exception as email_error:
                        st.error(f"❌ Email sending error: {str(email_error)}")
                        st.session_state.user_email = email_input
                        st.session_state.email_validated = True
                        st.session_state.email_sent = False
                        st.session_state.email_status = f"Email error: {str(email_error)}"
                        st.rerun()

# -------------------------------
# Show Download Button After Email Validation
# -------------------------------
if st.session_state.report_generated and st.session_state.email_validated:
    show_progress(3, 3, "Download Your Report")
    st.subheader("📥 Your AI Readiness Report")
    
    # Email Status Display
    if st.session_state.email_sent:
        # Email sent successfully
        st.markdown(f"""
        <div style="background-color: #f0fff0; padding: 20px; border-radius: 8px; border-left: 5px solid #28a745;">
            <h4 style="color: #28a745; margin-top: 0;">📧 Email Sent Successfully!</h4>
            <p style="margin-bottom: 10px;">Your AI readiness report has been sent to <strong>{st.session_state.user_email}</strong></p>
            <p style="margin-bottom: 0; font-size: 0.9em; color: #666;">
                📬 Check your inbox (and spam folder) for the email from Harish - BeaconAI Team
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.mailgun_id:
            st.markdown(f"<p style='font-size: 0.8em; color: #888; margin-top: 10px;'>📧 Email ID: {st.session_state.mailgun_id}</p>", unsafe_allow_html=True)
    else:
        # Email failed but download available
        st.markdown(f"""
        <div style="background-color: #fff3cd; padding: 20px; border-radius: 8px; border-left: 5px solid #ffc107;">
            <h4 style="color: #856404; margin-top: 0;">⚠️ Email Delivery Issue</h4>
            <p style="margin-bottom: 10px;">We couldn't send the email to <strong>{st.session_state.user_email}</strong></p>
            <p style="margin-bottom: 0; font-size: 0.9em; color: #666;">
                Don't worry! You can still download your report below.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Download Section
    st.markdown("### 📥 Download Options")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**💻 Web Download**")
        st.download_button(
            label="📥 Download PDF Report",
            data=st.session_state.download_data,
            file_name=st.session_state.filename,
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
        st.markdown("<small>Download directly to your device</small>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**📧 Email Copy**")
        if st.session_state.email_sent:
            st.markdown("""
            <div style="padding: 10px; background-color: #e8f5e8; border-radius: 5px; text-align: center;">
                <span style="color: #28a745;">✅ Sent to your email</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button("🔄 Retry Email Send", use_container_width=True):
                # Retry email sending
                with st.spinner("📧 Retrying email send..."):
                    try:
                        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                        
                        email_response = requests.post(
                            f"{backend_url}/report/generate-and-email",
                            json={
                                "company_name": st.session_state.company_name,
                                "company_website": st.session_state.company_website,
                                "persona": st.session_state.persona,
                                "insights": st.session_state.answers,
                                "user_email": st.session_state.user_email
                            },
                            timeout=60
                        )
                        
                        if email_response.status_code == 200:
                            email_data = email_response.json()
                            st.session_state.email_sent = True
                            st.session_state.email_status = email_data.get("email_status", "")
                            st.session_state.mailgun_id = email_data.get("mailgun_id", "")
                            st.success("✅ Email sent successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Email retry failed. Please use the download button above.")
                    except Exception as e:
                        st.error(f"❌ Email retry error: {str(e)}")
        
        st.markdown("<small>Get a copy in your inbox</small>", unsafe_allow_html=True)
    
    # Report Information
    st.markdown("---")
    st.markdown("### 📊 Report Details")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric("Company", st.session_state.company_name)
    with col2:
        st.metric("Role", st.session_state.persona)
    with col3:
        st.metric("File Size", f"{len(st.session_state.download_data) // 1024} KB")
    
    # Call-to-action for next steps
    st.markdown("---")
    st.markdown("### 🚀 What's Next?")
    
    # Enhanced CTA with buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        **📅 Schedule Consultation**
        
        Ready to discuss your AI strategy?
        """)
        st.link_button(
            "Book Strategy Session",
            "https://app.usemotion.com/meet/dalemyska/linkedin",
            use_container_width=True
        )
    
    with col2:
        st.markdown("""
        **🌐 Learn More**
        
        Explore our AI solutions and resources.
        """)
        st.link_button(
            "Visit BeaconAI.ai",
            "https://www.beaconai.ai",
            use_container_width=True
        )
    
    with col3:
        st.markdown("""
        **📞 Contact Us**
        
        Have questions? Get in touch!
        """)
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <p style="margin: 5px 0;"><strong>📧</strong> info@beaconai.ai</p>
            <p style="margin: 5px 0;"><strong>📞</strong> +1 (303) 877-4292</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Reset button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Generate Another Report", type="secondary", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                if key.startswith(('report_', 'email_', 'user_', 'download_', 'filename', 'company_', 'persona', 'answers', 'mailgun_')):
                    del st.session_state[key]
            st.rerun()
