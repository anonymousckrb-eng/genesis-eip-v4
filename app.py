import os, requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    key = os.environ.get("GROQ_API_KEY")
    msg = request.json.get("message")
    
    if not key:
        return jsonify({"response": "ERRO: GROQ_API_KEY ausente."}), 500

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Você é a AYZA. Responda como um // GROQ_INTELLIGENCE_REPORT tático."},
            {"role": "user", "content": msg}
        ]
    }
    
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                         json=payload, 
                         headers={"Authorization": f"Bearer {key}"}, 
                         timeout=15)
        return jsonify({"response": r.json()['choices'][0]['message']['content']})
    except:
        return jsonify({"response": "Erro na rede neural Groq."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

