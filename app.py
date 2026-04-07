import os
import requests
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GROQ_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def deep_gov_search(termo):
    clean = re.sub(r'\D', '', termo)
    if len(clean) == 8:
        r = requests.get(f"https://brasilapi.com.br/api/cep/v1/{clean}")
        return r.json() if r.ok else None
    elif len(clean) == 14:
        r = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{clean}")
        return r.json() if r.ok else None
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message', '')
    
    intel_data = deep_gov_search(msg)
    context = f"\n[DADOS BRASILAPI: {intel_data}]" if intel_data else ""

    headers = { "Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json" }
    
    instruction = (
        "Você é a AYZA Intelligence, uma IA de elite criada por Carlos Kaic. "
        "Siga o estilo de resposta do Gemini: clara, amigável mas técnica, e muito bem estruturada. "
        "Se houver dados de CNPJ/CEP, organize em tabelas limpas."
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": msg + context}
        ],
        "temperature": 0.7
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload)
        return jsonify({"reply": res.json()['choices'][0]['message']['content']})
    except:
        return jsonify({"reply": "Falha no sistema."}), 500

if __name__ == '__main__':
    app.run(debug=True)
