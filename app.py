from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

# Conexión con la base de datos PostgreSQL usando variables de entorno
def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=os.getenv("PGPORT", 5432)
    )

# Crear tabla si no existe
def ensure_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memorias (
            id SERIAL PRIMARY KEY,
            voz_origen TEXT,
            contenido TEXT,
            fecha TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

ensure_table()

@app.route("/")
def home():
    return "🧠 Módulo Memoria Compartida (PostgreSQL) activo"

@app.route("/guardar", methods=["POST"])
def guardar_memoria():
    data = request.json
    voz = data.get("voz_origen", "desconocida")
    contenido = data.get("contenido", "")
    fecha = datetime.now()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO memorias (voz_origen, contenido, fecha) VALUES (%s, %s, %s)",
        (voz, contenido, fecha)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"estado": "ok", "mensaje": "Memoria almacenada"}), 201

if __name__ == "__main__":
    app.run(debug=True)
