import streamlit as st
import base64
import mysql.connector
from boquitas import main as boquitas_main
import lotes
import notificaciones

st.set_page_config(
    page_title="Da Vinci",  # Nombre que aparecerá en la pestaña del navegador
    page_icon='C:/Users/Jufeguti/boquitas/logo.png'  # Ruta de la imagen del logo (favicon)
)

# Configuración de la conexión a la base de datos
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="gioti"
)

# Función para obtener la cadena base64 de un archivo binario para mostrar imagen de fondo
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Función para establecer el fondo de la aplicación
def imagen_fondo(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Función para establecer la imagen de Bancolombia en la parte inferior derecha
def imagen_bancolombia(png_file, width='300px', height='300px'):
    bin_str = get_base64_of_bin_file(png_file)
    bottom_right_img = f"""
    <style>
    .bottom-right {{
        position: fixed;
        bottom: 0;
        right: 0;
        width: {width};
        height: {height};
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: bottom right;
    }}
    </style>
    <div class="bottom-right"></div>
    """
    st.markdown(bottom_right_img, unsafe_allow_html=True)

# Establecer el fondo de pantalla y el logo de Bancolombia
imagen_fondo('C:/Users/Jufeguti/boquitas/fondo.png') # trazo.gif o circulo.gif
imagen_bancolombia('C:/Users/Jufeguti/boquitas//bancolombia.png')

# Imágenes y títulos correspondientes
IMAGE_PATH = 'C:/Users/Jufeguti/boquitas/davinci.png' # pc
IMAGE_PATH_BOQUITAS = 'C:/Users/Jufeguti/boquitas/boquita.png'
IMAGE_PATH_LOTES = 'C:/Users/Jufeguti/boquitas/lotes.png'
IMAGE_PATH_NOTIFICACION = 'C:/Users/Jufeguti/boquitas/notificacion.png'
IMAGE_PATH_MENU = 'C:/Users/Jufeguti/boquitas/menu.png'


# TITULO PRINCIPAL de la aplicación
col1, col2 = st.columns([8, 1])
with col1:
    st.title('Centro de Gestión y Monitoreo COES')
with col2:
    st.image(IMAGE_PATH, width=100)

# Layout de las columnas para los títulos y las imágenes
col1, col2 = st.columns([3, 1])

# Agregar imagen al menú lateral
st.sidebar.image(IMAGE_PATH_MENU)

# Título del menú lateral
st.sidebar.title("Menú")

# Opciones principales del menú
selected_option = st.sidebar.radio("Selecciona una opción:", ["Boquitas", "Lotes de Pago", "Notificación de Servicios"])

# Importar y ejecutar el formulario correspondiente
if selected_option == "Boquitas":
    with col1:
        st.title('Boquitas')
    with col2:
        st.image(IMAGE_PATH_BOQUITAS, width=70)
    boquitas_main(db_connection)
elif selected_option == "Lotes de Pago":
    with col1:
        st.title('Lotes de Pago')
    lotes.main()    
    with col2:
        st.image(IMAGE_PATH_LOTES, width=70)
elif selected_option == "Notificación de Servicios":
    with col1:
        st.title('Notificación de Servicios')
    with col2:
        st.image(IMAGE_PATH_NOTIFICACION, width=70)
    notificaciones.main(db_connection)
