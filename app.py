import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"response": "ERRO: GEMINI_API_KEY não encontrada."}), 500
    
    user_msg = request.json.get("message")
    
    # Lista de endpoints táticos para tentativa e erro (v1 e v1beta)
    endpoints = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    ]
    
    last_error = "404"
    for url in endpoints:
        try:
            payload = {
                "contents": [{"parts": [{"text": user_msg}]}],
                "systemInstruction": {"parts": [{"text": "Você é AYZA, inteligência tática avançada. Responda em português."}]}
            }
            res = requests.post(url, json=payload, timeout=10)
            
            if res.status_code == 200:
                data = res.json()
                return jsonify({"response": data['candidates'][0]['content']['parts'][0]['text']})
            else:
                last_error = f"Status {res.status_code}"
                continue # Tenta o próximo modelo da lista
        except Exception as e:
            last_error = str(e)
            continue

    return jsonify({"response": f"FALHA CRÍTICA EM TODOS OS MODELOS: {last_error}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
