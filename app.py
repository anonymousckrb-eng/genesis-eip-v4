import os
import requests
from flask import Flask, request, jsonify, send_from_directory

# DEFINIÇÃO DO APP (O que estava faltando no seu erro)
app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    api_key = os.environ.get("GEMINI_API_KEY")
    user_msg = request.json.get("message")
    
    if not api_key:
        return jsonify({"response": "ERRO: Chave API ausente no painel Render."}), 500
    
    # Tentativa em múltiplos modelos (v1beta e v1) para evitar erro 404
    configs = [
        {"v": "v1beta", "m": "gemini-1.5-flash"},
        {"v": "v1", "m": "gemini-1.0-pro"}
    ]
    
    for config in configs:
        url = f"https://generativelanguage.googleapis.com/{config['v']}/models/{config['m']}:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": user_msg}]}]}
        
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=15)
            if res.status_code == 200:
                return jsonify({"response": res.json()['candidates'][0]['content']['parts'][0]['text']})
        except:
            continue
            
    return jsonify({"response": "ERRO TÁTICO: Falha na comunicação com os núcleos de IA."}), 500

if __name__ == "__main__":
    # Garante que o Flask use a porta correta do Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

