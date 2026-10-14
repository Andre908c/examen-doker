import os

from flask import Flask, jsonify, request, send_from_directory

from db import get_connection, init_db

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(APP_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")


@app.get("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.get("/api/productos")
def listar_productos():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, nombre, categoria, precio FROM productos ORDER BY id DESC"
    )
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(filas)


@app.post("/api/productos")
def guardar_producto():
    datos = request.get_json(silent=True) or request.form
    nombre = (datos.get("nombre") or "").strip()
    categoria = (datos.get("categoria") or "").strip()
    precio_raw = datos.get("precio")

    if not nombre or not categoria or precio_raw in (None, ""):
        return jsonify({"error": "Todos los campos son obligatorios."}), 400

    try:
        precio = float(precio_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "El precio debe ser un número."}), 400

    if precio < 0:
        return jsonify({"error": "El precio no puede ser negativo."}), 400

    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, categoria, precio) VALUES (%s, %s, %s)",
        (nombre, categoria, precio),
    )
    conexion.commit()
    producto_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    return jsonify(
        {
            "id": producto_id,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
        }
    ), 201


if __name__ == "__main__":
    init_db()
    puerto = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=puerto)
