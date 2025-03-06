import subprocess
import os

def run_streamlit():
    # Obtiene la ruta del script de Streamlit
    script_path = os.path.join(os.path.dirname(__file__), "principal.py")
    
    # Ejecuta la aplicación Streamlit
    subprocess.run(["streamlit", "run", script_path])

if __name__ == "__main__":
    run_streamlit()