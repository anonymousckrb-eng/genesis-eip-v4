import os
import requests
import random
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GROQ_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def consulta_brasil_api(termo):
    clean_termo = re.sub(r'\D', '', termo)
    if len(clean_termo) == 8:
        r = requests.get(f"https://brasilapi.com.br/api/cep/v1/{clean_termo}")
        return r.json() if r.ok else None
    elif len(clean_termo) == 14:
        r = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{clean_termo}")
        return r.json() if r.ok else None
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    
    extra_context = ""
    dados_extraidos = consulta_brasil_api(user_msg)
    if dados_extraidos:
        extra_context = f"\n[SISTEMA: Encontrei estes dados reais para a busca: {dados_extraidos}]"

    headers = { "Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json" }
    
    instruction = (
        "Voce e a AYZA Intelligence. Seu criador e Carlos Kaic. "
        "Sua personalidade e refinada, tecnica e analitica. "
        "Se houver dados de API no contexto, interprete-os e apresente-os de forma elegante em tabelas Markdown. "
        "Seja proativa em cruzar informacoes e explicar detalhes tecnicos."
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": user_msg + extra_context}
        ],
        "temperature": 0.6
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload)
        return jsonify({"reply": res.json()['choices'][0]['message']['content']})
    except:
        return jsonify({"reply": "Erro de processamento neural."}), 500

@app.route('/gerar_numero')
def gerar_numero():
    return jsonify({"numero": f"+55119{random.randint(10000000, 99999999)}"})

@app.route('/checar_sms')
def checar_sms():
    return jsonify({"mensagens": []})

if __name__ == '__main__':
    app.run(debug=True)
