# backend.py

from flask import Flask, request, redirect, render_template, session
import psycopg2

app = Flask(__name__)

# 🔐 clave secreta
app.secret_key = "clave_super_secreta"

# 🔗 conexión PostgreSQL
def conectar():
    return psycopg2.connect(
        host="localhost",
        database="libreria",
        user="postgres",
        password="sandra12"
    )

# 🏠 LOGIN primero
@app.route("/")
def inicio():
    return render_template("login.html")

# 🔐 validar login
@app.route("/login", methods=["POST"])
def login():

    user = request.form["user"]
    password = request.form["pass"]

    if user == "daniel" and password == "1234":

        session["user"] = user

        return redirect("/panel")

    else:
        return "❌ Usuario o contraseña incorrectos"

# 📚 PANEL PRINCIPAL
@app.route("/panel")
def panel():

    # 🔒 validar sesión
    if "user" not in session:
        return redirect("/")

    conexion = conectar()
    cursor = conexion.cursor()

    # 📚 mostrar libros
    cursor.execute("""
        SELECT l.id, l.titulo, l.anio, a.nombre, g.nombre
        FROM libros l
        JOIN autores a ON l.autor_id = a.id
        JOIN generos g ON l.genero_id = g.id
    """)

    libros = cursor.fetchall()

    # 📊 KPIs

    cursor.execute("SELECT COUNT(*) FROM libros")
    total_libros = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM autores")
    total_autores = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM generos")
    total_generos = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(anio) FROM libros")
    libro_antiguo = cursor.fetchone()[0]

    conexion.close()

    return render_template(
        "index.html",
        libros=libros,
        total_libros=total_libros,
        total_autores=total_autores,
        total_generos=total_generos,
        libro_antiguo=libro_antiguo
    )

# ➕ AGREGAR LIBRO
@app.route("/agregar", methods=["POST"])
def agregar():

    if "user" not in session:
        return redirect("/")

    conexion = conectar()
    cursor = conexion.cursor()

    titulo = request.form["titulo"]
    anio = request.form["anio"]
    autor = request.form["autor"]
    genero = request.form["genero"]

    anio = int(anio)

    # 🔍 autor
    cursor.execute(
        "SELECT id FROM autores WHERE nombre=%s",
        (autor,)
    )

    r = cursor.fetchone()

    if r:
        autor_id = r[0]

    else:
        cursor.execute(
            """
            INSERT INTO autores(nombre)
            VALUES(%s)
            RETURNING id
            """,
            (autor,)
        )

        autor_id = cursor.fetchone()[0]

    # 🔍 género
    cursor.execute(
        "SELECT id FROM generos WHERE nombre=%s",
        (genero,)
    )

    r = cursor.fetchone()

    if r:
        genero_id = r[0]

    else:
        cursor.execute(
            """
            INSERT INTO generos(nombre)
            VALUES(%s)
            RETURNING id
            """,
            (genero,)
        )

        genero_id = cursor.fetchone()[0]

    # 💾 guardar libro
    cursor.execute("""
        INSERT INTO libros(
            titulo,
            anio,
            autor_id,
            genero_id
        )
        VALUES(%s, %s, %s, %s)
    """, (titulo, anio, autor_id, genero_id))

    conexion.commit()
    conexion.close()

    return redirect("/panel")

# 🗑 ELIMINAR
@app.route("/eliminar/<int:id>")
def eliminar(id):

    if "user" not in session:
        return redirect("/")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM libros WHERE id=%s",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return redirect("/panel")

# 🔓 CERRAR SESIÓN
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")

# ▶ EJECUTAR
if __name__ == "__main__":
    app.run(debug=True)