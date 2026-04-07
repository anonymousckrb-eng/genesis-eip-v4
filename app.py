import os
from flask import Flask, request, jsonify, send_from_directory
from google import genai

app = Flask(__name__, static_folder='.')

# Captura a chave que já está no seu painel
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
    model_id = "gemini-1.5-flash"
else:
    client = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({"response": "ERRO: Chave API não detectada no Render."}), 500
    
    try:
        data = request.get_json()
        msg = data.get('message', '').strip()
        
        # Resposta direta e tática
        response = client.models.generate_content(
            model=model_id,
            contents=msg,
            config={'system_instruction': 'Você é AYZA, uma inteligência artificial tática e eficiente.'}
        )
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"FALHA NA REDE NEURAL: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
