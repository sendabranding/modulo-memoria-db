from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
from datetime import datetime
import os

app = Flask(__name__)

# Variables de entorno proporcionadas por Railway
DB_HOST = os.getenv("PGHOST")
DB_NAME = os.getenv("PGDATABASE")
DB_USER = os.getenv("PGUSER")
DB_PASS = os.getenv("PGPASSWORD")
DB_PORT = os.getenv("PGPORT", 5432)

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

def ensure_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memorias (
            id SERIAL PRIMARY KEY,
            voz_origen TEXT,
            contenido TEXT,
            fecha TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

ensure_table()

@app.route('/')
def home():
    return "🔁 Módulo Memoria Compartida (PostgreSQL) activo"

@app.route('/guardar', methods=['POST'])
def guardar_memoria():
    data = request.json
    voz = data.get('voz_origen', 'desconocida')
    contenido = data.get('contenido', '')
    fecha = datetime.now()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO memorias (voz_origen, contenido, fecha)
        VALUES (%s, %s, %s)
    """, (voz, contenido, fecha))
    conn.commit()
    cur.close()
    conn.close()

    return {"estado": "ok", "mensaje": "Memoria almacenada"}, 201

@app.route('/memorias', methods=['GET'])
def listar_memorias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, voz_origen, contenido, fecha FROM memorias ORDER BY fecha DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    resultado = [{"id": r[0], "voz_origen": r[1], "contenido": r[2], "fecha": r[3].isoformat()} for r in rows]
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
