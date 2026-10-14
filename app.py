from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, categoria, precio) VALUES (?, ?, ?)", (nombre, categoria, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    return render_template('index.html', productos=productos)

if __name__ == '__main__':
    init_sqlite_db()
    app.run(host='0.0.0.0', port=5000)