import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__, static_folder='.')

# Captura a chave API das variáveis de ambiente do Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Usando o nome de modelo mais estável para produção
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        model = None
else:
    model = None

# Memória de conversa para manter o contexto
chat_sessions = {}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not model:
        return jsonify({"response": "SISTEMA: Chave API não configurada no Render."}), 500
    
    try:
        data = request.get_json()
        msg = data.get('message', '').strip()
        user_id = request.remote_addr

        if not msg:
            return jsonify({"response": "SISTEMA: Aguardando entrada de dados..."})

        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])

        # Instrução de personalidade Shadow
        instruction = "Você é AYZA. Responda de forma técnica e direta. Usuário: "
        
        response = chat_sessions[user_id].send_message(instruction + msg)
        return jsonify({"response": response.text})
        
    except Exception as e:
        # Retorna o erro real para facilitar o diagnóstico se persistir
        return jsonify({"response": f"ERRO DE CONEXÃO: Verifique os Logs no Render."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
