import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__, static_folder='.')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    model = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        msg = data.get('message', '').strip()
        if not msg: return jsonify({"response": "ALVO VAZIO"})

        prompt = f"""
        Aja como o sistema GENESIS_V22. 
        Gere um relatório estruturado exatamente neste estilo:
        
        // GROQ_INTELLIGENCE_REPORT
        **Relatório de Risco Rápido e Tático**
        
        **Alvo:** {msg}
        
        **Plataformas Detectadas:**
        - Analise possíveis vínculos em redes sociais e bancos de dados.
        
        **Análise Inicial:**
        1. Descreva o perfil de risco.
        2. Liste vulnerabilidades digitais encontradas.
        """

        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"ERRO OPERACIONAL: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
