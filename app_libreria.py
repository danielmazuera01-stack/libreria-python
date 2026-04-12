# ➕ Agregar libro (CORREGIDO)
def agregar_libro():
    conexion = conectar()
    cursor = conexion.cursor()

    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")

    #  Buscar autor_id
    cursor.execute("SELECT id FROM autores WHERE nombre = %s", (autor,))
    resultado_autor = cursor.fetchone()

    if resultado_autor:
        autor_id = resultado_autor[0]
    else:
        print("❌ Autor no existe")
        conexion.close()
        return

    #  Buscar genero_id
    cursor.execute("SELECT id FROM generos WHERE nombre = %s", (genero,))
    resultado_genero = cursor.fetchone()

    if resultado_genero:
        genero_id = resultado_genero[0]
    else:
        print("❌ Género no existe")
        conexion.close()
        return

    #  Insertar libro
    cursor.execute("""
        INSERT INTO libros (titulo, autor_id, genero_id)
        VALUES (%s, %s, %s)
    """, (titulo, autor_id, genero_id))

    conexion.commit()
    conexion.close()

    print("✅ Libro agregado")