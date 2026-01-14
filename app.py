# Importing Libraries

import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import io

# Page Config
st.set_page_config(
    page_title="AI Resume ATS Analyzer",
    layout="wide"
)

# Load Gemini API Key
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Gemini API key not found. Please add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# Read PDF
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Prompt Builder 

def build_prompt(job_desc, resume_text):
    return f"""
You are an ATS and hiring manager.

Compare the following job description with the candidate's resume.

Return the output in the following format:

1. ATS Match Score (0–100)
2. Matching Skills
3. Missing Skills
4. Keyword Gaps
5. Section-wise Feedback (Experience, Skills, Projects, Education)
6. Final Resume Improvement Recommendations

Job Description:
{job_desc}

Resume:
{resume_text}
"""

# UI
st.title("AI Resume ATS Score Analyzer")
st.subheader("Paste Job Description and Upload Resume to get ATS Score")

col1, col2 = st.columns(2)

with col1:
    job_desc = st.text_area("Paste Job Description", height=300)

with col2:
    resume_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

# Run Analysis
if st.button("Analyze Resume"):

    if not job_desc or not resume_file:
        st.warning("Please upload resume and paste job description.")
        st.stop()

    with st.spinner("Reading resume..."):
        resume_text = extract_text_from_pdf(resume_file)

    with st.spinner("Analyzing with Gemini AI..."):
        prompt = build_prompt(job_desc, resume_text)
        response = model.generate_content(prompt)

    # Display Results
    st.success("Analysis Complete")

    st.markdown("##ATS Analysis")
    st.write(response.text)