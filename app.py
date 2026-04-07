@app.route('/chat', methods=['POST'])
def chat():
    api_key = os.environ.get("GEMINI_API_KEY")
    user_msg = request.json.get("message")
    
    # Lista de modelos e versões para garantir conexão
    configs = [
        {"v": "v1beta", "m": "gemini-1.5-flash"},
        {"v": "v1", "m": "gemini-1.0-pro"}
    ]
    
    for config in configs:
        url = f"https://generativelanguage.googleapis.com/{config['v']}/models/{config['m']}:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": user_msg}]}]}
        
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=15)
            if res.status_code == 200:
                return jsonify({"response": res.json()['candidates'][0]['content']['parts'][0]['text']})
        except:
            continue
            
    return jsonify({"response": "ERRO TÁTICO: Verifique sua GEMINI_API_KEY no painel do Render."}), 500

