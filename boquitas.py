import streamlit as st
import streamlit.components.v1 as components

def main(db_connection):
    # Definición de opciones de notificación
    opciones_notificacion = [
        'Multiples Alertas',            
        'Tiempos de Respuesta',         
        'Disminución Transaccional',
        'Fuera de Promesa',
    ]

    # Mostrar el selectbox con las opciones de notificación
    seleccion_notificacion = st.selectbox(
        "Selecciona un tipo de notificación:",
        opciones_notificacion
    )

    # Definir el nombre de la columna según la selección de notificación
    columnas_notificacion = {
        'Multiples Alertas': 'multiples_alertas',
        'Tiempos de Respuesta': 'tiempos_respuesta',
        'Disminución Transaccional': 'disminucion_transaccional',
        'Fuera de Promesa': 'fuera_promesa'
    }
    columna_boquitas = columnas_notificacion.get(seleccion_notificacion)

    # Obtener datos de boquitas según la columna seleccionada, sin valores NULL o vacíos
    if columna_boquitas:
        cursor = db_connection.cursor()
        query = f"SELECT {columna_boquitas} FROM boquitas WHERE {columna_boquitas} IS NOT NULL AND {columna_boquitas} != ''"
        cursor.execute(query)
        boquitas_data = cursor.fetchall()
        opciones_boquitas = [item[0] for item in boquitas_data]

        if opciones_boquitas:  # Verifica si hay datos válidos
            seleccion_boquita = st.selectbox("Selecciona una Boquita:", opciones_boquitas)
        else:
            st.warning("No hay datos disponibles para esta notificación.")
            seleccion_boquita = None
    else:
        seleccion_boquita = None

    if seleccion_boquita:
        # Determinar el icono inicial según la selección de boquita
        if seleccion_boquita.startswith("Nos encontramos") or seleccion_boquita.startswith("Desde las"):
            icono_boquita = "🗣️"
        elif seleccion_boquita.startswith("Se presenta"):
            icono_boquita = "✅"
        elif seleccion_boquita.startswith("Se descarta"):
            icono_boquita = "✅"    
        else:
            icono_boquita = ""

        # Mostrar campos de tiempo si no es 'Multiples Alertas'
        if seleccion_notificacion != 'Multiples Alertas':
            if seleccion_boquita.startswith("Se presenta normalidad"):
                hora_inicial = st.time_input('Hora Inicial', key='hora_inicial', value=None)
                hora_final = st.time_input('Hora Final', key='hora_final', value=None)
            else:
                hora_inicial = None
                hora_final = None

            if seleccion_notificacion == 'Fuera de Promesa':
                hora_final = st.time_input("Hora Final:", value=None)
                incremento = 1
            else:
                incremento = st.number_input(
                    "Selecciona Cantidad de Servicios Alertados:",
                    min_value=1,
                    max_value=10,
                    value=1
                )
        else:
            hora_inicial = None
            hora_final = None
            incremento = st.number_input(
                "Selecciona Cantidad de Servicios Alertados:",
                min_value=1,
                max_value=10,
                value=1
            )

        # Consultar los servicios disponibles desde la base de datos
        cursor.execute("SELECT serv FROM Servicios")
        servicios_data = cursor.fetchall()
        opciones_servicios = [item[0] for item in servicios_data]

        # Lista para almacenar los servicios seleccionados e información adicional
        servicios_seleccionados = []

        # Mostrar dinámicamente los campos de selección de servicio e información adicional
        for i in range(incremento):
            st.subheader(f"Servicio {i+1}")
            seleccion_servicio = st.selectbox(
                f"Selecciona un Servicio Posiblemente Afectado {i+1}:",
                opciones_servicios
            )
            if seleccion_notificacion != 'Fuera de Promesa':
                informacion_adicional = st.text_input(f"Transacción Alertada {i+1}:")
                if informacion_adicional.strip():
                    servicios_seleccionados.append(f"{seleccion_servicio} ({informacion_adicional})")
                else:
                    servicios_seleccionados.append(f"{seleccion_servicio}")
            else:
                servicios_seleccionados.append(f"{seleccion_servicio}")

            # Obtener datos de la tabla servicios
            cursor.execute("SELECT nom_sre, promesa_serv FROM Servicios WHERE serv = %s", (seleccion_servicio,))
            servicio_info = cursor.fetchone()
            if servicio_info:
                nom_sre, promesa_serv = servicio_info
                # Mostrar como markdown para estilizar el texto
                st.markdown(f"<div style='font-size: 12px;'>Ing. Sre.: {nom_sre}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 12px;'>Promesa de Servicio: {promesa_serv}</div>", unsafe_allow_html=True)

        # Concatenar icono de notificación, icono de boquita y servicios seleccionados
        servicios_concatenados = ", ".join(servicios_seleccionados)

        # Reemplazar 'XXXXX' por servicios seleccionados, 'II:II' por hora inicial y 'FF:FF' por hora final en seleccion_boquita
        if seleccion_boquita:
            seleccion_boquita = seleccion_boquita.replace('XXXXX', servicios_concatenados)
            if hora_inicial:
                seleccion_boquita = seleccion_boquita.replace('II:II', hora_inicial.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.').lower())
            if hora_final:
                seleccion_boquita = seleccion_boquita.replace('FF:FF', hora_final.strftime('%I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.').lower())

        # Construir texto_concatenado según la selección de notificación y horas seleccionadas
        if seleccion_notificacion == 'Fuera de Promesa' and hora_final is not None:
            texto_concatenado = f"{icono_boquita} {seleccion_boquita}"
        elif seleccion_boquita.startswith("Se presenta normalidad") and hora_inicial is not None and hora_final is not None:
            texto_concatenado = f"{icono_boquita} {seleccion_boquita}"
        else:
            texto_concatenado = f"{icono_boquita} {seleccion_boquita} {servicios_concatenados}"

        # Mostrar el resultado concatenado
        st.header('Notificar en el Chat GIOTI-ADMINISTRATIVO')
        st.write(texto_concatenado)

        # 🔹 Botón de copiar al portapapeles usando JavaScript
        copy_button_html = f"""
            <script>
                function copiarAlPortapapeles() {{
                    var textArea = document.createElement("textarea");
                    textArea.value = `{texto_concatenado}`;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand("copy");
                    document.body.removeChild(textArea);
                    
                    // Actualizar el mensaje en la interfaz de usuario
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

        # Mostrar el botón de copiar
        components.html(copy_button_html, height=250)

if __name__ == "__main__":
    from principal import db_connection  # Se asume que la conexión está en principal.py
    main(db_connection)