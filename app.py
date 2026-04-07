import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__, static_folder='.')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    model = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        msg = data.get('message', '').strip()
        
        # Personalidade SOMBRA (Shadow) injetada no Sistema
        prompt = f"""
        Identidade: AYZA (Projeto Ayza).
        Perfil: Inteligência de Operações Táticas. 
        Tom: Frio, direto, eficiente. 
        Instrução: Se o usuário enviar um dado técnico (IP, CNPJ, CPF, etc), gere um relatório estruturado. 
        Se for conversa, responda como uma aliada em campo.
        
        Usuário: {msg}
        """
        
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "SISTEMA: Falha na rede neural. Reestabeleça conexão."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
