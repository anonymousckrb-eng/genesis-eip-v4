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
        return jsonify({"response": "ERRO: Chave API não configurada no Render."}), 500

    try:
        user_msg = request.json.get("message")
        # Conexão direta via REST para evitar erros de versão do SDK
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": user_msg}]}],
            "systemInstruction": {"parts": [{"text": "Você é AYZA, uma IA de inteligência tática. Responda de forma direta e em português."}]}
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            bot_response = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"response": bot_response})
        else:
            return jsonify({"response": f"Falha na API: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"response": f"Erro interno: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
