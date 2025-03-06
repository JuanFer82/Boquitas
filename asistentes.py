import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import base64

# Lista de orden de equipos
orden_equipos = [
    "Líder Mesa", "Operación Nube", "Centro de Gestión y Monitoreo",
    "Soporte Canales", "Información Procesada y Operación Malla",
    "Base de Datos", "Iseries", "Pseries", "Infraestructura Seguridad",
    "Plataformas Distribuidas", "Telecomunicaciones", "Integración",
    "Accesos Plataformas Iseries", "Accesos Plataformas Windows",
    "SOA", "Centro de Cómputo"
]

# Función para obtener integrantes de un equipo específico
def obtener_integrantes(db_connection, equipo):
    try:
        cursor = db_connection.cursor()
        query = "SELECT integrante FROM disponibles WHERE equipo = %s ORDER BY integrante ASC"
        cursor.execute(query, (equipo,))
        resultados = cursor.fetchall()
        cursor.close()
        return [integrante[0] for integrante in resultados]
    except Exception as e:
        st.error(f"Error al obtener integrantes: {e}")
        return []

# Función para obtener detalles de un integrante específico
def obtener_detalles_integrante(db_connection, integrante):
    try:
        cursor = db_connection.cursor()
        query = "SELECT celular, correo, equipo FROM disponibles WHERE integrante = %s"
        cursor.execute(query, (integrante,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado if resultado else (None, None, None)
    except Exception as e:
        st.error(f"Error al obtener detalles del integrante: {e}")
        return (None, None, None)

# Función para insertar un nuevo registro en la base de datos
def insertar_registro(db_connection, nombre, celular, correo, equipo):
    try:
        cursor = db_connection.cursor()
        query = "INSERT INTO disponibles (integrante, celular, correo, equipo) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, celular, correo, equipo))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        st.error(f"Error al insertar registro: {e}")

# Función para actualizar un registro existente en la base de datos
def actualizar_registro(db_connection, integrante, nuevo_celular, nuevo_correo, nuevo_equipo):
    try:
        cursor = db_connection.cursor()
        query = "UPDATE disponibles SET celular = %s, correo = %s, equipo = %s WHERE integrante = %s"
        cursor.execute(query, (nuevo_celular, nuevo_correo, nuevo_equipo, integrante))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        st.error(f"Error al actualizar registro: {e}")

# Función para eliminar un registro de la base de datos
def eliminar_registro(db_connection, integrante):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM disponibles WHERE integrante = %s"
        cursor.execute(query, (integrante,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        st.error(f"Error al eliminar registro: {e}")

# Función para mostrar los turnos y equipos disponibles
def mostrar_turnos(db_connection):
    Opcion_turno = [
        "ASISTENTES MESA GIOTI TURNO 06:00 AM A 02:00 PM",
        "ASISTENTES MESA GIOTI TURNO 02:00 PM A 10:00 PM",
        "ASISTENTES MESA GIOTI TURNO 10:00 PM A 06:00 AM",
    ]
    
    turno_seleccionado = st.selectbox("Selecciona un Turno:", Opcion_turno, key="turno_seleccionado")
    
    opcion_equipos = {equipo: equipo for equipo in orden_equipos}
    equipo_seleccionado = st.selectbox("Selecciona un Servicio:", list(opcion_equipos.keys()), key="equipo_seleccionado")
    equipo_filtrado = opcion_equipos[equipo_seleccionado]
    
    integrantes = obtener_integrantes(db_connection, equipo_filtrado)

    return integrantes, equipo_filtrado, opcion_equipos, turno_seleccionado

################### Función para crear la imagen
def crear_imagen(turno_seleccionado, df):
    fig, ax = plt.subplots(figsize=(25, 10))

    # Establecer el fondo negro
    ax.set_facecolor('black')

    # Agregar imágenes
    img1 = mpimg.imread("C:/Users/Jufeguti/boquitas/fondo1.png")
    ax.imshow(img1, aspect='auto', extent=[0.4, 0.6, 0.85, 1])

    # Título
    ax.text(0.5, 0.85, turno_seleccionado, fontsize=22, ha='center', va='bottom', color='white', transform=ax.transAxes)

    # Formatear tabla con bordes
    table_data = []
    current_rol = None

    for index, row in df.iterrows():
        if row['ROL'] != current_rol:
            current_rol = row['ROL']
            table_data.append([current_rol, row['INTEGRANTE'], row['CELULAR'], row['CORREO']])
        else:
            table_data.append(['', row['INTEGRANTE'], row['CELULAR'], row['CORREO']])  # ROL vacío para filas adicionales

    # Crear tabla
    table = ax.table(cellText=table_data,
                     colLabels=['ROL', 'INTEGRANTE', 'CELULAR', 'CORREO'],
                     cellLoc='center',
                     loc='center',
                     bbox=[0.1, 0.15, 0.8, 0.6])

    # Estilo de la tabla
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1.2, 1.2)  # Escalar la tabla

    # Ajustar tamaño de celdas según el texto
    for (i, cell) in table.get_celld().items():
        cell.set_edgecolor('white')  # Bordes blancos
        cell.set_linewidth(1)
        cell.set_facecolor('black')  # Color de fondo negro para las celdas
        cell.set_text_props(color='white')  # Texto blanco
        
        if i[0] == 0:  # Encabezados
            cell.set_text_props(weight='bold')
        else:
            if i[1] == 0:  # ROL a la izquierda
                cell.set_text_props(ha='left')
            elif i[1] == 1:  # INTEGRANTE a la izquierda
                cell.set_text_props(ha='left')
            else:  # CELULAR y CORREO al centro
                cell.set_text_props(ha='center')

        cell.set_height(0.1)  # Ajustar altura de la celda
        cell.set_width(0.2)  # Ajustar ancho de la celda basado en contenido

    ax.axis('off')  # Ocultar ejes
    plt.tight_layout()

    # Guardar la imagen con mayor resolución
    plt.savefig("output.png", bbox_inches='tight', facecolor='black', dpi=300)  # Ajuste de DPI
    plt.close(fig)

##############################

# Función para mostrar las acciones disponibles
def mostrar_acciones(integrantes, db_connection, equipo_filtrado, opcion_equipos, turno_seleccionado):
    acciones = ["Crear Tabla", "Nuevo Registro", "Editar Registro", "Eliminar Registro"]
    accion_seleccionada = st.sidebar.radio("Selecciona una Acción:", acciones, key="accion_seleccionada")

    if accion_seleccionada == "Crear Tabla":
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame(columns=['ROL', 'INTEGRANTE', 'CELULAR', 'CORREO'])

        integrante_seleccionado = st.selectbox("Selecciona el Integrante:", integrantes, key="integrante_seleccionado")

        if st.button("Añadir a la Tabla", key="añadir_a_la_tabla"):
            celular, correo, equipo = obtener_detalles_integrante(db_connection, integrante_seleccionado)
            nuevo_registro = pd.DataFrame({'ROL': [equipo_filtrado], 'INTEGRANTE': [integrante_seleccionado], 'CELULAR': [celular], 'CORREO': [correo]})
            st.session_state.df = pd.concat([st.session_state.df, nuevo_registro], ignore_index=True)
            st.session_state.df['ROL'] = pd.Categorical(st.session_state.df['ROL'], categories=orden_equipos, ordered=True)
            st.session_state.df = st.session_state.df.sort_values('ROL').reset_index(drop=True)
            st.success("Integrante añadido a la tabla.")

        if st.session_state.df.empty:
            st.text("No hay integrantes en la tabla.")
        else:
            st.dataframe(st.session_state.df)

            integrante_a_eliminar = st.selectbox("Selecciona el Integrante para Eliminar:", st.session_state.df['INTEGRANTE'].unique(), key="integrante_a_eliminar")

            # Distribuir botones en una fila
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                if st.button("Eliminar de la Tabla", key="eliminar_de_la_tabla"):
                    st.session_state.df = st.session_state.df[st.session_state.df['INTEGRANTE'] != integrante_a_eliminar].reset_index(drop=True)
                    st.success("Integrante eliminado de la tabla.")

            with col2:
                if st.button("Crear Imagen", key="crear_imagen"):
                    crear_imagen(turno_seleccionado, st.session_state.df)
                    st.image("output.png")

                    # Copiar imagen al portapapeles
                    with open("output.png", "rb") as f:
                        img_base64 = base64.b64encode(f.read()).decode()
                    href = f'<a href="data:image/png;base64,{img_base64}" download="output.png">Copiar Imagen al Portapapeles</a>'
                    st.markdown(href, unsafe_allow_html=True)

            with col3:
                if st.button("Limpiar Tabla", key="limpiar_tabla"):
                    st.session_state.df = pd.DataFrame(columns=['ROL', 'INTEGRANTE', 'CELULAR', 'CORREO'])
                    st.success("Tabla borrada exitosamente.")

    elif accion_seleccionada == "Nuevo Registro":
        nombre = st.text_input("Nombre del Integrante:")
        celular = st.text_input("Celular del Integrante:")
        correo = st.text_input("Correo del Integrante:")
        
        if st.button("Registrar Integrante", key="registrar_integrante"):
            insertar_registro(db_connection, nombre, celular, correo, equipo_filtrado)
            st.success("Integrante registrado exitosamente.")
    
    elif accion_seleccionada == "Editar Registro":
        integrante_seleccionado = st.selectbox("Selecciona el Integrante para Editar:", integrantes, key="integrante_a_editar")
        if integrante_seleccionado:
            celular_actual, correo_actual, equipo_actual = obtener_detalles_integrante(db_connection, integrante_seleccionado)
            nuevo_celular = st.text_input("Nuevo Celular:", value=celular_actual)
            nuevo_correo = st.text_input("Nuevo Correo:", value=correo_actual)
            
            # Verificar si equipo_actual es válido
            if equipo_actual in opcion_equipos.keys():
                nuevo_equipo = st.selectbox("Nuevo Equipo:", opcion_equipos.keys(), key="nuevo_equipo", index=list(opcion_equipos.keys()).index(equipo_actual))
            else:
                nuevo_equipo = st.selectbox("Nuevo Equipo:", opcion_equipos.keys(), key="nuevo_equipo")
                st.warning(f"El equipo actual '{equipo_actual}' no está en la lista de equipos disponibles.")

            if st.button("Actualizar Registro", key="actualizar_registro"):
                actualizar_registro(db_connection, integrante_seleccionado, nuevo_celular, nuevo_correo, nuevo_equipo)
                st.success("Registro actualizado exitosamente.")
    
    elif accion_seleccionada == "Eliminar Registro":
        integrante_seleccionado = st.selectbox("Selecciona el Integrante para Eliminar:", integrantes, key="integrante_a_eliminar_registro")

        if st.button("Eliminar Registro", key="eliminar_registro"):
            eliminar_registro(db_connection, integrante_seleccionado)
            st.success("Registro eliminado exitosamente.")

# Función principal
def main(db_connection):
    integrantes, equipo_filtrado, opcion_equipos, turno_seleccionado = mostrar_turnos(db_connection)
    mostrar_acciones(integrantes, db_connection, equipo_filtrado, opcion_equipos, turno_seleccionado)

# Ejecutar la aplicación
if __name__ == "__main__":
    db_connection = None  # Reemplaza con la conexión a tu base de datos
    main(db_connection)