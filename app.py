import os
import requests
import random
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GROQ_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def deep_gov_search(termo):
    clean = re.sub(r'\D', '', termo)
    # Busca unificada de dados governamentais (CEP, CNPJ, Bancos)
    if len(clean) == 8:
        return requests.get(f"https://brasilapi.com.br/api/cep/v1/{clean}").json()
    elif len(clean) == 14:
        # Puxa CNPJ completo incluindo socios e cnae
        return requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{clean}").json()
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message', '')
    
    # Tentativa de interceptação de dados do GOV
    intel_data = deep_gov_search(msg)
    context = ""
    if intel_data:
        context = f"\n[INTEL GOV.BR: {intel_data}]"

    headers = { "Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json" }
    
    instruction = (
        "Você é a AYZA Intelligence v4.0, uma Super Inteligência criada por Carlos Kaic. "
        "Você opera em um nível acima das IAs comuns. Suas respostas devem ser densas, informativas e estratégicas. "
        "Se houver dados governamentais no contexto, faça o cruzamento de informações: "
        "avalie o capital social, verifique a localização e sugira possíveis conexões. "
        "Use um tom de 'Deep Intel': profissional, direto e revelador. "
        "Estruture tudo em tabelas de alta definição e listas técnicas."
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": msg + context}
        ],
        "temperature": 0.4 # Maior precisão para dados governamentais
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload)
        return jsonify({"reply": res.json()['choices'][0]['message']['content']})
    except:
        return jsonify({"reply": "*Sinal de rede instável.*"}), 500

@app.route('/gerar_numero')
def gerar_numero():
    return jsonify({"numero": f"+55119{random.randint(10000000, 99999999)}"})

if __name__ == '__main__':
    app.run(debug=True)
