import streamlit as st
from mysql.connector import Error
import pandas as pd
from datetime import datetime, timedelta
import streamlit.components.v1 as components

def main(db_connection):
    option = st.sidebar.radio("Gestión de Notificaciones", ["Nueva Notificación", "Editar Notificación", "Eliminar Notificación"])

    if option == "Nueva Notificación":
        nueva_notificacion(db_connection)
    elif option == "Editar Notificación":
        editar_notificacion(db_connection)
    elif option == "Eliminar Notificación":
        eliminar_notificacion(db_connection)

def nueva_notificacion(db_connection):
    cantidad_servicios = st.number_input("Cantidad de Servicios Afectados (Max. 2)", min_value=1, max_value=2, value=1, step=1)
    tipo_afectacion = st.selectbox("Selecciona el Tipo de Afectación:", ["Parcial", "Total", "Ok"])
    fecha_falla = None
    fecha_ok = None
    hora_ok = None
        
    servicio_1 = st.selectbox("Selecciona el Servicio 1:", obtener_servicios(db_connection))
    # Mostrar Ing. Sre. y Promesa de Servicio para servicio_1
    if servicio_1:
        cursor = db_connection.cursor()
        cursor.execute("SELECT nom_sre, promesa_serv FROM Servicios WHERE serv = %s", (servicio_1,))
        servicio_info_1 = cursor.fetchone()
        if servicio_info_1:
            nom_sre_1, promesa_serv_1 = servicio_info_1
            st.markdown(f"<div style='font-size: 12px;'>Ing. Sre.: {nom_sre_1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 12px;'>Promesa de Servicio: {promesa_serv_1}</div>", unsafe_allow_html=True)    
            st.markdown("<br>", unsafe_allow_html=True)  # Añadir espacio
            
    servicio_2 = st.selectbox("Selecciona el Servicio 2:", obtener_servicios(db_connection)) if cantidad_servicios > 1 else None

    # Mostrar Ing. Sre. y Promesa de Servicio para servicio_2
    if servicio_2:
        cursor.execute("SELECT nom_sre, promesa_serv FROM Servicios WHERE serv = %s", (servicio_2,))
        servicio_info_2 = cursor.fetchone()
        if servicio_info_2:
            nom_sre_2, promesa_serv_2 = servicio_info_2
            st.markdown(f"<div style='font-size: 12px;'>Ing. Sre.: {nom_sre_2}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 12px;'>Promesa de Servicio: {promesa_serv_2}</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)  # Añadir espacio
            
    descripcion_afectacion = st.text_input("Descripción de la Afectación:")
    hora_falla = st.time_input("Hora Falla:", value=None)

    if tipo_afectacion == 'Ok':
        fecha_falla = st.date_input("Fecha Falla:", value=None)
        hora_ok = st.time_input("Hora Ok:", value=None)
        fecha_ok = st.date_input("Fecha Ok:", value=None)
    
    causa = st.text_input("Causa:")
    solucion = st.text_input("Solución:") if tipo_afectacion == 'Ok' else None
    cantidad_avances = st.number_input("Cantidad de Avances:", min_value=1, max_value=20, value=1, step=1)

    avances = [st.text_input(f"Avance #{i + 1}:", key=f"avance_{i + 1}") for i in range(cantidad_avances)]
    avances_dict = {f"avance{i + 1}": (avances[i] if i < len(avances) else None) for i in range(20)}

    if st.button("Guardar"):
        guardar_notificacion(db_connection, tipo_afectacion, servicio_1, servicio_2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa, solucion, avances_dict)
        st.success("Datos guardados exitosamente")
        
    st.header('Notificar en el Chat GIOTI-ADMINISTRATIVO')
    st.markdown("### Servicio Afectado a Notificar:")
    iconos = {"Parcial": "⚠️", "Total": "❌", "Ok": "✅"}
    icono_seleccionado = iconos.get(tipo_afectacion, "")
    servicios_seleccionados = servicio_1 if cantidad_servicios == 1 else f"{servicio_1} - {servicio_2 or ''}"

    info = [
        f"{icono_seleccionado} {servicios_seleccionados}",
        f"{descripcion_afectacion}",
        f"Tipo de Falla: {tipo_afectacion}",
    ]
    
    if fecha_falla and hora_falla:
        info.append(f"Hora y Fecha Falla: {hora_falla.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.')} - {fecha_falla.strftime('%d-%m-%Y')}")
    elif fecha_falla:
        info.append(f"Fecha Falla: {fecha_falla.strftime('%d-%m-%Y')}")
    elif hora_falla:
        info.append(f"Hora Falla: {hora_falla.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.')}")

    if tipo_afectacion == 'Ok':
        if fecha_ok and hora_ok:
            info.append(f"Hora y Fecha Ok: {hora_ok.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.')} - {fecha_ok.strftime('%d-%m-%Y')}")
        elif fecha_ok:
            info.append(f"Fecha Ok: {fecha_ok.strftime('%d-%m-%Y')}")
        elif hora_ok:
            info.append(f"Hora Ok: {hora_ok.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.')}")
        info.append(f"Causa: {causa}")
        info.append(f"Solución: {solucion}")
    else:
        info.append(f"Causa: {causa}")

    for i in range(20, 0, -1):
        avance = avances_dict.get(f"avance{i}", None)
        if avance:
            info.append(f"Avance #{i}: {avance}")

    for line in info:
        st.markdown(line)

    # 🔹 Botón de copiar al portapapeles usando JavaScript
    notification_data = "\n".join(info)
    copy_button_html = f"""
        <script>
            function copiarAlPortapapeles() {{
                var textArea = document.createElement("textarea");
                textArea.value = `{notification_data}`;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand("copy");
                document.body.removeChild(textArea);
                
                // Mostrar el mensaje de copiado
                document.getElementById("mensaje-copiado").style.display = 'block';

                // Ocultar el mensaje después de 3 segundos
                setTimeout(function() {{
                    document.getElementById("mensaje-copiado").style.display = 'none';
                }}, 3000);
            }}
        </script>
        <div style="text-align: center; margin-top: 10px;">
            <button onclick="copiarAlPortapapeles()" style="padding: 10px 15px; font-size: 16px; border-radius: 5px; background-color: #4CAF50; color: white; border: none; cursor: pointer; font-family: 'Arial', sans-serif;">
                Copiar al Portapapeles
            </button>
        </div>
        <!-- Mensaje de confirmación que se mostrará después de copiar -->
        <div id="mensaje-copiado" style="display: none; background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 5px; font-size: 16px; margin-top: 10px; text-align: center; font-family: 'Arial', sans-serif;">
            Información copiada al portapapeles
        </div>
    """

    # Inyectar el HTML con el botón para copiar al portapapeles
    components.html(copy_button_html, height=250)

    notificaciones = obtener_notificaciones(db_connection)
    if notificaciones is not None:
        st.dataframe(notificaciones)

def obtener_servicios(db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT serv FROM gioti.servicios")
        results = cursor.fetchall()
        return [row[0] for row in results]
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return []

def obtener_ids_notificaciones(db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM notificaciones")
        results = cursor.fetchall()
        return [row[0] for row in results]
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return []

def guardar_notificacion(db_connection, tipo_afectacion, servicio_1, servicio_2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa, solucion, avances_dict):
    try:
        cursor = db_connection.cursor()
        query = """
        INSERT INTO notificaciones (tipo_afectacion, servicio_ok, servicios_afectados, servicios_afectados2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa_afectacion, solucion, avance20, avance19, avance18, avance17, avance16, avance15, avance14, avance13, avance12, avance11, avance10, avance9, avance8, avance7, avance6, avance5, avance4, avance3, avance2, avance1)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            tipo_afectacion, None, servicio_1, servicio_2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa, solucion,
            avances_dict['avance20'], avances_dict['avance19'], avances_dict['avance18'], avances_dict['avance17'], avances_dict['avance16'], avances_dict['avance15'], avances_dict['avance14'],
            avances_dict['avance13'], avances_dict['avance12'], avances_dict['avance11'], avances_dict['avance10'], avances_dict['avance9'], avances_dict['avance8'], avances_dict['avance7'],
            avances_dict['avance6'], avances_dict['avance5'], avances_dict['avance4'], avances_dict['avance3'], avances_dict['avance2'], avances_dict['avance1']
        )
        cursor.execute(query, values)
        db_connection.commit()
        cursor.close()
    except Error as e:
        st.error(f"Error al guardar los datos: {e}")

def editar_notificacion(db_connection):
    ids_notificaciones = obtener_ids_notificaciones(db_connection)
    id_notificacion_seleccionada = st.selectbox("Id de Notificación:", ids_notificaciones)

    if id_notificacion_seleccionada:
        notificacion = obtener_notificacion_por_id(db_connection, id_notificacion_seleccionada)
        if notificacion:
            tipo_afectacion = notificacion['tipo_afectacion']
            servicio_1 = notificacion['servicios_afectados']
            servicio_2 = notificacion['servicios_afectados2']
            descripcion_afectacion = notificacion['descripcion_afectacion']
            hora_falla = notificacion['hora_falla']
            fecha_falla = notificacion['fecha_falla']
            hora_ok = notificacion['hora_ok']
            fecha_ok = notificacion['fecha_ok']
            causa = notificacion['causa_afectacion']
            solucion = notificacion['solucion']
            avances_dict = {f"avance{i+1}": notificacion[f"avance{i+1}"] for i in range(20)}

            cantidad_servicios = st.number_input("Cantidad de Servicios Afectados (Max. 2)", min_value=1, max_value=2, value=2 if servicio_2 else 1, step=1)
            tipo_afectacion = st.selectbox("Selecciona el Tipo de Afectación:", ["Parcial", "Total", "Ok"], index=["Parcial", "Total", "Ok"].index(tipo_afectacion))
            
            servicio_1 = st.selectbox("Selecciona el Servicio 1:", obtener_servicios(db_connection), index=obtener_servicios(db_connection).index(servicio_1))
            
            # Mostrar Ing. Sre. y Promesa de Servicio para servicio_1
            if servicio_1:
                cursor = db_connection.cursor()
                cursor.execute("SELECT nom_sre, promesa_serv FROM Servicios WHERE serv = %s", (servicio_1,))
                servicio_info_1 = cursor.fetchone()
                if servicio_info_1:
                    nom_sre_1, promesa_serv_1 = servicio_info_1
                    st.markdown(f"<div style='font-size: 12px;'>Ing. Sre.: {nom_sre_1}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 12px;'>Promesa de Servicio: {promesa_serv_1}</div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espacio
            
            servicio_2 = st.selectbox("Selecciona el Servicio 2:", obtener_servicios(db_connection), index=obtener_servicios(db_connection).index(servicio_2) if servicio_2 else 0) if cantidad_servicios > 1 else None
            
            # Mostrar Ing. Sre. y Promesa de Servicio para servicio_2
            if servicio_2:
                cursor.execute("SELECT nom_sre, promesa_serv FROM Servicios WHERE serv = %s", (servicio_2,))
                servicio_info_2 = cursor.fetchone()
                if servicio_info_2:
                    nom_sre_2, promesa_serv_2 = servicio_info_2
                    st.markdown(f"<div style='font-size: 12px;'>Ing. Sre.: {nom_sre_2}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 12px;'>Promesa de Servicio: {promesa_serv_2}</div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espacio

            descripcion_afectacion = st.text_input("Descripción de la Afectación:", value=descripcion_afectacion)

            # Manejar hora_falla y hora_ok correctamente
            if isinstance(hora_falla, timedelta):
                hora_falla = (datetime.min + hora_falla).time()
            if isinstance(hora_ok, timedelta):
                hora_ok = (datetime.min + hora_ok).time()
                
            hora_falla = st.time_input("Hora Falla:", value=hora_falla)
            
            if tipo_afectacion == 'Ok':
                fecha_falla = st.date_input("Fecha Falla:", value=fecha_falla)
                hora_ok = st.time_input("Hora Ok:", value=hora_ok)
                fecha_ok = st.date_input("Fecha Ok:", value=fecha_ok)
                
            causa = st.text_input("Causa:", value=causa)
            solucion = st.text_input("Solución:", value=solucion) if tipo_afectacion == 'Ok' else None
            
            # Manejo de avances
            cantidad_avances = st.number_input(
                "Cantidad de Avances:", 
                min_value=1, 
                max_value=20, 
                value=max(1, len([av for av in avances_dict.values() if av])),  # Asegurar al menos 1 avance
                step=1
            )
            avances = [st.text_input(f"Avance #{i + 1}:", value=avances_dict[f"avance{i + 1}"], key=f"avance_{i + 1}") for i in range(cantidad_avances)]

            if st.button("Actualizar"):
                avances_dict = {f"avance{i + 1}": (avances[i] if i < len(avances) else None) for i in range(20)}

                actualizar_notificacion(db_connection, id_notificacion_seleccionada, tipo_afectacion, servicio_1, servicio_2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa, solucion, avances_dict)
                    
                st.success("Datos actualizados exitosamente")
                st.success("📢Recuerda modificar el campo de 'Descripción de la Afectación: ' Antes de enviar la notificación en estado OK")
                
            notificacion = obtener_notificacion_por_id(db_connection, id_notificacion_seleccionada)
            if notificacion:
                tipo_afectacion_db = notificacion['tipo_afectacion']
                
            # Mostrar los campos de la afectación
            st.header('Notificar en el Chat GIOTI-ADMINISTRATIVO')
            st.markdown("### Servicio Afectado a Notificar:")
            iconos = {"Parcial": "⚠️", "Total": "❌", "Ok": "✅"}
            icono_seleccionado = iconos.get(tipo_afectacion, "")
            servicios_seleccionados = servicio_1 if cantidad_servicios == 1 else f"{servicio_1} - {servicio_2 or ''}"

            info = [
                f"{icono_seleccionado} {servicios_seleccionados}",
                f"{descripcion_afectacion}",
                f"Tipo de Falla: {tipo_afectacion_db}",
            ]
            
            if fecha_falla and hora_falla:
                info.append(f"Hora y Fecha Falla: {hora_falla.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.')} - {fecha_falla.strftime('%d-%m-%Y')}")
            elif fecha_falla:
                info.append(f"Fecha Falla: {fecha_falla.strftime('%d-%m-%Y')}")
            elif hora_falla:
                info.append(f"Hora Falla: {hora_falla.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.')}")

            if tipo_afectacion == 'Ok':
                if fecha_ok and hora_ok:
                    info.append(f"Hora y Fecha Ok: {hora_ok.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.')} - {fecha_ok.strftime('%d-%m-%Y')}")
                elif fecha_ok:
                    info.append(f"Fecha Ok: {fecha_ok.strftime('%d-%m-%Y')}")
                elif hora_ok:
                    info.append(f"Hora Ok: {hora_ok.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.')}")
                info.append(f"Causa: {causa}")
                info.append(f"Solución: {solucion}")
            else:
                info.append(f"Causa: {causa}")

            for i in range(20, 0, -1):
                avance = avances_dict.get(f"avance{i}", None)
                if avance:
                    info.append(f"Avance #{i}: {avance}")

            for line in info:
                st.markdown(line)

            # 🔹 Botón de copiar al portapapeles usando JavaScript
            notification_data = "\n".join(info)
            copy_button_html = f"""
                <script>
                    function copiarAlPortapapeles() {{
                        var textArea = document.createElement("textarea");
                        textArea.value = `{notification_data}`;
                        document.body.appendChild(textArea);
                        textArea.select();
                        document.execCommand("copy");
                        document.body.removeChild(textArea);
                        
                        // Mostrar el mensaje de copiado
                        document.getElementById("mensaje-copiado").style.display = 'block';

                        // Ocultar el mensaje después de 3 segundos
                        setTimeout(function() {{
                            document.getElementById("mensaje-copiado").style.display = 'none';
                        }}, 3000);
                    }}
                </script>
                <div style="text-align: center; margin-top: 10px;">
                    <button onclick="copiarAlPortapapeles()" style="padding: 10px 15px; font-size: 16px; border-radius: 5px; background-color: #4CAF50; color: white; border: none; cursor: pointer; font-family: 'Arial', sans-serif;">
                        Copiar al Portapapeles
                    </button>
                </div>
                <!-- Mensaje de confirmación que se mostrará después de copiar -->
                <div id="mensaje-copiado" style="display: none; background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 5px; font-size: 16px; margin-top: 10px; text-align: center; font-family: 'Arial', sans-serif;">
                    Información copiada al portapapeles
                </div>
            """

            # Inyectar el HTML con el botón para copiar al portapapeles
            components.html(copy_button_html, height=250)
            
    # Mostrar el dataframe de notificaciones
    mostrar_notificaciones_guardadas(db_connection)
    
    
def obtener_servicios(db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT serv FROM gioti.servicios")
        results = cursor.fetchall()
        return [row[0] for row in results]
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return []

def obtener_ids_notificaciones(db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM notificaciones")
        results = cursor.fetchall()
        return [row[0] for row in results]
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return []

def guardar_notificacion(db_connection, tipo_afectacion, servicio_1, servicio_2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa, solucion, avances_dict):
    try:
        cursor = db_connection.cursor()
        query = """
        INSERT INTO notificaciones (tipo_afectacion, servicio_ok, servicios_afectados, servicios_afectados2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa_afectacion, solucion, avance20, avance19, avance18, avance17, avance16, avance15, avance14, avance13, avance12, avance11, avance10, avance9, avance8, avance7, avance6, avance5, avance4, avance3, avance2, avance1)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            tipo_afectacion, None, servicio_1, servicio_2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa, solucion,
            avances_dict['avance20'], avances_dict['avance19'], avances_dict['avance18'], avances_dict['avance17'], avances_dict['avance16'], avances_dict['avance15'], avances_dict['avance14'],
            avances_dict['avance13'], avances_dict['avance12'], avances_dict['avance11'], avances_dict['avance10'], avances_dict['avance9'], avances_dict['avance8'], avances_dict['avance7'],
            avances_dict['avance6'], avances_dict['avance5'], avances_dict['avance4'], avances_dict['avance3'], avances_dict['avance2'], avances_dict['avance1']
        )
        cursor.execute(query, values)
        db_connection.commit()
        cursor.close()
    except Error as e:
        st.error(f"Error al guardar los datos: {e}")

def obtener_notificacion_por_id(db_connection, id_notificacion):
    try:
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notificaciones WHERE id = %s", (id_notificacion,))
        return cursor.fetchone()
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None

def actualizar_notificacion(db_connection, id_notificacion, tipo_afectacion, servicio_1, servicio_2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa, solucion, avances_dict):
    try:
        cursor = db_connection.cursor()
        if (tipo_afectacion == 'Ok'):
            query = """
            UPDATE notificaciones
            SET servicio_ok = %s, servicios_afectados = %s, servicios_afectados2 = %s, descripcion_afectacion = %s, hora_falla = %s, fecha_falla = %s, hora_ok = %s, fecha_ok = %s, causa_afectacion = %s, solucion = %s, avance20 = %s, avance19 = %s, avance18 = %s, avance17 = %s, avance16 = %s, avance15 = %s, avance14 = %s, avance13 = %s, avance12 = %s, avance11 = %s, avance10 = %s, avance9 = %s, avance8 = %s, avance7 = %s, avance6 = %s, avance5 = %s, avance4 = %s, avance3 = %s, avance2 = %s, avance1 = %s
            WHERE id = %s
            """
            values = (
                tipo_afectacion, servicio_1, servicio_2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa, solucion,
                avances_dict['avance20'], avances_dict['avance19'], avances_dict['avance18'], avances_dict['avance17'], avances_dict['avance16'], avances_dict['avance15'], avances_dict['avance14'],
                avances_dict['avance13'], avances_dict['avance12'], avances_dict['avance11'], avances_dict['avance10'], avances_dict['avance9'], avances_dict['avance8'], avances_dict['avance7'],
                avances_dict['avance6'], avances_dict['avance5'], avances_dict['avance4'], avances_dict['avance3'], avances_dict['avance2'], avances_dict['avance1'],
                id_notificacion
            )
        else:
            query = """
            UPDATE notificaciones
            SET tipo_afectacion = %s, servicios_afectados = %s, servicios_afectados2 = %s, descripcion_afectacion = %s, hora_falla = %s, fecha_falla = %s, hora_ok = %s, fecha_ok = %s, causa_afectacion = %s, solucion = %s, avance20 = %s, avance19 = %s, avance18 = %s, avance17 = %s, avance16 = %s, avance15 = %s, avance14 = %s, avance13 = %s, avance12 = %s, avance11 = %s, avance10 = %s, avance9 = %s, avance8 = %s, avance7 = %s, avance6 = %s, avance5 = %s, avance4 = %s, avance3 = %s, avance2 = %s, avance1 = %s
            WHERE id = %s
            """
            values = (
                tipo_afectacion, servicio_1, servicio_2, descripcion_afectacion, hora_falla, fecha_falla, hora_ok, fecha_ok, causa, solucion,
                avances_dict['avance20'], avances_dict['avance19'], avances_dict['avance18'], avances_dict['avance17'], avances_dict['avance16'], avances_dict['avance15'], avances_dict['avance14'],
                avances_dict['avance13'], avances_dict['avance12'], avances_dict['avance11'], avances_dict['avance10'], avances_dict['avance9'], avances_dict['avance8'], avances_dict['avance7'],
                avances_dict['avance6'], avances_dict['avance5'], avances_dict['avance4'], avances_dict['avance3'], avances_dict['avance2'], avances_dict['avance1'],
                id_notificacion
            )
        cursor.execute(query, values)
        db_connection.commit()
        cursor.close()
    except Error as e:
        st.error(f"Error al actualizar los datos: {e}")
    
def eliminar_notificacion(db_connection):
    ids_notificaciones = obtener_ids_notificaciones(db_connection)
    id_notificacion_seleccionada = st.selectbox("Id de Notificación a Eliminar:", ids_notificaciones)

    mostrar_notificaciones_guardadas(db_connection)
    
    if st.button("Eliminar"):
        try:
            cursor = db_connection.cursor()
            cursor.execute("DELETE FROM notificaciones WHERE id = %s", (id_notificacion_seleccionada,))
            db_connection.commit()
            st.success("Notificación eliminada exitosamente")
        except Error as e:
            st.error(f"Error al eliminar los datos: {e}")

def obtener_notificaciones(db_connection):
    try:
        query = "SELECT * FROM notificaciones"
        cursor = db_connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        return pd.DataFrame(data, columns=columns)
    except Error as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None

def mostrar_notificaciones_guardadas(db_connection):
    notificaciones = obtener_notificaciones(db_connection)
    if notificaciones is not None:
        st.dataframe(notificaciones)

# if __name__ == "__main__":
    # Aquí se debe inicializar la conexión a la base de datos y llamar a la función main
   # pass