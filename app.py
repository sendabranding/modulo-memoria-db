from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
db_path = "memorias.db"

def ensure_table():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS memorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voz_origen TEXT,
                contenido TEXT,
                fecha TIMESTAMP
            );
        """)
        conn.commit()

ensure_table()

@app.route("/")
def home():
    return "🧠 Módulo Memoria Compartida (SQLite) activo"

@app.route("/guardar", methods=["POST"])
def guardar_memoria():
    data = request.json
    voz = data.get("voz_origen", "desconocida")
    contenido = data.get("contenido", "")
    fecha = datetime.now()

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO memorias (voz_origen, contenido, fecha)
            VALUES (?, ?, ?)
        """, (voz, contenido, fecha))
        conn.commit()

    return jsonify({"estado": "ok", "mensaje": "Memoria almacenada"}), 201

@app.route("/memorias", methods=["GET"])
def obtener_memorias():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, voz_origen, contenido, fecha FROM memorias ORDER BY fecha DESC")
        filas = cur.fetchall()

    resultado = [
        {"id": row[0], "voz_origen": row[1], "contenido": row[2], "fecha": row[3]}
        for row in filas
    ]
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
