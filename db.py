import os
import time

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "3306")),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "root"),
    "database": os.environ.get("DB_NAME", "mydb"),
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_db(intentos=20, espera=2):
    ultimo_error = None
    for _ in range(intentos):
        try:
            conexion = mysql.connector.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
            )
            cursor = conexion.cursor()
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            cursor.execute("USE mydb")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS productos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(120) NOT NULL,
                    categoria VARCHAR(80) NOT NULL,
                    precio DECIMAL(10, 2) NOT NULL
                )
                """
            )
            conexion.commit()
            cursor.close()
            conexion.close()
            return
        except Error as error:
            ultimo_error = error
            time.sleep(espera)

    raise RuntimeError(f"No se pudo conectar a MySQL (mydb): {ultimo_error}")
