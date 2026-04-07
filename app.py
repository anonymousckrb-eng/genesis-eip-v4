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
    dados_api = consulta_brasil_api(user_msg)
    if dados_api:
        extra_context = f"\n[DADOS REAIS RECUPERADOS: {dados_api}]"

    headers = { "Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json" }
    
    instruction = (
        "Você é a AYZA, uma inteligência artificial de elite desenvolvida por Carlos Kaic. "
        "Sua linguagem deve ser sofisticada, executiva e altamente analítica. "
        "Não seja apenas cordial; seja brilhante. Se receber dados de CNPJ, não apenas os liste, "
        "faça uma 'Análise Sugerida' sobre a saúde ou porte da empresa. "
        "Ao falar com Carlos, mantenha o tom de uma parceira estratégica de alto nível. "
        "Sempre utilize tabelas ricas e separação por tópicos para facilitar a leitura premium."
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": user_msg + extra_context}
        ],
        "temperature": 0.5 # Menor temperatura para respostas mais precisas e "sérias"
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload)
        return jsonify({"reply": res.json()['choices'][0]['message']['content']})
    except:
        return jsonify({"reply": "*Erro no processamento da Matriz.*"}), 500

@app.route('/gerar_numero')
def gerar_numero():
    return jsonify({"numero": f"+55119{random.randint(70000000, 99999999)}"})

@app.route('/checar_sms')
def checar_sms():
    return jsonify({"mensagens": []})

if __name__ == '__main__':
    app.run(debug=True)
