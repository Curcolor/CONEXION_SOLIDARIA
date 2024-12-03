from flask import Flask
from flask_cors import CORS
from .connection_db_debug import *

def create_app():
    app = Flask(__name__, static_url_path="/src/static/", static_folder="static")
    CORS(app)  # Permitir peticiones cross-origin
    
    # Registrar get_db como variable global de la app
    app.get_db = get_db
    
    # Importar las rutas aquí dentro para evitar la importación circular
    from .routes import routes
    routes(app)
    
    # Verificar la conexión a la base de datos - descomentar para verificar
    # check_database_connection()
    
    return app

