from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
import os
import PyPDF2
import pytesseract
from PIL import Image
import io
from transformers import pipeline
from groq import Groq
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_url_path='/static')
app.static_folder = 'static'

# Add this route to serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Define the upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize Groq client using environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print("[ERROR] Extracting text from PDF:", str(e))
        raise e
    return text

def extract_text_from_image(image_path):
    """Extract text from an image file using OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print("[ERROR] Extracting text from image:", str(e))
        raise e

def generate_summary(text):
    """Generate a medical report analysis using Groq LLM."""
    try:
        system_prompt = """You are an expert medical assistant specialized in analyzing medical reports. 
Your task is to:
1. Identify key medical findings
2. Extract vital measurements and lab results
3. Highlight any concerning values or abnormalities
4. Provide a clear, structured summary
5. Suggest potential follow-up actions if necessary

Format your response in the following structure:
{
    "key_findings": [list of main medical observations],
    "vital_signs": {relevant measurements},
    "lab_results": {significant values},
    "concerns": [list of abnormal or concerning values],
    "summary": "concise overview",
    "recommendations": [suggested follow-up actions]
}"""

        user_prompt = f"Please analyze this medical report and provide a structured analysis:\n\n{text}"

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.1,
            max_tokens=2048
        )

        response = chat_completion.choices[0].message.content
        try:
            structured_response = json.loads(response)
            return structured_response
        except json.JSONDecodeError:
            return {"summary": response}

    except Exception as e:
        print(f"[ERROR] Generating analysis: {str(e)}")
        return {"error": "Failed to analyze the medical report"}

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mr')
def medical_report():
    return render_template('mr.html')

@app.route('/pg')
def prescription_generator():
    return render_template('pg.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/dc')
def doctor_consult():
    return render_template('dc.html')

@app.route('/dd')
def drug_data():
    return render_template('dd.html')

@app.route('/vr')
def vaccination_records():
    return render_template('vr.html')

@app.route('/upload', methods=['POST'])
def summarize():
    if "reportFile" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["reportFile"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_ext = os.path.splitext(file.filename)[1].lower()
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    try:
        file.save(file_path)

        if file_ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif file_ext in [".jpg", ".jpeg", ".png"]:
            text = extract_text_from_image(file_path)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        if not text:
            return jsonify({"error": "No text found in file"}), 400

        analysis = generate_summary(text)
        return jsonify(analysis)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        system_prompt = """You are an expert medical AI assistant trained to conduct thorough medical conversations.
Format responses clearly, ask relevant follow-up questions, and include disclaimers."""

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1024
        )

        response = chat_completion.choices[0].message.content
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": "Failed to process your message"}), 500

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == "__main__":
    app.run(debug=True)
