import streamlit as st
import os
import tempfile
import PyPDF2
import google.generativeai as genai
from PIL import Image
import io
import base64
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""

# Initialize additional session state variables
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_title' not in st.session_state:
    st.session_state.job_title = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""

# Add custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stApp {
    }
    .stButton button {
        background-color: #4361ee;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    .stButton button:hover {
        background-color: #3a56e4;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    .result-container {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #4361ee;
        margin: 20px 0;
    }
    h1, h2, h3 {
        color: #2C3E50;
        font-weight: 700;
    }
    h1 {
        background: linear-gradient(90deg, #4361ee, #3a0ca3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
    }
    .highlight {
        padding: 10px;
        border-left: 5px solid #4361ee;
        margin: 10px 0;
    }
    .section-header {
        padding: 10px 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        border-left: 4px solid #4361ee;
        font-weight: bold;
    }
    .chat-user {
        padding: 12px 15px;
        border-radius: 15px 15px 15px 0;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        position: relative;
        animation: slideInLeft 0.3s ease;
    }
    .chat-ai {
        padding: 12px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 3px solid #4361ee;
        position: relative;
        animation: slideInRight 0.3s ease;
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .upload-section, .job-details-section {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 100%;
        transition: transform 0.3s ease;
    }
    .upload-section:hover, .job-details-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    /* Custom file uploader */
    .stFileUploader > div:first-child {
        width: 100%;
        border: 2px dashed #4361ee;
        background-color: rgba(67, 97, 238, 0.05);
        border-radius: 8px;
        padding: 25px 0;
    }
    .stFileUploader > div:first-child:hover {
        background-color: rgba(67, 97, 238, 0.1);
    }
    /* Input fields styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px 15px;
    }
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #ccc;
    }
</style>
""", unsafe_allow_html=True)

# Function that adds icons to section headers
def section_header(title, icon):
    return f"<div class='section-header'>{icon} {title}</div>"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_file.read())
        temp_file_path = temp_file.name
    
    with open(temp_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    
    os.unlink(temp_file_path)
    return text

# Configure Gemini AI
def configure_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring Gemini AI: {e}")
        return False

# Function to analyze resume
def analyze_resume(resume_text, job_title, job_description):
    model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
    
    prompt = f"""
    Act as an expert resume analyst and career coach. You are analyzing a resume for a {job_title} position.
    
    JOB DESCRIPTION:
    {job_description}
    
    RESUME:
    {resume_text}
    
    Provide a comprehensive analysis of the resume compared to the job requirements. Structure your analysis as follows:
    
    1. Match Score: Provide a percentage match score between the resume and job description.
    
    2. Key Strengths: List 3-5 strengths in the resume that align well with the job requirements.
    
    3. Improvement Areas: List 3-5 specific areas where the resume could be improved to better match the job.
    
    4. Missing Skills/Keywords: Identify specific skills or keywords from the job description that are missing in the resume.
    
    5. Format and Presentation: Analyze the structure, organization, and presentation of the resume.
    
    6. Action Items: Provide 3-5 specific, actionable recommendations to improve the resume for this specific job application.
    
    Your analysis should be detailed, specific, and actionable. Use bullet points where appropriate for clarity.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing resume: {e}"

# Function to ask questions about the resume
def ask_question_about_resume(resume_text, job_title, job_description, question):
    model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
    
    prompt = f"""
    Act as an expert resume analyst and career coach. You are analyzing a resume for a {job_title} position.
    
    JOB DESCRIPTION:
    {job_description}
    
    RESUME:
    {resume_text}
    
    QUESTION: {question}
    
    Provide a detailed, insightful, and helpful response to the question based on your analysis of how the resume matches with the job requirements.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Function to generate a sample optimized resume
def generate_sample_resume(resume_text, job_title, job_description, analysis_result):
    model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
    
    prompt = f"""
    Act as an expert resume writer. Based on the following information, create a sample optimized resume that would be highly suitable for the {job_title} position.
    
    ORIGINAL RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    ANALYSIS OF THE ORIGINAL RESUME:
    {analysis_result}
    
    Create a well-formatted, professional resume that:
    1. Incorporates the missing skills and keywords identified in the analysis
    2. Addresses the improvement areas mentioned
    3. Builds upon the strengths already present in the original resume
    4. Uses a professional and ATS-friendly format
    5. Includes all relevant sections (Summary, Experience, Skills, Education, etc.)
    
    Format the resume in markdown with clear sections and bullet points for readability.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating sample resume: {e}"

# Function to handle chat messages
def handle_chat_message(message, resume_text, job_title, job_description, analysis_result):
    # Check if it's a resume generation request
    if any(phrase in message.lower() for phrase in ["provide resume", "generate resume", "create resume", "sample resume", "optimized resume"]):
        st.info("Generating an optimized sample resume based on the analysis...")
        sample_resume = generate_sample_resume(resume_text, job_title, job_description, analysis_result)
        return "Here's a sample optimized resume based on our analysis. Use this as a template to improve your own resume:\n\n" + sample_resume
    
    # Regular chat response
    model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
    prompt = f"""
    You are a helpful resume coach assistant. The user has received an analysis of their resume for a {job_title} position.
    
    RESUME CONTENT:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    ANALYSIS RESULTS:
    {analysis_result}
    
    USER QUESTION: {message}
    
    Provide a helpful, supportive, and actionable response to help them improve their resume based on the analysis.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Function to submit a message to the chat
def submit_message():
    user_message = st.session_state.user_input
    if user_message:
        # Add user message to chat history
        st.session_state.chat_history.append({"text": user_message, "is_user": True})
        
        # Get response
        with st.spinner("Thinking..."):
            response_text = handle_chat_message(
                user_message,
                st.session_state.resume_text,
                st.session_state.job_title,
                st.session_state.job_description,
                st.session_state.analysis_result
            )
            
        # Add assistant response to chat history
        st.session_state.chat_history.append({"text": response_text, "is_user": False})
        
        # Clear the input by setting our custom session state variable (not the widget state)
        st.session_state.user_input = ""

# Main application
def main():
    st.markdown("<h1 style='text-align: center;'>🚀 AI Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Optimize your resume for your dream job with AI-powered analysis and feedback</p>", unsafe_allow_html=True)
    
    # Sidebar for API key
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Enter your Google Gemini API Key", type="password")
        if api_key:
            if configure_gemini(api_key):
                st.success("Gemini API configured successfully!")
            else:
                st.error("Failed to configure Gemini API. Check your API key.")
        
        st.markdown("### About")
        st.info(
            """
            This app uses Google's Gemini AI to analyze your resume against job descriptions.
            Get insights on how well your resume matches the job requirements and receive
            personalized recommendations to improve your chances.
            """
        )

    # Tabs for different functionalities
    tab1, tab2 = st.tabs(["Resume Analysis", "Ask Questions"])
    
    # Resume Analysis Tab
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(section_header("📄 Upload Your Resume", "📤"), unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="upload-section">', unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
                
                if uploaded_file is not None:
                    st.success("✅ Resume uploaded successfully!")
                    try:
                        resume_text = extract_text_from_pdf(uploaded_file)
                        st.session_state.resume_text = resume_text  # Store in session state
                        with st.expander("🔍 Preview Extracted Text"):
                            st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
                    except Exception as e:
                        st.error(f"Error extracting text from PDF: {e}")
                        resume_text = ""
                        st.session_state.resume_text = ""
                else:
                    st.info("📁 Please upload your resume in PDF format")
                    resume_text = ""
                    if 'resume_text' not in st.session_state:
                        st.session_state.resume_text = ""
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(section_header("💼 Job Details", "📋"), unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="job-details-section">', unsafe_allow_html=True)
                job_title = st.text_input("Job Title", placeholder="e.g., Data Scientist")
                st.session_state.job_title = job_title
                
                job_description = st.text_area("Job Description", height=200, 
                                    placeholder="Paste the job description here...")
                st.session_state.job_description = job_description
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Analyze button with enhanced styling
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            analyze_button = st.button(
                "🔍 Analyze Resume", 
                key="analyze_btn", 
                disabled=not (api_key and resume_text and job_title and job_description)
            )
        
        # Analysis section - always show if there's an analysis result
        if st.session_state.analysis_result:
            st.markdown(section_header("📊 Analysis Results", "🎯"), unsafe_allow_html=True)
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.markdown(st.session_state.analysis_result)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Process the analysis when button is clicked
        if analyze_button:
            with st.spinner("⏳ Analyzing your resume..."):
                analysis = analyze_resume(resume_text, job_title, job_description)
                st.session_state.analysis_result = analysis
                
                # Show the analysis after it's done
                st.markdown(section_header("📊 Analysis Results", "🎯"), unsafe_allow_html=True)
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown(analysis)
                st.markdown('</div>', unsafe_allow_html=True)
                
        # Chat section - always show if there's an analysis result
        if st.session_state.analysis_result:
            st.markdown(section_header("💬 Ask Follow-up Questions", "❓"), unsafe_allow_html=True)
            st.write("Ask questions about the analysis or request specific feedback about your resume")
            
            # Create a container for chat messages with better styling
            chat_container = st.container()
            
            # Display chat history in the container with improved styling
            with chat_container:
                for message in st.session_state.chat_history:
                    if message["is_user"]:
                        st.markdown(f'<div class="chat-user"><strong>You:</strong> {message["text"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-ai"><strong>AI Assistant:</strong> {message["text"]}</div>', unsafe_allow_html=True)
            
            # Chat input with a send button - better styled
            col1, col2 = st.columns([5, 1])  # Adjust the ratio as needed
            
            with col1:
                # Text input without on_change callback
                st.text_input(
                    "Type your question here:", 
                    key="chat_input",
                    placeholder="e.g., How can I improve my technical skills section?",
                    value=st.session_state.user_input,
                    # No on_change parameter here
                )
                
                # Update user_input whenever chat_input changes
                st.session_state.user_input = st.session_state.chat_input
            
            with col2:
                # Add some vertical space to align the button with the input field
                st.write("")
                # Add the send button
                if st.button("Send ✉️", key="send_button"):
                    submit_message()
                    # Use st.rerun() instead of st.experimental_rerun()
                    st.rerun()
    
    # Ask Questions Tab - With improved styling
    with tab2:
        if not st.session_state.resume_text:
            st.info("📋 Please upload your resume in the 'Resume Analysis' tab first.")
        elif not st.session_state.job_title or not st.session_state.job_description:
            st.info("💼 Please enter job details in the 'Resume Analysis' tab first.")
        else:
            st.markdown(section_header("❓ Ask Questions About Your Resume", "🔍"), unsafe_allow_html=True)
            st.write("Ask anything about how your resume fits the job or how to improve it.")
            
            with st.container():
                st.markdown('<div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
                question = st.text_area("Your Question", placeholder="e.g., What are the top 3 skills I should add to my resume for this job?")
                
                col_q1, col_q2, col_q3 = st.columns([1, 2, 1])
                with col_q2:
                    ask_button = st.button("Get Answer 🔍", key="question_btn", disabled=not (api_key and question))
                st.markdown('</div>', unsafe_allow_html=True)
                
                if ask_button:
                    with st.spinner("⏳ Thinking..."):
                        answer = ask_question_about_resume(st.session_state.resume_text, st.session_state.job_title, st.session_state.job_description, question)
                    
                    st.markdown(section_header("💬 Answer", "✨"), unsafe_allow_html=True)
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown(answer)
                    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
