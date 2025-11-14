🧬 AI Medical Report Analyzer
An AI-powered web application that analyzes medical reports using OCR technology and provides instant health insights with interactive visualizations.

🆕 NEW: Urine Test Analysis!
Now supports comprehensive urinalysis with 16 parameters including pH, protein, glucose, blood, WBC, RBC, and more. Detects UTIs, kidney disease, diabetes, and kidney stones. Ask the AI chatbot detailed questions about urinary health!

✨ Features
Core Functionality
📄 Upload medical reports (PDF, JPG, PNG)
🔍 High-quality OCR extraction with image preprocessing
🎨 Color-coded health status indicators
💡 AI-generated health insights
📱 Responsive, modern UI
🎯 Interactive Visualizations
📊 Bar Charts - Overview of all test results with color coding
🎯 Gauge Charts - Individual test gauges with normal range indicators
📈 Pie Charts - Status distribution (Normal/High/Low)
🕸️ Radar Charts - Multi-parameter comparison in spider web format
📉 Trend Charts - Simulated historical trends over 6 months
📦 Box Plots - Statistical distribution analysis
🔥 Heatmaps - Correlation matrix between test parameters
🌐 3D Scatter Plots - Advanced 3D visualization of key parameters
🔄 Interactive Comparison - Dynamic slider to compare your values with normal ranges
🤖 AI Health Assistant Chatbot (ENHANCED!)
Comprehensive Answers - 10x more detailed responses (500-1,000 words)
Interactive Q&A - Ask questions about your test results
Smart Context - Understands your specific report data
Medical Knowledge - Explains tests, ranges, and health tips
Action Plans - Detailed food lists, lifestyle changes, supplements
Natural Language - Chat naturally, no technical jargon needed
Instant Answers - Get immediate responses to health questions
Personalized Insights - Tailored advice based on your results
Structured Information - Emojis, bullet points, clear sections
🎨 Enhanced User Experience
Tab Navigation - Organized charts into Overview, Gauges, Trends, and Advanced tabs
Animated Counters - Smooth number animations for summary statistics
Hover Effects - Interactive tooltips and hover states
Smooth Transitions - Fade-in animations for all elements
Responsive Design - Works perfectly on desktop, tablet, and mobile
Floating Chat Button - Easy access to AI assistant
Installation
Prerequisites
Python 3.8+ installed
Tesseract OCR installed:
Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
Add Tesseract to PATH or set in code
Poppler (for PDF support):
Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/
Setup
Install dependencies:
pip install -r requirements.txt
If Tesseract is not in PATH, add this to app.py:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
Run the application:
python app.py
Open browser to: http://localhost:5000
🩺 Supported Tests
Blood Tests
Hemoglobin, WBC, RBC, Platelets
Neutrophils, Lymphocytes
Glucose, Cholesterol (Total, HDL, LDL)
Triglycerides, Creatinine, Urea
Liver enzymes (ALT, AST)
Thyroid (TSH)
Hematocrit, MCV, MCH, MCHC
💧 Urine Tests (NEW!)
Physical Properties: pH, Specific Gravity
Chemical Analysis: Protein, Glucose, Ketones, Blood, Bilirubin, Urobilinogen, Nitrite, Leukocyte Esterase
Microscopic Examination: WBC/Pus Cells, RBC, Epithelial Cells, Bacteria, Crystals, Casts
Detects:

Urinary Tract Infections (UTI)
Kidney Disease
Diabetes
Kidney Stones
Dehydration
Liver Problems
Usage
Click or drag-drop your medical report (blood or urine test)
Click "Analyze Report"
View results, charts, and health insights
Ask the AI chatbot questions about your results
Tech Stack
Backend: Flask
OCR: Pytesseract + OpenCV
Visualization: Plotly
Frontend: HTML/CSS/JavaScript
Data Processing: Pandas, NumPy
Customization
Edit reference_data.csv to modify normal ranges for medical tests.

Note
This tool is for informational purposes only. Always consult healthcare professionals for medical advice.
