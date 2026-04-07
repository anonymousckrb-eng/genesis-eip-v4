import os
import requests
import random
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
    msg = data.get('message', '').strip()
    if not msg:
        return jsonify({"error": "Prompt vazio"}), 400

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Você é a AYZA, operando em modo stealth. Seja direta, técnica e eficiente."},
            {"role": "user", "content": msg}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if not response.ok:
            return jsonify({"error": "Erro Groq", "details": response.json()}), response.status_code
        
        res_data = response.json()
        return jsonify({"reply": res_data['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gerar_numero')
def gerar_numero():
    prefixos = ["+55119", "+1202", "+4477", "+336", "+4915"]
    num = random.choice(prefixos) + "".join([str(random.randint(0,9)) for _ in range(8)])
    return jsonify({"numero": num, "status": "ativo"})

@app.route('/checar_sms')
def checar_sms():
    num = request.args.get('num')
    exemplos = [
        {"from": "Google", "text": "Seu código de verificação é 492031"},
        {"from": "WhatsApp", "text": "Não compartilhe este código: 122-334"},
        {"from": "Telegram", "text": "Código de login: 99821"}
    ]
    if random.random() > 0.6:
        return jsonify({"mensagens": [random.choice(exemplos)]})
    return jsonify({"mensagens": []})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
