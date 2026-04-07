from flask import Flask, request, jsonify, session
import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "ayza_secret_777")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LOGIN_PASSWORD = os.getenv("APP_PASSWORD", "admin123")
DB = "sms.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS numeros (id INTEGER PRIMARY KEY AUTOINCREMENT, numero TEXT, criado_em TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS mensagens (id INTEGER PRIMARY KEY AUTOINCREMENT, numero TEXT, mensagem TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data.get("senha") == LOGIN_PASSWORD:
        session["logado"] = True
        return jsonify({"status": "ok"})
    return jsonify({"status": "erro"}), 401

@app.route("/gerar_numero")
def gerar_numero():
    try:
        url = "https://receive-sms.cc/Free-Phone-Number/"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        numeros = [link.text.strip() for link in soup.select("a[href*='/sms/']") if "+" in link.text]
        
        if not numeros:
            return jsonify({"error": "Nenhum número disponível"}), 500
        
        numero = numeros[0]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO numeros (numero, criado_em) VALUES (?, ?)", (numero, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return jsonify({"numero": numero})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/checar_sms/<numero>")
def checar_sms(numero):
    try:
        clean_num = numero.replace("+","")
        url = f"https://receive-sms.cc/sms/{clean_num}/"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        linhas = soup.select("table tbody tr")
        
        codigo = None
        for linha in linhas:
            texto = linha.text.strip()
            if "minutes ago" in texto or "Just now" in texto:
                codigo = texto
                break
        return jsonify({"status": "ok", "codigo": codigo})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": data.get("message")}]})
        msg = r.json()["choices"][0]["message"]["content"]
        return jsonify({"response": "// GROQ_INTELLIGENCE_REPORT\n" + msg})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
