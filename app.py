"""
LegalLens AI - Flask Backend Server
AI-Powered Legal Assistance & Contract Intelligence Platform
Built for PromptWars 2026 (Google for Developers Challenge)
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv

import groq_service
import document_parser
from sample_contracts import SAMPLE_CONTRACTS

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "legallens-ai-promptwars-secret-2026")
CORS(app)

# Helper to extract API key from header, json payload, or session
def get_request_api_key():
    header_key = request.headers.get("X-Groq-Key")
    if header_key and header_key.strip():
        return header_key.strip()
    
    if request.is_json:
        data = request.get_json(silent=True) or {}
        payload_key = data.get("api_key")
        if payload_key and payload_key.strip():
            return payload_key.strip()
            
    return session.get("groq_api_key") or os.getenv("GROQ_API_KEY")

@app.route("/")
def index():
    """Renders the main LegalLens AI dashboard."""
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    """Returns system status, active engine, and sample contracts."""
    api_key = get_request_api_key()
    has_key = bool(api_key and not api_key.startswith("your_"))
    
    return jsonify({
        "status": "online",
        "system": "LegalLens AI v1.0",
        "engine": "Groq LPU (LLaMA 3.3 70B & 3.1 8B)" if has_key else "LegalLens High-Fidelity Heuristic Engine",
        "has_custom_key": has_key,
        "sample_count": len(SAMPLE_CONTRACTS)
    })

@app.route("/api/samples", methods=["GET"])
def get_samples():
    """Returns available pre-loaded sample contracts for instant testing."""
    samples_list = []
    for k, v in SAMPLE_CONTRACTS.items():
        samples_list.append({
            "id": v["id"],
            "title": v["title"],
            "category": v["category"],
            "parties": v["parties"],
            "summary": v["summary"],
            "text": v["text"]
        })
    return jsonify({"samples": samples_list})

@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Extracts text from uploaded PDF, DOCX, or TXT file."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    try:
        file_bytes = file.read()
        extracted_text, error = document_parser.extract_text_from_bytes(file_bytes, file.filename)
        if error:
            return jsonify({"error": error}), 400
            
        return jsonify({
            "filename": file.filename,
            "text": extracted_text,
            "char_count": len(extracted_text),
            "word_count": len(extracted_text.split())
        })
    except Exception as e:
        return jsonify({"error": f"Failed to parse file: {str(e)}"}), 500

@app.route("/api/analyze", methods=["POST"])
def analyze_endpoint():
    """Analyzes contract text: generates executive summary, ELI5, score, and red flags."""
    data = request.get_json(silent=True) or {}
    contract_text = data.get("text", "").strip()
    if not contract_text:
        return jsonify({"error": "Contract text is required"}), 400
        
    api_key = get_request_api_key()
    try:
        result = groq_service.analyze_contract(contract_text, user_api_key=api_key)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/compare", methods=["POST"])
def compare_endpoint():
    """Compares two contracts (e.g. Original vs Redline Markup)."""
    data = request.get_json(silent=True) or {}
    text_a = data.get("text_a", "").strip()
    text_b = data.get("text_b", "").strip()
    
    if not text_a or not text_b:
        return jsonify({"error": "Both Version 1 and Version 2 texts are required for comparison"}), 400
        
    api_key = get_request_api_key()
    try:
        result = groq_service.compare_contracts(text_a, text_b, user_api_key=api_key)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/interrogate", methods=["POST"])
def interrogate_endpoint():
    """Grounded clause Q&A assistant with exact citations."""
    data = request.get_json(silent=True) or {}
    contract_text = data.get("text", "").strip()
    question = data.get("question", "").strip()
    history = data.get("history", [])
    
    if not contract_text or not question:
        return jsonify({"error": "Both contract text and question are required"}), 400
        
    api_key = get_request_api_key()
    try:
        result = groq_service.interrogate_clause(contract_text, question, chat_history=history, user_api_key=api_key)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/simulate", methods=["POST"])
def simulate_endpoint():
    """Hypothetical 'What-If' scenario dispute simulator."""
    data = request.get_json(silent=True) or {}
    contract_text = data.get("text", "").strip()
    scenario = data.get("scenario", "").strip()
    
    if not contract_text or not scenario:
        return jsonify({"error": "Both contract text and scenario description are required"}), 400
        
    api_key = get_request_api_key()
    try:
        result = groq_service.simulate_scenario(contract_text, scenario, user_api_key=api_key)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/redraft", methods=["POST"])
def redraft_endpoint():
    """Generates balanced, protective, or simplified replacement clauses."""
    data = request.get_json(silent=True) or {}
    clause = data.get("clause", "").strip()
    goal = data.get("goal", "balanced").strip()
    context = data.get("context", "").strip()
    
    if not clause:
        return jsonify({"error": "Clause text to redraft is required"}), 400
        
    api_key = get_request_api_key()
    try:
        result = groq_service.redraft_clause(clause, redraft_goal=goal, contract_context=context, user_api_key=api_key)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/translate", methods=["POST"])
def translate_endpoint():
    """Translates legal clauses or summaries into regional languages."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    target_language = data.get("target_language", "Hindi").strip()
    
    if not text:
        return jsonify({"error": "Text to translate is required"}), 400
        
    api_key = get_request_api_key()
    try:
        result = groq_service.translate_legal_text(text, target_language=target_language, user_api_key=api_key)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/set-api-key", methods=["POST"])
def set_api_key_endpoint():
    """Saves user API key to session or tests its validity."""
    data = request.get_json(silent=True) or {}
    key = data.get("api_key", "").strip()
    if key:
        session["groq_api_key"] = key
        return jsonify({"status": "success", "message": "Groq API key activated"})
    else:
        session.pop("groq_api_key", None)
        return jsonify({"status": "cleared", "message": "Reverted to Built-in Engine"})

if __name__ == "__main__":
    # If --test argument is passed, exit cleanly after initialization
    if "--test" in sys.argv:
        print("LegalLens AI server initialized successfully. Exiting test mode.")
        sys.exit(0)
        
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    print(f"Starting LegalLens AI server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=debug)
