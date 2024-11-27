from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from .Models.modelo_db import BaseDatos 
from flask_sqlalchemy import SQLAlchemy  # Importar SQLAlchemy
import sqlite3
 # Importar la clase BaseDatos

 # Configuración de la base de datos SQLite
DATABASE = 'donaciones.sqlite'

# Función para obtener la conexión a la base de datos
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn

def check_database_connection():
    """Función para verificar la conexión y estructura de la base de datos"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Obtener todas las tablas de la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        
        # Obtener información detallada de cada tabla
        info_tablas = {}
        for tabla in tablas:
            nombre_tabla = tabla[0]
            cursor.execute(f"PRAGMA table_info({nombre_tabla})")
            columnas = cursor.fetchall()
            info_tablas[nombre_tabla] = [
                {
                    "nombre": col[1],
                    "tipo": col[2],
                    "nullable": not col[3],
                    "pk": col[5]
                } for col in columnas
            ]
        
        # Preparar el mensaje de respuesta
        mensaje = {
            "status": "Conexión exitosa",
            "database_path": conn.path if hasattr(conn, 'path') else "SQLite database",
            "tablas_encontradas": len(tablas),
            "detalle_tablas": info_tablas
        }
        
        # Imprimir en consola para debug
        print("\n=== INFORMACIÓN DE LA BASE DE DATOS ===")
        print(f"Estado: {mensaje['status']}")
        print(f"Base de datos: {mensaje['database_path']}")
        print(f"Número de tablas: {mensaje['tablas_encontradas']}")
        print("\nTablas encontradas:")
        for nombre_tabla, columnas in info_tablas.items():
            print(f"\n{nombre_tabla}:")
            for columna in columnas:
                print(f"  - {columna['nombre']} ({columna['tipo']})")
                print(f"    Nullable: {columna['nullable']}, Primary Key: {columna['pk']}")
        
        return mensaje
        
    except Exception as e:
        error_mensaje = {
            "status": "Error de conexión",
            "error": str(e)
        }
        print("\n=== ERROR EN LA BASE DE DATOS ===")
        print(f"Error: {str(e)}")
        return error_mensaje
    
    finally:
        if 'conn' in locals():
            conn.close()

app = Flask(__name__,static_url_path='/src/static/', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donaciones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Crear instancia de SQLAlchemy
app = Flask(
        __name__, static_url_path="/src/static/", static_folder="static"
    )
CORS(app)  # Permitir peticiones cross-origin
db = BaseDatos()  # Crear instancia de la base de datos

from src.routes import *

def create_app():

    # Configuración del servidor
    UPLOAD_FOLDER = 'src/static/uploads/'  # Cambiamos la ruta para mejor organización
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No se seleccionó un archivo"}), 400

        if file and allowed_file(file.filename):
            # Crear nombre único para el archivo
            import time
            filename = f"{int(time.time())}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Crear URL relativa del archivo
            url_imagen = f'/static/uploads/{filename}'

            # Si se proporciona ID de organización, proyecto o solicitud, actualizar la URL
            if 'organizacion_id' in request.form:
                org_id = int(request.form['organizacion_id'])
                db.actualizar_imagen_organizacion(org_id, url_imagen)
            elif 'proyecto_id' in request.form:
                proyecto_id = int(request.form['proyecto_id'])
                db.actualizar_imagen_proyecto(proyecto_id, url_imagen)
            elif 'solicitud_id' in request.form:
                solicitud_id = int(request.form['solicitud_id'])
                db.actualizar_imagen_solicitud(solicitud_id, url_imagen)

            return jsonify({
                "message": "Archivo subido exitosamente",
                "url": url_imagen
            }), 200
        else:
            return jsonify({"error": "Extensión no permitida"}), 400
        

    @app.route('/api/registro', methods=['POST'])
    def registro_usuario():
        try:
            datos = request.get_json()
            
            # Verificar que todos los campos necesarios estén presentes
            campos_requeridos = ['nombre_completo', 'dni', 'email', 'telefono', 'fecha_nacimiento', 'contraseña']
            for campo in campos_requeridos:
                if campo not in datos:
                    return jsonify({'error': f'Falta el campo {campo}'}), 400

            # Crear instancia de la base de datos
            db = BaseDatos()
            
            # Llamar al método crear_usuario con todos los parámetros requeridos
            usuario_id = db.crear_usuario(
                nombre_completo=datos['nombre_completo'],
                dni=datos['dni'],
                email=datos['email'],
                telefono=datos['telefono'],
                fecha_nacimiento=datos['fecha_nacimiento'],
                contraseña=datos['contraseña']
            )

            if usuario_id:
                return jsonify({
                    'success': True,
                    'mensaje': 'Usuario registrado exitosamente',
                    'usuario_id': usuario_id
                })
            else:
                return jsonify({'error': 'Error al crear el usuario'}), 400

        except Exception as e:
            print(f"Error en el registro: {str(e)}")  # Para debugging
            return jsonify({'error': str(e)}), 500

    return app

# Puedes llamar a la función durante la inicialización de la app
check_database_connection()

