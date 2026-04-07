from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SYSTEM_PROMPT = "Você é uma IA de inteligência tática avançada chamada AYZA. Responda de forma direta, objetiva e técnica."

@app.route("/")
def home():
    return "PROJETO AYZA ONLINE"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.6,
            "max_tokens": 1024
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            return jsonify({"error": f"Erro Groq: {response.status_code}", "details": response.text}), 500
        
        data = response.json()
        ai_response = data["choices"][0]["message"]["content"]
        return jsonify({"response": "// GROQ_INTELLIGENCE_REPORT\n" + ai_response})
    except Exception as e:
        return jsonify({"error": "Falha interna", "details": str(e)}), 500

@app.route("/gerar_sms", methods=["GET"])
def gerar_sms():
    try:
        # Estrutura preparada para integração futura com 5SIM ou SMS-Activate
        mock_data = {
            "numero": "+55 11 91234-5678",
            "status": "AGUARDANDO SMS",
            "mensagens": []
        }
        return jsonify(mock_data)
    except Exception as e:
        return jsonify({"error": "Erro ao gerar número", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
