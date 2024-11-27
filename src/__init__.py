from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from .Models.modelo_db import BaseDatos 

 # Importar la clase BaseDatos

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
    return app

