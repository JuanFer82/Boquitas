#limpiar tabla de la base de datos


import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="gioti"
)

cursor = conexion.cursor()

try:
    # Elimina todos los registros de la tabla
    cursor.execute("DELETE FROM notificaciones;")
    # Reinicia el contador de auto-incremento
    cursor.execute("ALTER TABLE notificaciones AUTO_INCREMENT = 1;")
    # Confirma los cambios
    conexion.commit()
    print("Todos los movimientos han sido eliminados y el contador de 'id' ha sido reiniciado.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conexion.close()