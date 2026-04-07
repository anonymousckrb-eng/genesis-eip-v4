from flask import Flask, request, jsonify, render_template, session
import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

app.secret_key = os.getenv("SECRET_KEY", "devkey")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LOGIN_PASSWORD = os.getenv("APP_PASSWORD", "123456")

DB = "sms.db"

# ================================
# DATABASE INIT
# ================================
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS numeros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT,
        criado_em TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS mensagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT,
        mensagem TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================================
# HOME (FIX 404)
# ================================
@app.route("/")
def index():
    return render_template("index.html")

# ================================
# LOGIN
# ================================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    senha = data.get("senha")

    if senha == LOGIN_PASSWORD:
        session["logado"] = True
        return jsonify({"status": "ok"})
    return jsonify({"status": "erro"}), 401

def protegido():
    return session.get("logado")

# ================================
# SCRAPER
# ================================
def buscar_numeros():
    url = "https://receive-sms.cc/Free-Phone-Number/"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    numeros = []

    for link in soup.select("a[href*='/sms/']"):
        numero = link.text.strip()
        if "+" in numero:
            numeros.append(numero)

    return list(set(numeros))

# ================================
# GERAR NÚMERO
# ================================
@app.route("/gerar_numero")
def gerar_numero():
    if not protegido():
        return jsonify({"error": "não autorizado"}), 403

    numeros = buscar_numeros()

    if not numeros:
        return jsonify({"error": "nenhum número encontrado"}), 500

    numero = numeros[0]

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT INTO numeros (numero, criado_em) VALUES (?, ?)",
              (numero, datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({"numero": numero})

# ================================
# CHECAR SMS
# ================================
@app.route("/checar_sms/<numero>")
def checar_sms(numero):
    if not protegido():
        return jsonify({"error": "não autorizado"}), 403

    try:
        url = f"https://receive-sms.cc/sms/{numero.replace('+','')}/"
        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        mensagens = soup.select("table tbody tr")

        codigo = None

        conn = sqlite3.connect(DB)
        c = conn.cursor()

        for msg in mensagens:
            texto = msg.text.strip()

            if any(char.isdigit() for char in texto):
                codigo = texto

                c.execute("""
                INSERT INTO mensagens (numero, mensagem, timestamp)
                VALUES (?, ?, ?)
                """, (numero, texto, datetime.now().isoformat()))

        conn.commit()
        conn.close()

        return jsonify({"codigo": codigo})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================================
# GROQ CHAT
# ================================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        r = requests.post(url, headers=headers, json=payload, timeout=30)

        res = r.json()
        msg = res["choices"][0]["message"]["content"]

        return jsonify({
            "response": "// GROQ_INTELLIGENCE_REPORT\n" + msg
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================================
# RUN LOCAL
# ================================
if __name__ == "__main__":
    app.run(debug=True)
