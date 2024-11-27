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
            data = request.get_json()
            print("Datos recibidos:", data)  # Log para verificar los datos recibidos
            
            if not data:
                return jsonify({
                    "success": False, 
                    "message": "No se recibieron datos en formato JSON"
                })
            
            # Validar campos requeridos
            if not data.get("nombre"):
                return jsonify({
                    "success": False, 
                    "message": "El nombre es obligatorio"
                })

            connection = get_db()
            if not connection:
                return jsonify({
                    "success": False,
                    "message": "No se pudo conectar a la base de datos"
                })

            try:
                cursor = connection.cursor()
                
                # Verificar si la tabla existe y su estructura
                cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='organizaciones'")
                table_info = cursor.fetchone()
                print("Información de la tabla:", table_info)  # Log para verificar la tabla
                
                query = """
                INSERT INTO organizaciones (
                    nombre,
                    descripcion,
                    categoria,
                    imagen_url,
                    usuarios_id_usuario
                )
                VALUES (?, ?, ?, ?, ?)
                """
                
                valores = (
                    data.get('nombre'),
                    data.get('descripcion'),
                    data.get('categoria'),
                    data.get('imagen_url'),
                    1  # ID del usuario
                )
                print("Valores a insertar:", valores)  # Log para verificar valores
                
                cursor.execute(query, valores)
                id_organizacion = cursor.lastrowid  # Cambiamos para obtener el ID insertado
                print("ID generado:", id_organizacion)  # Log para verificar ID
                
                # Importante: Hacer commit antes de la consulta SELECT
                connection.commit()
                
                # Verificar si se insertó correctamente
                cursor.execute("SELECT * FROM organizaciones WHERE id_organizacion = ?", (id_organizacion,))
                verificacion = cursor.fetchone()
                print("Verificación de inserción:", verificacion)  # Log para verificar inserción
                
                if verificacion:
                    query_select = """
                    SELECT 
                        o.id_organizacion,
                        o.nombre,
                        o.descripcion,
                        o.categoria,
                        o.imagen_url,
                        o.fecha_registro,
                        u.nombre_completo as creador
                    FROM organizaciones o
                    JOIN usuarios u ON o.usuarios_id_usuario = u.id_usuario
                    WHERE o.id_organizacion = ?
                    """
                    
                    cursor.execute(query_select, (id_organizacion,))
                    organizacion = cursor.fetchone()
                    
                    if organizacion:
                        return jsonify({
                            "success": True,
                            "message": "Organización registrada correctamente",
                            "organizacion": {
                                "id": organizacion[0],
                                "nombre": organizacion[1],
                                "descripcion": organizacion[2],
                                "categoria": organizacion[3],
                                "imagen_url": organizacion[4],
                                "fecha_registro": organizacion[5],
                                "creador": organizacion[6]
                            }
                        })
                    else:
                        return jsonify({
                            "success": False,
                            "message": "La organización se creó pero no se pudo recuperar la información"
                        })
                else:
                    return jsonify({
                        "success": False,
                        "message": "No se pudo verificar la inserción de la organización"
                    })

            except Exception as e:
                print("Error en la base de datos:", str(e))  # Log del error
                return jsonify({
                    "success": False,
                    "message": "Error al guardar en la base de datos",
                    "error": str(e)
                })
            finally:
                cursor.close()
                connection.close()

        except Exception as e:
            print("Error inesperado:", str(e))  # Log del error
            return jsonify({
                "success": False,
                "message": "Error inesperado en el servidor",
                "error": str(e)
            })
    
    return render_template('pages/html/nuevaOR.html')

@app.route('/src/templates/pages/html/organizaciones.html')
def organizaciones():
    return render_template('pages/html/organizaciones.html')

@app.route('/src/templates/pages/html/update_files.html')
def update_files():
    return render_template('pages/html/update_files.html')

@app.route('/api/organizaciones', methods=['GET'])
def obtener_organizaciones():
    try:
        connection = get_db()
        cursor = connection.cursor()
        
        query = """
        SELECT 
            o.id_organizacion,
            o.nombre,
            o.descripcion,
            o.categoria,
            o.imagen_url,
            o.fecha_registro,
            u.nombre_completo as creador
        FROM organizaciones o
        JOIN usuarios u ON o.usuarios_id_usuario = u.id_usuario
        """
        
        cursor.execute(query)
        organizaciones = cursor.fetchall()
        
        # Convertir los resultados a una lista de diccionarios
        lista_organizaciones = [{
            "id": org[0],
            "nombre": org[1],
            "descripcion": org[2],
            "categoria": org[3],
            "imagen_url": org[4],
            "fecha_registro": org[5],
            "creador": org[6]
        } for org in organizaciones]
        
        return jsonify({
            "success": True,
            "organizaciones": lista_organizaciones
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error al obtener las organizaciones",
            "error": str(e)
        })
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/organizaciones/<int:id_organizacion>', methods=['DELETE'])
def borrar_organizacion(id_organizacion):
    try:
        connection = get_db()
        cursor = connection.cursor()
        
        # Verificar si la organización existe
        cursor.execute("SELECT * FROM organizaciones WHERE id_organizacion = ?", (id_organizacion,))
        organizacion = cursor.fetchone()
        
        if not organizacion:
            return jsonify({
                "success": False,
                "message": "La organización no existe"
            }), 404
        
        # Borrar la organización
        cursor.execute("DELETE FROM organizaciones WHERE id_organizacion = ?", (id_organizacion,))
        connection.commit()
        
        return jsonify({
            "success": True,
            "message": f"Organización {id_organizacion} eliminada correctamente"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error al eliminar la organización",
            "error": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/organizaciones/borrar-todo', methods=['DELETE'])
def borrar_todas_organizaciones():
    try:
        connection = get_db()
        cursor = connection.cursor()
        
        # Borrar todas las organizaciones
        cursor.execute("DELETE FROM organizaciones")
        connection.commit()
        
        return jsonify({
            "success": True,
            "message": "Todas las organizaciones han sido eliminadas"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error al eliminar las organizaciones",
            "error": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

