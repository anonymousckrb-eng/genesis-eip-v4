import os
import requests
from flask import Flask, request, jsonify, send_from_directory

# ==================== CONFIGURAÇÃO PRINCIPAL ====================
# Definimos static_folder='.' para ele achar o index.html na raiz
app = Flask(__name__, static_folder='.') 

# Chave da Groq vinda do ambiente (configurada no Render)
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

SYSTEM_PROMPT = """Você é AYZA Intelligence, o núcleo tático de inteligência artificial do dashboard AYZA.

REGRAS OBRIGATÓRIAS:
1. Toda resposta DEVE começar EXATAMENTE com: // GROQ_INTELLIGENCE_REPORT
2. Use tom de relatório tático militar/estratégico: claro, conciso e organizado.
3. Estruture com seções e bullet points.
4. Responda exclusivamente em português (Brasil)."""

# ==================== ROTAS ====================

@app.route('/')
def index():
    """Serve o arquivo index.html direto da raiz do projeto"""
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint que processa mensagens e consulta a Groq API"""
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY não configurada no Render."}), 500

    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Mensagem vazia."}), 400

    user_message = data['message']

    # Configuração da chamada para Groq
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.6
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        groq_response = response.json()
        ai_message = groq_response['choices'][0]['message']['content'].strip()
        
        return jsonify({"response": ai_message})
        
    except Exception as e:
        return jsonify({"error": f"Erro na conexão: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

