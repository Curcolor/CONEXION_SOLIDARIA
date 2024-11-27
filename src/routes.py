from src import app, get_db
from flask import render_template, request, jsonify

@app.route('/')
@app.route('/src/templates/index.html')
def home():
    return render_template('index.html')

@app.route('/src/templates/pages/html/registro.html')
def registro():
    return render_template('pages/html/registro.html')

@app.route('/src/templates/pages/html/login.html')
def login():
    return render_template('pages/html/login.html')

@app.route('/src/templates/pages/html/donar.html')
def donar():
    return render_template('pages/html/donar.html')

@app.route('/src/templates/pages/html/perfil.html')
def perfil():
    return render_template('pages/html/perfil.html')

@app.route('/src/templates/pages/html/proyectos.html')
def proyectos():
    return render_template('pages/html/proyectos.html')

@app.route('/src/templates/pages/html/recibir.html')
def recibir():
    return render_template('pages/html/recibir.html')

@app.route('/src/templates/pages/html/nuevaOR.html', methods=['GET', 'POST'])
def nuevaOR():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario (en formato JSON)
            data = request.get_json()
            if not data:
                return jsonify({
                    "success": False, 
                    "message": "No se recibieron datos en formato JSON"
                })
            
            # Validar que los datos estén completos
            campos_requeridos = ["nombre", "descripcion", "categoria"]
            campos_faltantes = [campo for campo in campos_requeridos if not data.get(campo)]
            
            if campos_faltantes:
                return jsonify({
                    "success": False, 
                    "message": f"Faltan los siguientes campos: {', '.join(campos_faltantes)}"
                })

            # Obtener los valores del JSON
            nombre = data["nombre"]
            descripcion = data["descripcion"]
            categoria = data["categoria"]
            usuarios_id_usuario = 1  # Aquí pondrías el id del usuario logueado

            # Conectar a la base de datos
            try:
                conn = get_db()
                cursor = conn.cursor()

                query = """
                INSERT INTO organizaciones (nombre, descripcion, categoria, usuarios_id_usuario)
                VALUES (?, ?, ?, ?)
                """
                
                cursor.execute(query, (nombre, descripcion, categoria, usuarios_id_usuario))
                conn.commit()

            except Exception as db_error:
                return jsonify({
                    "success": False, 
                    "message": "Error al guardar en la base de datos",
                    "error": str(db_error)
                })
            
            finally:
                if 'conn' in locals():
                    conn.close()

            return jsonify({
                "success": True, 
                "message": "Organización registrada correctamente"
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Error inesperado en el servidor",
                "error": str(e)
            })
    
    return render_template('pages/html/nuevaOR.html')

@app.route('/src/templates/pages/html/organizaciones.html')
def organizaciones():
    return render_template('pages/html/organizaciones.html')

