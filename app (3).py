import os
import streamlit as st
import PyPDF2
import google.generativeai as genai

# Securely set your Google Gemini API Key
GEMINI_API_KEY ="AIzaSyAYr3lCAy_EuaYpN9SmtVY9O_jlCSwBMfQ"  # Recommended way
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit Page Setup
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 34px;
        font-weight: bold;
        color: #0077b6;
        text-shadow: 1px 1px 3px rgba(0, 119, 182, 0.3);
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #ccc;
        margin-bottom: 20px;
    }
    .stButton button {
        background: linear-gradient(to right, #0077b6, #023e8a);
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(to right, #023e8a, #03045e);
    }
    .result-card {
        background: rgba(0, 119, 182, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 8px rgba(0, 119, 182, 0.2);
    }
    .success-banner {
        background: linear-gradient(to right, #023e8a, #03045e);
        color: white;
        padding: 15px;
        font-size: 18px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0px 2px 8px rgba(0, 119, 182, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("ℹ How to Use This Tool?")
st.sidebar.markdown("""
- Upload your resume in PDF format.
- The AI will extract and analyze your resume.
- You'll receive detailed insights and career suggestions.
""")

# Title
st.markdown('<h1 class="main-title">📄 AI-Powered Resume Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload your Resume PDF for Insights and Suggestions</p>', unsafe_allow_html=True)

# File Uploader
uploaded_file = st.file_uploader("📂 Upload Resume (PDF only)", type=["pdf"])

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

# Resume Analysis Prompt
def analyze_resume(text):
    model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
    prompt = f"""
    You are an expert career coach and resume analyst.

    Analyze the following resume and provide a structured report including:
    1. Candidate's Name (if mentioned)
    2. Career Summary
    3. Top 5 Skills
    4. Education Summary
    5. Work Experience Highlights
    6. Weak Areas / Improvements
    7. Suggestions for Enhancement
    8. Recommended Job Roles

    Resume Text:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "⚠ Error analyzing resume."

# Resume Upload Flow
if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")

    with st.spinner("📄 Extracting text..."):
        extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        st.error("⚠ Failed to extract text. Make sure it's not a scanned image.")
    else:
        with st.spinner("🤖 Analyzing your resume..."):
            insights = analyze_resume(extracted_text)

        st.subheader("📋 Resume Insights Report")
        st.markdown(f'<div class="result-card"><b>📄 Analysis for {uploaded_file.name}</b></div>', unsafe_allow_html=True)
        st.write(insights)
        st.markdown('<div class="success-banner">🎉 Analysis Completed! Use these insights to improve your resume. 🚀</div>', unsafe_allow_html=True)
        st.balloons()

    os.remove(file_path)
