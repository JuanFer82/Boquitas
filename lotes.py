import streamlit as st
from datetime import time
import streamlit.components.v1 as components

def main():
    # Selectbox para seleccionar el tipo de notificación
    tipo_notificacion = st.selectbox(
        "Selecciona un tipo de notificación:",
        [
            "🗣️ Lotes de Pago por la Sucursal Virtual Empresas Bancolombia",
            "✅ Lotes de Pago por la Sucursal Virtual Empresas Bancolombia",
        ],
    )

    # Campo para descripción de la afectación
    descripcion_afectacion = st.text_input("Descripción de la Afectación")

    # Hora y Fecha de Retención
    hora_inicio_retencion = st.time_input("Hora Inicio Retención:", value=None, key="hora_retencion")
    fecha_retencion = None
    if tipo_notificacion == "✅ Lotes de Pago por la Sucursal Virtual Empresas Bancolombia":
        fecha_retencion = st.date_input("Fechas de Retención:", value=None, key="fecha_retencion")

    # Hora y Fecha de Dosificación
    hora_inicio_dosificacion = st.time_input("Hora Inicio Dosificación:", value=None, key="hora_dosificacion")
    fecha_inicio_dosificacion = None
    if tipo_notificacion == "✅ Lotes de Pago por la Sucursal Virtual Empresas Bancolombia":
        fecha_inicio_dosificacion = st.date_input("Fecha Inicio Dosificación:", value=None, key="fecha_dosificacion")

    # Hora y Fecha OK
    hora_ok = None
    fecha_ok = None
    if tipo_notificacion == "✅ Lotes de Pago por la Sucursal Virtual Empresas Bancolombia":
        hora_ok = st.time_input("Hora OK:", value=None, key="hora_ok")
        fecha_ok = st.date_input("Fecha OK:", value=None, key="fecha_ok")

    # Campos para lotes
    lotes_retenidos = st.text_input("Lotes Retenidos:")
    lotes_procesados = st.text_input("Lotes Procesados:")
    lotes_fallidos = st.text_input("Lotes Fallidos:")
    dosificacion_lotes = st.text_input("Dosificación de Lotes por Minuto:")

    # Crear un string con los datos generados
    notification_data = ""
    notification_data += f"{tipo_notificacion}\n"
    notification_data += f"{descripcion_afectacion}\n"

    # Hora y Fecha Retención
    if hora_inicio_retencion and fecha_retencion:
        notification_data += f"Hora y Fecha Retención: {hora_inicio_retencion.strftime('%I:%M %p')} - {fecha_retencion.strftime('%d-%m-%Y')}\n"
    elif hora_inicio_retencion:
        notification_data += f"Hora Inicio Retención: {hora_inicio_retencion.strftime('%I:%M %p')}\n"

    # Hora y Fecha Dosificación
    if hora_inicio_dosificacion and fecha_inicio_dosificacion:
        notification_data += f"Hora y Fecha Inicio Dosificación: {hora_inicio_dosificacion.strftime('%I:%M %p')} - {fecha_inicio_dosificacion.strftime('%d-%m-%Y')}\n"
    elif hora_inicio_dosificacion:
        notification_data += f"Hora Inicio Dosificación: {hora_inicio_dosificacion.strftime('%I:%M %p')}\n"

    # Hora y Fecha OK
    if hora_ok and fecha_ok:
        notification_data += f"Hora y Fecha OK: {hora_ok.strftime('%I:%M %p')} - {fecha_ok.strftime('%d-%m-%Y')}\n"
    elif hora_ok:
        notification_data += f"Hora OK: {hora_ok.strftime('%I:%M %p')}\n"
    
    notification_data += f"Lotes Retenidos: {lotes_retenidos}\n"
    notification_data += f"Lotes Procesados: {lotes_procesados}\n"
    notification_data += f"Lotes Fallidos: {lotes_fallidos}\n"
    notification_data += f"Dosificación de Lotes por Minuto: {dosificacion_lotes}\n"

    # Mostrar la notificación sin el área de texto
    st.header('Notificar en el Chat GIOTI-ADMINISTRATIVO')
    st.markdown(notification_data.replace("\n", "  \n"))  # Mantiene el formato con saltos de línea

    # 🔹 Botón de copiar al portapapeles usando JavaScript
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

if __name__ == "__main__":
    main()
