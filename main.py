import os
import sys
import webview
from flask import Flask, render_template

# Función para localizar la carpeta templates tanto en desarrollo como en el .exe compilado
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, 
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))

# Simulación de base de datos local de reportes / PQR para el aplicativo
historial_pqr = []

class Api:
    def login(self, correo, password):
        print(f"Intento de inicio de sesión con correo: {correo}")
        return {
            "success": True, 
            "nombre": "Juan David Hernández", 
            "direccion": "Carrera 7 # 15-30", 
            "barrio": "San Carlos", 
            "localidad": "Soacha"
        }
    
    def obtener_historial(self):
        return historial_pqr

    def radicar_pqr(self, descripcion, lat, lon):
        import datetime
        codigo_pqr = f"PQR-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
        nuevo_reporte = {
            "codigo": codigo_pqr,
            "descripcion": descripcion,
            "fecha": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            "lat": lat,
            "lon": lon
        }
        historial_pqr.append(nuevo_reporte)
        return {"success": True, "pqr": codigo_pqr}

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    api = Api()
    
    # Crear la ventana de escritorio con pywebview exponiendo la API
    window = webview.create_window(
        "Seguridad Vial - TRL 5", 
        app, 
        js_api=api,
        width=1280, 
        height=720, 
        min_size=(1024, 600)
    )
    
    # CORRECCIÓN AQUÍ: Se cambió 'private_storage' por 'private_mode'
    webview.start(private_mode=False)


