import psycopg2

# Conectar a la base de datos por defecto
conexion = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="sandra12",
    client_encoding='utf-8'
)

conexion.autocommit = True
cursor = conexion.cursor()

# Crear la base de datos
cursor.execute("CREATE DATABASE tu_base;")

cursor.close()
conexion.close()

print("Base de datos 'tu_base' creada exitosamente.")