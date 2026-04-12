import psycopg2

# Conectar a la base de datos tu_base
conexion = psycopg2.connect(
    host="localhost",
    database="tu_base",
    user="postgres",
    password="sandra12",
    client_encoding='utf-8'
)

cursor = conexion.cursor()

# Leer el archivo SQL
with open('libreria_db.session.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

# Ejecutar el SQL
cursor.execute(sql)

conexion.commit()
cursor.close()
conexion.close()

print("Esquema de la base de datos creado exitosamente.")