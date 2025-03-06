import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

def main(db_connection):
    def obtener_servicios():
        query = "SELECT serv FROM servicios"
        df = pd.read_sql(query, db_connection)
        return df['serv'].tolist()

    def obtener_canales():
        query = "SELECT serv, canal_servicio FROM servicios"
        df = pd.read_sql(query, db_connection)
        return df.set_index('serv')['canal_servicio'].to_dict()

    servicios = obtener_servicios()
    canal_servicio_dict = obtener_canales()

    if 'estado_texto' not in st.session_state:
        st.session_state.estado_texto = {
            "Canales Digitales": [],
            "Canales Físicos": [],
            "Malla de operación": [],
            "Filiales del Exterior": [],
            "Servicios PIC": [],
            "Sucursal Telefónica": [],
            "Otros": []
        }

    def limpiar_estado():
        st.session_state.estado_texto = {
            "Canales Digitales": [],
            "Canales Físicos": [],
            "Malla de operación": [],
            "Filiales del Exterior": [],
            "Servicios PIC": [],
            "Sucursal Telefónica": [],
            "Otros": []
        }

    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            selected_service = st.selectbox("Selecciona un Servicio", servicios, key='servicio_select')

            if st.button("Añadir al Estado de Servicios"):
                icono = "⚠️" if st.session_state.tipo_seleccion == "⚠️ Parcial" else "❌"
                canal_relacionado = canal_servicio_dict.get(selected_service)

                if canal_relacionado in st.session_state.estado_texto:
                    nuevo_estado = f"{icono} {selected_service}"
                    st.session_state.estado_texto[canal_relacionado].append(nuevo_estado)

        with col2:
            seleccion = st.radio("Selecciona el tipo:", ("⚠️ Parcial", "❌ Total"), index=0, key='tipo_seleccion')

        def obtener_icono(canal, servicios):
            if canal == "Malla de operación":
                if any(servicio.startswith("❌") for servicio in servicios):
                    return "❌"
                elif any(servicio.startswith("⚠️") for servicio in servicios):
                    return "⚠️"
            else:
                if servicios:
                    return "⚠️"
                else:
                    return "✅"

        estado_servicios_texto = "\n".join([
            f"{obtener_icono(canal, st.session_state.estado_texto[canal])} {canal}\n   " + "\n   ".join(st.session_state.estado_texto[canal]) if st.session_state.estado_texto[canal] else f"✅ {canal}"
            for canal in st.session_state.estado_texto
        ])

        estado_texto_area = st.text_area("**Estado de los Servicios:**", estado_servicios_texto, height=250, key='estado_texto_area')

        # 🔹 Estilos en CSS para los botones (Negro con letras blancas y alineados)
        st.markdown("""
            <style>
                .boton-container {
                    display: flex;
                    justify-content: space-between;
                    gap: 10px;
                    margin-top: 10px;
                }
                .stButton>button, .boton-copiar {
                    background-color: #000000 !important;
                    color: white !important;
                    border-radius: 8px !important;
                    padding: 10px 16px !important;
                    border: none !important;
                    font-size: 14px !important;
                    cursor: pointer;
                }
            </style>
        """, unsafe_allow_html=True)

        # 🔹 Botón de copiar al portapapeles usando JavaScript
        copy_button_html = f"""
            <script>
                function copiarAlPortapapeles() {{
                    var textArea = document.createElement("textarea");
                    textArea.value = `{estado_servicios_texto}`;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand("copy");
                    document.body.removeChild(textArea);
                    alert("Texto copiado al portapapeles!");
                }}
            </script>
            <div class="boton-container">
                <button onclick="copiarAlPortapapeles()" style="padding:10px 15px; font-size:16px; border-radius:5px; background-color:#000000; color:white; border:none; cursor:pointer;">
                    Copiar al Portapapeles
                </button>
            </div>
        """

        # 🔹 Alinear botones en la misma fila
        col_btn1, col_btn2 = st.columns([1, 1])

        with col_btn1:
            components.html(copy_button_html, height=50)

        with col_btn2:
            if st.button("Limpiar Estado de los Servicios"):
                limpiar_estado()
                st.rerun()
