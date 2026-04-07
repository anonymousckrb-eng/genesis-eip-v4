import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Integração com a Inteligência Groq para respostas organizadas
    api_key = os.environ.get("GROQ_API_KEY")
    user_msg = request.json.get("message")
    
    if not api_key:
        return jsonify({"response": "ERRO: GROQ_API_KEY não configurada."}), 500

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Prompt de sistema para garantir o formato de relatório tático
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system", 
                "content": "Você é a AYZA. Responda sempre no formato: // GROQ_INTELLIGENCE_REPORT. Use negrito, tópicos e uma linguagem técnica de inteligência tática."
            },
            {"role": "user", "content": user_msg}
        ]
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            return jsonify({"response": data['choices'][0]['message']['content']})
        else:
            return jsonify({"response": f"Falha no Núcleo Groq: {res.status_code}"}), 500
    except Exception as e:
        return jsonify({"response": f"Erro de Conexão: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

