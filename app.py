import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__, static_folder='.')

# Captura a chave que já vimos que está configurada no seu Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Mudança tática: Usando apenas o nome do modelo sem prefixos
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

chat_sessions = {}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        msg = data.get('message', '').strip()
        user_id = request.remote_addr

        if not msg: return jsonify({"response": "SISTEMA: Aguardando entrada."})
        if not model: return jsonify({"response": "ERRO: Chave API não detectada no Render."}), 500

        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])

        # O segredo é deixar a biblioteca gerenciar a versão da API sozinha
        response = chat_sessions[user_id].send_message(msg)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"FALHA NA REDE NEURAL: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
