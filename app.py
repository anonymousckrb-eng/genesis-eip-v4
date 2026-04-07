import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__, static_folder='.')

api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not model:
        return jsonify({"response": "ERRO: Chave API ausente no Render."}), 500
    try:
        data = request.get_json()
        msg = data.get('message', '')
        prompt = f"Aja como AYZA, IA tática. Usuário: {msg}"
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "ERRO DE CONEXAO CENTRAL."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
