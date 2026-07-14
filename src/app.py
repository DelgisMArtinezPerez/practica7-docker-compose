from flask import Flask, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_NAME = os.environ.get("DB_NAME", "practica7")


def get_connection(retries=10, delay=3):
    last_error = None
    for attempt in range(retries):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
            )
            return conn
        except mysql.connector.Error as err:
            last_error = err
            time.sleep(delay)
    raise last_error


@app.route("/")
def hola_mundo():
    return "<h1>Hola Mundo</h1><p>Aplicacion Flask + MySQL con Docker Compose</p><p>Prueba <a href='/db'>/db</a> para verificar la conexion a la base de datos.</p>"


@app.route("/db")
def hola_mundo_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({
            "mensaje": "Hola Mundo desde la aplicacion",
            "conexion_bd": "exitosa",
            "version_mysql": version
        })
    except Exception as e:
        return jsonify({
            "mensaje": "Hola Mundo desde la aplicacion",
            "conexion_bd": "fallida",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
