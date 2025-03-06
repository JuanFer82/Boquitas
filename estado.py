import streamlit as st

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