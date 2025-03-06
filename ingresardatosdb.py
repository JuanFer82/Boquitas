import pandas as pd
import mysql.connector
import numpy as np

# Ruta del archivo Excel
ruta_excel = r"C:\Users\Jufeguti\Documents\Turno\servicios entregados.xlsx"

# Leer el archivo Excel
df = pd.read_excel(ruta_excel)

# Reemplazar NaN con None (para que MySQL los interprete como NULL)
df = df.replace({np.nan: None})

# Configuración de la conexión a la base de datos
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="gioti"
)
cursor = db_connection.cursor()

# Consulta SQL para insertar datos
consulta = """
INSERT INTO servicios (serv, nom_sre, promesa_serv) 
VALUES (%s, %s, %s)
"""

# Insertar cada fila en la base de datos
for _, fila in df.iterrows():
    valores = (fila["Servicio"], fila["Ing. SRE"], fila["Promesa del Servicio"])
    cursor.execute(consulta, valores)

# Confirmar cambios
db_connection.commit()

# Cerrar conexión
cursor.close()
db_connection.close()

print("Datos insertados correctamente en MySQL.")
