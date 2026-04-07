import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    api_key = os.environ.get("GEMINI_API_KEY")
    user_msg = request.json.get("message")

    # Lista de modelos para tentar (Evita o erro 404)
    models = ["gemini-1.5-pro", "gemini-1.0-pro"]

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            response = requests.post(url, json={
                "contents": [{"parts": [{"text": user_msg}]}]
            }, timeout=10)

            if response.status_code == 200:
                res_data = response.json()
                return jsonify({"response": res_data['candidates'][0]['content']['parts'][0]['text']})
        except:
            continue

    return jsonify({"response": "SISTEMA: Erro de conexão com todos os núcleos."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
cat << 'EOF' > app.py
import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    api_key = os.environ.get("GEMINI_API_KEY")
    user_msg = request.json.get("message")

    # Lista de modelos para tentar (Evita o erro 404)
    models = ["gemini-1.5-pro", "gemini-1.0-pro"]

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            response = requests.post(url, json={
                "contents": [{"parts": [{"text": user_msg}]}]
            }, timeout=10)

            if response.status_code == 200:
                res_data = response.json()
                return jsonify({"response": res_data['candidates'][0]['content']['parts'][0]['text']})
        except:
            continue

    return jsonify({"response": "SISTEMA: Erro de conexão com todos os núcleos."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
