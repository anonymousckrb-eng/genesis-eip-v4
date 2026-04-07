import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__, static_folder='.')

# Puxa a chave que você já configurou no painel do Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
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
        if not model: return jsonify({"response": "ERRO: Chave API não detectada."}), 500

        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])

        response = chat_sessions[user_id].send_message(f"Aja como AYZA. Usuário: {msg}")
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"FALHA TÁTICA: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
