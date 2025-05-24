import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os

# Configure Streamlit
st.set_page_config(
    page_title="UPI Transaction Analyzer",
    page_icon="💰",
    layout="centered"
)

GEMINI_API_KEY = "AIzaSyA4oAnTKbhcyEgx2QR8p56dOsKr1Opd-H8"  

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Main App
st.title("💰 UPI Transaction Analyzer")
st.markdown("""
Upload your UPI transaction PDF for instant financial advice.  
*No data is stored—analysis happens in real-time.*
""")

# File Upload
uploaded_file = st.file_uploader("Choose PDF", type="pdf")

def extract_text(pdf_file):
    """Extract text without storing data"""
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()+ "\n"
    return text.strip()

def analyze_transactions(text):
    """Send text to Gemini for analysis"""
    prompt = f"""
1. **Spending Analysis**:
   - Categorize expenses (Food, Shopping, Bills, Entertainment, etc.)
   - Identify top 3 spending categories by amount
   - Highlight unusual/atypical transactions

2. **Cash Flow Assessment**:
   - Calculate monthly income vs expenses
   - Show net savings rate (as percentage)
   - Identify any negative cash flow periods

3. **Budgeting Recommendations**:
   - Suggest realistic spending limits per category
   - Recommend 3 specific cost-cutting opportunities
   - Highlight recurring subscriptions worth reviewing

4. **Financial Health Check**:
   - Assess emergency fund adequacy
   - Suggest investment opportunities based on surplus
   - Flag any concerning patterns (late payments, overdrafts)

5. **Actionable Insights**:
   - Provide 5 concrete action items
   - Prioritize recommendations by impact
   - Include timeframes for implementation

**Output Format**:
```markdown
### 📊 Spending Analysis
- [Analysis here with bullet points]

### 💰 Cash Flow
- [Key findings with amounts]

### 🎯 Recommendations
1. [Priority 1]
2. [Priority 2] 
    
    {text[:15000]}  # Truncate to avoid token limits
    """
    response = model.generate_content(prompt)
    return response.text

if uploaded_file:
    try:
        with st.spinner("Analyzing..."):
            text = extract_text(uploaded_file)
            if not text.strip():
                st.error("No text found in PDF!")
            else:
                advice = analyze_transactions(text)
                st.success("Analysis Complete!")
                st.subheader("📊 Your Financial Advice")
                st.markdown(advice)
                
                # Optional: Show raw text (debug)
                if st.toggle("Show extracted text"):
                    st.text_area("Raw Text", text, height=200)
                    
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Privacy disclaimer
st.caption("🔒 Your data is processed temporarily and never stored.")