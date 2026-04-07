import os
import requests
from flask import Flask, request as req, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not GEMINI_API_KEY:
        return jsonify({"response": "ERRO: Chave API ausente no Render."}), 500
    
    try:
        data = req.get_json()
        msg = data.get('message', '').strip()
        
        # CONEXÃO DIRETA (BYPASS DO SDK)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{"parts": [{"text": msg}]}],
            "systemInstruction": {"parts": [{"text": "Aja como AYZA, uma inteligência artificial tática e eficiente. Responda sempre em português."}]}
        }
        headers = {'Content-Type': 'application/json'}
        
        api_resp = requests.post(url, json=payload, headers=headers)
        
        if api_resp.status_code == 200:
            texto_final = api_resp.json()['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"response": texto_final})
        else:
            return jsonify({"response": f"FALHA DE COMUNICAÇÃO: {api_resp.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"response": f"FALHA CRÍTICA DE SISTEMA: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
