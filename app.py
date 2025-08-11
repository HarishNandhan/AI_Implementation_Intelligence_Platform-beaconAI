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
                
                # Store form data for email collection step
                st.session_state.company_name = company_name
                st.session_state.company_website = company_website
                st.session_state.persona = persona
                st.session_state.answers = answers
                st.session_state.report_generated = True
                st.session_state.email_validated = False
                
                st.success("✅ Assessment completed! Please provide your email to generate and receive your report.")
                st.rerun()



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
            <h4 style="color: #0A3161; margin-top: 0;">📥 Download Your Report</h4>
            <p style="margin-bottom: 0;">To download your personalized AI readiness report, please provide your email address. 
            This helps us:</p>
            <ul style="margin: 10px 0;">
                <li>Track report downloads for analytics</li>
                <li>Send you additional AI insights and resources (optional)</li>
                <li>Provide follow-up consultation opportunities</li>
            </ul>
            <p style="margin-bottom: 0; font-size: 0.9em; color: #666;">
                <em>Your report will be available for immediate download. Email delivery coming soon!</em>
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
                email_submitted = st.form_submit_button("📥 Generate & Download Report", use_container_width=True)
        
        if email_submitted:
            if not email_input:
                st.error("❌ Please enter your email address.")
            elif not validate_email(email_input):
                st.error("❌ Please enter a valid email address (e.g., name@company.com)")
            else:
                # Email is valid, now generate report for download
                with st.spinner("📄 Generating your personalized AI readiness report..."):
                    try:
                        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                        
                        # Generate report with email (now required)
                        email_response = requests.post(
                            f"{backend_url}/report/generate",
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
                            
                            # Get PDF content from response (base64 encoded)
                            import base64
                            pdf_content_b64 = email_data.get("pdf_content", "")
                            filename = email_data.get("filename", "report.pdf")
                            
                            if pdf_content_b64:
                                try:
                                    # Decode base64 PDF content
                                    pdf_content = base64.b64decode(pdf_content_b64)
                                    
                                    # Update session state with results
                                    st.session_state.user_email = email_input
                                    st.session_state.email_validated = True
                                    st.session_state.email_sent = email_data.get("email_sent", False)
                                    st.session_state.email_status = email_data.get("email_status", "")
                                    st.session_state.mailgun_id = email_data.get("mailgun_id", "")
                                    st.session_state.download_data = pdf_content
                                    st.session_state.filename = filename
                                    
                                    # Show appropriate success message based on email status
                                    if email_data.get("email_sent", False):
                                        st.success("✅ Report generated and emailed successfully! Check your inbox and download below.")
                                    else:
                                        st.success("✅ Report generated successfully! Ready for download.")
                                    st.rerun()
                                except Exception as decode_error:
                                    st.error(f"❌ Failed to decode PDF content: {decode_error}")
                            else:
                                st.error("❌ No PDF content in response")
                            
                        else:
                            st.error(f"❌ Failed to send email. Status: {email_response.status_code}")
                            st.error(f"Details: {email_response.text}")
                            
                            # Try to get PDF content even if email fails
                            try:
                                # Check if response is JSON
                                if email_response.headers.get('content-type', '').startswith('application/json'):
                                    email_data = email_response.json()
                                    pdf_content_b64 = email_data.get("pdf_content", "")
                                    filename = email_data.get("filename", "report.pdf")
                                    
                                    if pdf_content_b64:
                                        import base64
                                        pdf_content = base64.b64decode(pdf_content_b64)
                                        
                                        st.session_state.user_email = email_input
                                        st.session_state.email_validated = True
                                        st.session_state.email_sent = False
                                        st.session_state.email_status = "Email sending failed, but download is available"
                                        st.session_state.download_data = pdf_content
                                        st.session_state.filename = filename
                                        
                                        st.warning("⚠️ Email sending failed, but you can still download the report below.")
                                        st.rerun()
                                    else:
                                        st.error("❌ No PDF content in response")
                                else:
                                    st.error("❌ Server returned non-JSON response")
                                    st.error(f"Response content: {email_response.text[:200]}...")
                            except Exception as fallback_error:
                                st.error(f"❌ Fallback download failed: {fallback_error}")
                                st.error("Please try again or contact support if the issue persists.")
                            
                    except requests.exceptions.Timeout:
                        st.error("❌ Report generation timed out. Please try again.")
                        
                    except Exception as email_error:
                        st.error(f"❌ Report generation error: {str(email_error)}")
                        st.error("Please check if the backend service is running and try again.")

# -------------------------------
# Show Download Button After Email Validation
# -------------------------------
if st.session_state.report_generated and st.session_state.email_validated:
    show_progress(3, 3, "Download Your Report")
    st.subheader("📥 Your AI Readiness Report")
    
    # Download Status Display with Email Status
    email_sent = st.session_state.get('email_sent', False)
    email_status = st.session_state.get('email_status', '')
    
    if email_sent:
        status_color = "#28a745"
        status_bg = "#f0fff0"
        status_icon = "📧"
        status_title = "Report Ready & Emailed!"
        status_message = f"Your personalized AI readiness report has been generated and sent to <strong>{st.session_state.user_email}</strong>"
    else:
        status_color = "#ffc107"
        status_bg = "#fff3cd"
        status_icon = "📄"
        status_title = "Report Ready!"
        status_message = f"Your personalized AI readiness report has been generated for <strong>{st.session_state.user_email}</strong>"
    
    st.markdown(f"""
    <div style="background-color: {status_bg}; padding: 20px; border-radius: 8px; border-left: 5px solid {status_color};">
        <h4 style="color: {status_color}; margin-top: 0;">{status_icon} {status_title}</h4>
        <p style="margin-bottom: 10px;">{status_message}</p>
        <p style="margin-bottom: 0; font-size: 0.9em; color: #666;">
            📥 Click the download button below to save your report
        </p>
        {f'<p style="margin-top: 10px; font-size: 0.8em; color: #666;"><em>Email Status: {email_status}</em></p>' if email_status else ''}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Download Section
    st.markdown("### 📥 Download Your Report")
    
    # Centered Download Button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.download_data is not None:
            st.download_button(
                label="📥 Download Your AI Readiness Report",
                data=st.session_state.download_data,
                file_name=st.session_state.filename,
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
            st.markdown("<p style='text-align: center; font-size: 0.9em; color: #666; margin-top: 10px;'>Click to save PDF to your device</p>", unsafe_allow_html=True)
        else:
            st.error("❌ Download data not available. Please try generating the report again.")
    
    
    # Email delivery status
    st.markdown("---")
    
    # Display email status based on backend response
    if st.session_state.get('email_sent', False):
        # Email was sent successfully
        st.markdown("""
        <div style="background-color: #d4edda; padding: 15px; border-radius: 8px; text-align: center; border-left: 5px solid #28a745;">
            <p style="margin: 0; font-size: 0.9em; color: #155724;">
                📧 <strong>Email sent successfully!</strong><br>
                Your AI readiness report has been delivered to <strong>{}</strong><br>
                Please check your inbox (and spam folder if needed).
            </p>
        </div>
        """.format(st.session_state.user_email), unsafe_allow_html=True)
    elif st.session_state.get('email_status', '').startswith('Email sending failed') or st.session_state.get('email_status', '').startswith('Email configuration error'):
        # Email failed but download is available
        st.markdown("""
        <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; text-align: center; border-left: 5px solid #ffc107;">
            <p style="margin: 0; font-size: 0.9em; color: #856404;">
                ⚠️ <strong>Email delivery failed</strong><br>
                We couldn't send the report to <strong>{}</strong>, but you can download it above.<br>
                <small>Status: {}</small>
            </p>
        </div>
        """.format(st.session_state.user_email, st.session_state.get('email_status', 'Unknown error')), unsafe_allow_html=True)
    else:
        # Default message for email capture
        st.markdown("""
        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 8px; text-align: center;">
            <p style="margin: 0; font-size: 0.9em; color: #0A3161;">
                📧 <strong>Email captured!</strong><br>
                We've saved your email (<strong>{}</strong>) for future AI insights and consultation opportunities.<br>
                Your report is ready for download above.
            </p>
        </div>
        """.format(st.session_state.user_email), unsafe_allow_html=True)
    
    # Report Information
    st.markdown("---")
    st.markdown("### 📊 Report Details")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric("Company", st.session_state.company_name)
    with col2:
        st.metric("Role", st.session_state.persona)
    with col3:
        if st.session_state.download_data is not None:
            st.metric("File Size", f"{len(st.session_state.download_data) // 1024} KB")
        else:
            st.metric("File Size", "N/A")
    
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
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("🔄 Generate Another Report", type="secondary", use_container_width=True):
                # Clear session state
                for key in list(st.session_state.keys()):
                    if key.startswith(('report_', 'email_', 'user_', 'download_', 'filename', 'company_', 'persona', 'answers', 'mailgun_')):
                        del st.session_state[key]
                st.rerun()
        
        with col_b:
            if st.button("🧪 Test Email System", type="secondary", use_container_width=True):
                with st.spinner("Testing email configuration..."):
                    try:
                        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                        test_response = requests.post(f"{backend_url}/report/test-email", timeout=10)
                        
                        if test_response.status_code == 200:
                            test_data = test_response.json()
                            if test_data["status"] == "success":
                                st.success(f"✅ Email system working: {test_data['message']}")
                            else:
                                st.error(f"❌ Email system issue: {test_data['message']}")
                        else:
                            st.error(f"❌ Test failed: {test_response.text}")
                    except Exception as e:
                        st.error(f"❌ Test error: {str(e)}")
