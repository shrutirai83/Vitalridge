
Vital Ridge – AI Healthcare Platform 🏥🤖

Project Overview:

Vital Ridge is a prototype AI-powered healthcare platform designed to demonstrate how digital health solutions can support patients and doctors.

It combines a clean front-end interface with a Flask-based backend powered by AI/ML models for tasks like: 

Chat with MI (AI health assistant) 💬

Medical report analysis 📑

Prescription generation 💊

Vaccination record management 💉

Drug data lookup 🔍

Doctor consultation module 🩺

This project serves as a conceptual demo and proof-of-concept, showcasing both UI/UX design and AI-driven healthcare capabilities.

🛠️ Tech Stack Frontend:

HTML, CSS, JavaScript

Backend: Python (Flask) PyPDF2 (PDF text extraction) pytesseract + Pillow (OCR for images) Hugging Face Transformers (NLP pipelines) Groq API (LLM integration for chat & report analysis)

Others:

JSON for structured outputs
File uploads (PDF/Image) for report analysis

🚀 Features

AI Health Chatbot (MI) – GPT-like conversational assistant for patient queries

Medical Report Analyzer – Upload PDF or image reports, get structured analysis (findings, vitals, lab results, concerns, recommendations)

Prescription Generator – (Prototype page ready for extension)

Doctor Consultation Module – Demo flow for doctor-patient interactions

Vaccination Records – Manage patient immunization history

Drug Data Lookup – Simple drug information access

⚡ Installation & Run Locally

Clone the repository:

git clone https://github.com/shrutirai83/Vitalridge.git

cd Vitalridge

Create virtual environment & install dependencies:

python -m venv venv

source venv/bin/activate # On Windows: venv\Scripts\activate

pip install -r requirements.txt

Run the app:

python app.py

Open in browser: http://127.0.0.1:5000

Disclaimer:

⚠️ This project is a prototype/demo and not intended for real medical use.

All outputs are for demonstration purposes only. Always consult a licensed medical professional for health advice.
