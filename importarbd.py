import pandas as pd
import mysql.connector

# Configuración de la conexión a la base de datos
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="gioti"
)

cursor = db_connection.cursor()

# Leer el archivo de Excel
df = pd.read_excel("C:/Users/Jufeguti/boquitas/serviciosbanco1.xlsx", sheet_name="GIOTI")

# Rellenar los valores NaN con una cadena vacía
df = df.fillna('')

# Convertir la columna 'celular' a string
df['celular'] = df['celular'].astype(str)

# Crear una tabla en MySQL si no existe
create_table_query = """
CREATE TABLE IF NOT EXISTS gioti (
    integrante VARCHAR(500),
    celular VARCHAR(100),
    correo VARCHAR(500),
    equipo VARCHAR(500)
)
"""
cursor.execute(create_table_query)

# Insertar los datos de la DataFrame en la tabla de MySQL
for i, row in df.iterrows():
    insert_query = """
    INSERT INTO gioti (integrante, celular, correo, equipo)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (row['integrante'], row['celular'], row['correo'], row['equipo']))

# Confirmar la transacción
db_connection.commit()

# Cerrar la conexión
cursor.close()
db_connection.close()
