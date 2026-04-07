import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"error": "Mensagem vazia recebida pelo servidor."}), 400

    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY nao configurada no servidor."}), 500

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Você é a AYZA Intelligence, uma assistente virtual avançada, objetiva e inteligente."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        
        if not response.ok:
            return jsonify({
                "error": f"Groq API retornou status {response.status_code}",
                "details": response.json()
            }), response.status_code

        response_data = response.json()
        reply = response_data['choices'][0]['message']['content']
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": "Erro interno no servidor.", "details": str(e)}), 500

@app.route('/gerar_numero', methods=['GET', 'POST'])
def gerar_numero():
    return jsonify({
        "status": "sucesso", 
        "acao": "gerar_numero", 
        "mensagem": "Rota de Scraper preservada."
    })

@app.route('/checar_sms', methods=['GET', 'POST'])
def checar_sms():
    return jsonify({
        "status": "sucesso", 
        "acao": "checar_sms",
        "mensagem": "Rota de Scraper preservada."
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
