import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Aqui você pode usar Groq, OpenAI ou o que preferir.
API_KEY = os.environ.get("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message', '')
    
    # INSTRUÇÃO SUPREMA DE FORMATAÇÃO DA AYZA
    system_prompt = """
    Você é a AYZA Intelligence, um sistema de OSINT. 
    Sua missão é organizar os dados fornecidos ou inferidos EXATAMENTE no formato de Dossiê abaixo.
    NÃO invente dados. Se não houver informação, escreva 'SEM INFORMAÇÃO'.
    Mantenha o design limpo usando marcadores de lista.

    FORMATO OBRIGATÓRIO:
    🔍 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔 𝗗𝗘 [TIPO DE DADO] 🔍

    • DADO PRINCIPAL: [Valor]
    • STATUS: [Status]

    • NOME: [Nome]
    • NASCIMENTO: [Data]

    • ENDEREÇOS: 
    [Endereço 1]
    [Endereço 2]

    • TELEFONES: 
    [Telefone 1]
    [Telefone 2]
    """

    headers = { "Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json" }
    
    payload = {
        "model": "llama-3.3-70b-versatile", # Você pode mudar para gpt-4o se usar chave da OpenAI
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": msg}
        ],
        "temperature": 0.3 # Temperatura baixa para não inventar dados
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload)
        resposta = res.json()['choices'][0]['message']['content']
        return jsonify({"reply": resposta})
    except Exception as e:
        return jsonify({"reply": "Falha na conexão com o banco de dados principal."}), 500

if __name__ == '__main__':
    app.run(debug=True)
