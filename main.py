import sqlite3
import os
import webview

class Api:
    def __init__(self):
        self.inicializar_base_datos()

    def inicializar_base_datos(self):
        """Crea la base de datos y las tablas si no existen."""
        conn = sqlite3.connect('seguridad_vial.db')
        cursor = conn.cursor()
        
        # Tabla de usuarios con cédula, correo (único) y contraseña
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                correo TEXT UNIQUE,
                cedula TEXT,
                edad TEXT,
                contrasena TEXT,
                direccion TEXT,
                barrio TEXT,
                localidad TEXT
            )
        ''')
        
        # Tabla de reportes / PQR
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reportes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                correo TEXT,
                descripcion TEXT,
                lat REAL,
                lon REAL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def registrar_usuario(self, nombre, correo, cedula, edad, contrasena, direccion, barrio, localidad):
        try:
            conn = sqlite3.connect('seguridad_vial.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO usuarios (nombre, correo, cedula, edad, contrasena, direccion, barrio, localidad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, correo, cedula, edad, contrasena, direccion, barrio, localidad))
            
            conn.commit()
            conn.close()
            return {"success": True, "message": "Usuario registrado con éxito."}
        except sqlite3.IntegrityError:
            return {"success": False, "message": "El correo electrónico ya se encuentra registrado."}
        except Exception as e:
            return {"success": False, "message": f"Error en el servidor: {str(e)}"}

    def login(self, correo, contrasena):
        try:
            conn = sqlite3.connect('seguridad_vial.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT nombre, correo, cedula, edad, direccion, barrio, localidad 
                FROM usuarios WHERE correo = ? AND contrasena = ?
            ''', (correo, contrasena))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "success": True,
                    "nombre": user[0],
                    "correo": user[1],
                    "cedula": user[2] if user[2] else "",
                    "edad": user[3],
                    "direccion": user[4],
                    "barrio": user[5],
                    "localidad": user[6]
                }
            else:
                return {"success": False, "message": "Correo o contraseña incorrectos."}
        except Exception as e:
            return {"success": False, "message": f"Error al iniciar sesión: {str(e)}"}

    def actualizar_usuario(self, correo_actual, nombre, cedula, edad, direccion, barrio, localidad):
        try:
            conn = sqlite3.connect('seguridad_vial.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE usuarios 
                SET nombre = ?, cedula = ?, edad = ?, direccion = ?, barrio = ?, localidad = ?
                WHERE correo = ?
            ''', (nombre, cedula, edad, direccion, barrio, localidad, correo_actual))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "usuario": {
                    "nombre": nombre,
                    "correo": correo_actual,
                    "cedula": cedula,
                    "edad": edad,
                    "direccion": direccion,
                    "barrio": barrio,
                    "localidad": localidad
                }
            }
        except Exception as e:
            print("Error al actualizar en BD:", e)
            return {"success": False, "message": "Error al actualizar en la base de datos."}

    def radicar_pqr(self, descripcion, lat, lon):
        try:
            conn = sqlite3.connect('seguridad_vial.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO reportes (correo, descripcion, lat, lon)
                VALUES (?, ?, ?, ?)
            ''', ("sistema", descripcion, lat, lon))
            
            pqr_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {"success": True, "pqr": f"PQR-{pqr_id:04d}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def obtener_historial(self):
        try:
            conn = sqlite3.connect('seguridad_vial.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT descripcion, lat, lon, fecha FROM reportes ORDER BY id DESC')
            filas = cursor.fetchall()
            conn.close()
            
            reportes = []
            for f in filas:
                reportes.append({
                    "descripcion": f[0],
                    "lat": f[1],
                    "lon": f[2],
                    "fecha": f[3]
                })
            return reportes
        except Exception as e:
            print("Error al obtener historial:", e)
            return []

if __name__ == '__main__':
    api = Api()
    
    # Asegúrate de que tu archivo HTML esté guardado en la carpeta 'templates/index.html'
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates', 'index.html'))
    
    window = webview.create_window(
        'Seguridad Vial - TRL 5',
        url=f'file://{html_path}',
        js_api=api,
        width=1150,
        height=700,
        resizable=True,
        min_size=(900, 600)
    )
    
    webview.start(debug=False)