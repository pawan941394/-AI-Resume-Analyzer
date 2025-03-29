# 🚀 AI Resume Analyzer

![Resume Analyzer Banner](https://img.shields.io/badge/AI-Resume%20Analyzer-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0%2B-red)
![Google Gemini](https://img.shields.io/badge/AI-Gemini%20AI-yellow)

An AI-powered application that analyzes your resume against specific job descriptions, providing personalized feedback and recommendations to help improve your chances of landing your dream job.

<div align="center">
 <img src="https://github.com/pawan941394/-AI-Resume-Analyzer/blob/main/screenshoots/Screenshot%202025-03-29%20115400.png" alt="AI Resume Analyzer Screenshot">
</div>

## 🌐 Live Demo

Try out the application now without any installation:

[**🔗 Live Demo: Job Cracking Resume Analyzer**](https://job-cracking.streamlit.app/)

## 📺 Video Tutorial

Learn how to use and customize this project step-by-step:

[![Watch the tutorial](https://img.shields.io/badge/YouTube-Watch%20Tutorial-red?style=for-the-badge&logo=youtube)](https://youtu.be/CotlWZ5nx3A?si=-f0EcuwvYShA9AL-)

Check out more Python and AI tutorials on my channel:
[Pawan Kumar - Python Tutorials](https://www.youtube.com/@Pawankumar-py4tk/videos)

## ✨ Features

- **Resume Analysis**: Upload your resume and get a comprehensive analysis against a specific job description
- **Match Scoring**: Receive a percentage score showing how well your resume matches the job requirements
- **Strengths & Weaknesses**: Identify key strengths in your resume and areas that need improvement
- **Missing Keywords**: Discover important keywords and skills from the job description missing in your resume
- **Format Analysis**: Get feedback on your resume's structure, organization, and presentation
- **Interactive Chat**: Ask follow-up questions about your analysis and get personalized advice
- **Optimized Resume Generation**: Request an AI-generated optimized resume based on the analysis
- **Animated UI**: Enjoy a responsive and animated user interface for better experience

<div align="center">
  <table>
    <tr>
      <td><img src="https://github.com/pawan941394/-AI-Resume-Analyzer/blob/main/screenshoots/analysis.png" alt="Resume Analysis" width="100%"></td>
      <td><img  src="https://github.com/pawan941394/-AI-Resume-Analyzer/blob/main/screenshoots/chat.png" alt="Interactive Chat" width="100%"></td>
    </tr>
    <tr>
      <td align="center"><b>Resume Analysis</b></td>
      <td align="center"><b>Interactive Chat</b></td>
    </tr>
  </table>
</div>

## 🎨 UI Animation Features

The application includes several animations to enhance the user experience:

- **Sliding Chat Messages**: Messages slide in from the left (user) or right (AI) with a smooth fade-in effect
- **Hover Effects**: Interactive elements like upload boxes and job detail sections have subtle lift animations on hover
- **Button Animations**: Buttons feature elevation and color changes when hovered
- **Transition Effects**: Smooth transitions between different states and sections
- **Loading Animations**: Visual feedback during resume analysis and AI response generation
- **Gradient Text Effects**: Dynamic gradient coloring for headings

These animations make the application feel more responsive and engaging while providing visual feedback during interactions.

## 📋 Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get it here](https://ai.google.dev/))

## 🔧 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/pawan941394/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

You have two options to use this application:

### Option 1: Use the Live Demo

Visit our hosted version at [**https://job-cracking.streamlit.app/**](https://job-cracking.streamlit.app/) to use the application without any setup.

<div align="center">
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Live Demo Usage" width="60%">
</div>

### Option 2: Run Locally

<div align="center">
  <img src="https://github.com/pawan941394/-AI-Resume-Analyzer/blob/main/screenshoots/second.png" alt="Local Setup" width="80%">
</div>

1. Run the application using Streamlit:
   ```bash
   streamlit run resume_analyzer.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Enter your Google Gemini API key in the sidebar configuration section

4. Upload your resume (PDF format)

5. Enter the job title and paste the job description

6. Click "Analyze Resume" to get insights

7. Use the chat interface to ask follow-up questions or request an optimized resume

## 📸 Screenshots

<div align="center">
  <img src="https://github.com/pawan941394/-AI-Resume-Analyzer/blob/main/screenshoots/Screenshot%202025-03-29%20115400.png" alt="Main Interface" width="80%">
  <p><i>Resume Dashboard Example</i></p>
  
  <img src="https://github.com/pawan941394/-AI-Resume-Analyzer/blob/main/screenshoots/analysis.png" alt="Analysis Results" width="80%">
  <p><i>Analysis Results Example</i></p>
  
  <img src="https://github.com/pawan941394/-AI-Resume-Analyzer/blob/main/screenshoots/chat.png" alt="Chat Interface" width="80%">
  <p><i>Interactive Chat Interface Example</i></p>
</div>

## 🛠️ How It Works



1. **Resume Extraction**: The application extracts text from your uploaded PDF resume
2. **AI Analysis**: Google's Gemini AI compares your resume against the job description
3. **Results Presentation**: Results are presented in a structured format with actionable insights
4. **Interactive Assistance**: The AI coach can answer specific questions and provide tailored advice

## 🔐 API Key Configuration

This application requires a Google Gemini API key to function:

1. Visit [Google AI Studio](https://ai.google.dev/) to create an account and obtain an API key
2. Enter the API key in the sidebar of the application
3. Your key is only used for the current session and is not stored permanently

## 🔄 Future Improvements

- Support for more document formats (DOCX, TXT, etc.)
- Integration with job posting APIs to automatically retrieve job descriptions
- Enhanced visualization of resume-to-job matching
- Resume formatting suggestions with visual examples
- Improved accessibility features
- Additional UI animations and transitions for a more polished experience
- Dark mode with animated transitions

## 🎓 Learn More

For a comprehensive tutorial on how this application works and how to customize it for your needs, watch my detailed video guide:

[📺 AI Resume Analyzer Tutorial](https://youtu.be/CotlWZ5nx3A?si=-f0EcuwvYShA9AL-)

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) for powering the analysis
- [Streamlit](https://streamlit.io/) for the web application framework
- [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF text extraction

## 📬 Contact

If you have any questions, feel free to reach out or open an issue in this repository.

Subscribe to [my YouTube channel](https://www.youtube.com/@Pawankumar-py4tk/videos) for more tutorials on Python, AI, and web development.

---

⭐️ If you found this project helpful, please give it a star on GitHub! ⭐️
