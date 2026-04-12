from flask import Flask, request, redirect, render_template
import psycopg2

app = Flask(__name__)

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="libreria",
        user="postgres",
        password="sandra12"
    )

# 🏠 Inicio
@app.route("/")
def inicio():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT l.id, l.titulo, l.anio, a.nombre, g.nombre
        FROM libros l
        JOIN autores a ON l.autor_id = a.id
        JOIN generos g ON l.genero_id = g.id
    """)
    libros = cursor.fetchall()
    conexion.close()

    return render_template("index.html", libros=libros)

# ➕ Agregar (CREA autor y genero si no existen)
@app.route("/agregar", methods=["POST"])
def agregar():
    conexion = conectar()
    cursor = conexion.cursor()

    titulo = request.form['titulo']
    anio = int(request.form['anio'])
    autor = request.form['autor']
    genero = request.form['genero']

    # 🔍 autor
    cursor.execute("SELECT id FROM autores WHERE nombre=%s", (autor,))
    r = cursor.fetchone()

    if r:
        autor_id = r[0]
    else:
        cursor.execute("INSERT INTO autores (nombre) VALUES (%s) RETURNING id", (autor,))
        autor_id = cursor.fetchone()[0]

    # 🔍 genero
    cursor.execute("SELECT id FROM generos WHERE nombre=%s", (genero,))
    r = cursor.fetchone()

    if r:
        genero_id = r[0]
    else:
        cursor.execute("INSERT INTO generos (nombre) VALUES (%s) RETURNING id", (genero,))
        genero_id = cursor.fetchone()[0]

    # 💾 libro
    cursor.execute("""
        INSERT INTO libros (titulo, anio, autor_id, genero_id)
        VALUES (%s, %s, %s, %s)
    """, (titulo, anio, autor_id, genero_id))

    conexion.commit()
    conexion.close()

    return redirect("/")

# 🗑 eliminar
@app.route("/eliminar/<int:id>")
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM libros WHERE id=%s", (id,))
    conexion.commit()
    conexion.close()

    return redirect("/")

# ▶️ ejecutar
if __name__ == "__main__":
    app.run(debug=True)