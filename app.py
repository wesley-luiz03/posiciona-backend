from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS acessos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, evento TEXT NOT NULL, data_hora DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/api/track', methods=['POST'])
def track():
    data = request.json
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO acessos (evento) VALUES (?)", (data.get('evento'),))
    conn.commit()
    conn.close()
    return jsonify({"status": "capturado"}), 201

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute('SELECT evento, COUNT(*) as total FROM acessos GROUP BY evento')
    results = cursor.fetchall()
    conn.close()
    return jsonify({row[0]: row[1] for row in results})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    # Verifique se os dados batem exatamente com o que você digita
    if data.get('username') == 'admin' and data.get('password') == 'posiciona2026':
        return jsonify({"auth": True}), 200
    return jsonify({"auth": False}), 401

import os
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)