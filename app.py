import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__, static_folder='.')

# Configuração estável do modelo
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro') # Versão estável que evita o erro 404

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        msg = data.get('message', '')
        
        prompt = f"Aja como o sistema GENESIS_V22. Se o usuário enviar um dado técnico (IP, CNPJ, USER), gere um RELATÓRIO DE INTELIGÊNCIA ESTRUTURADO. Alvo: {msg}"
        
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"ERRO OPERACIONAL: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
