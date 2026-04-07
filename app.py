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
    models = ["gemini-1.5-pro", "gemini-1.5-flash"]
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": user_msg}]}]}, timeout=10)
            if res.status_code == 200:
                return jsonify({"response": res.json()['candidates'][0]['content']['parts'][0]['text']})
        except:
            continue
    return jsonify({"response": "Erro nos núcleos de IA."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

