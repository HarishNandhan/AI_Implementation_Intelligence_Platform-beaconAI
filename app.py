import streamlit as st
import requests
import os
from care.question_bank import CARE_QUESTIONS

st.set_page_config(page_title="BeaconAI Diagnostic", page_icon="🤖")
st.title("🤖 BeaconAI – AI Readiness Diagnostic")

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

    submitted = st.form_submit_button("🧾 Generate Insight Report")

# -------------------------------
# Call Backend and Show Download
# -------------------------------
if submitted:
    with st.spinner("Generating your personalized PDF report..."):
        try:
            response = requests.post(
                "https://ai-implementation-intelligence-platform.onrender.com/report/generate",
                json={
                    "company_name": company_name,
                    "persona": persona,
                    "insights": answers
                }
            )

            if response.status_code == 200:
                data = response.json()
                filepath = data["filepath"]

                st.success("✅ Report generated successfully!")

                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        pdf_bytes = f.read()
                    st.download_button(
                        label="📥 Download Report (PDF)",
                        data=pdf_bytes,
                        file_name=filepath.split("/")[-1],
                        mime="application/pdf"
                    )
                else:
                    st.error("PDF file not found on server.")

            else:
                st.error("❌ Report generation failed from the backend.")

        except Exception as e:
            st.error(f"❌ Could not connect to the backend: {e}")
