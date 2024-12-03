from flask import render_template, request, jsonify

def routes(app):
    
    # PAGES ROUTES
    @app.route('/')
    @app.route('/inicio')
    def home():
        return render_template('index.html')

    @app.route('/registrarse')
    def registro():
        return render_template('pages/registro.html')
    
    @app.route('/iniciarSesion')
    def login():
        return render_template('pages/login.html')

    @app.route('/donar')
    def donar():
        return render_template('pages/donar.html')

    @app.route('/perfil')
    def perfil():
        return render_template('pages/perfil.html')

    @app.route('/proyectos')
    def proyectos():
        return render_template('pages/proyectos.html')

    @app.route('/recibir')
    def recibir():
        return render_template('pages/recibir.html')
    
    @app.route('/nuevoProyecto')
    def nuevoProyecto():
        return render_template('pages/nuevoProyecto.html')

    @app.route('/organizaciones')
    def organizaciones():
        return render_template('pages/organizaciones.html')
    
    @app.route('/nuevaOrganizacion')
    def nuevaOrganizacion():
        return render_template('pages/nuevaOR.html')
    
    
    # API ROUTES
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
            db = app.get_db()
                
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
                # Obtener el mensaje de error desde la base de datos
                return jsonify({
                    'success': False,
                    'error': db.ultimo_error if hasattr(db, 'ultimo_error') else 'Error al crear el usuario'
                }), 400

        except Exception as e:
            print(f"Error en el registro: {str(e)}")  # Para debugging
            return jsonify({'error': str(e)}), 500
   
    @app.route('/api/nuevaOR', methods=['GET', 'POST'])
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

                connection = app.get_db()
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
        
        return render_template('pages/nuevaOR.html')

    @app.route('/api/organizaciones', methods=['GET'])
    def obtener_organizaciones():
        try:
            connection = app.get_db()
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
            connection = app.get_db()
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
            connection = app.get_db()
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

    @app.route('/api/proyectos', methods=['GET', 'POST'])
    def crear_proyecto():
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
                campos_requeridos = ['titulo', 'meta_financiera', 'organizaciones_id_organizacion']
                for campo in campos_requeridos:
                    if not data.get(campo):
                        return jsonify({
                            "success": False, 
                            "message": f"El campo {campo} es obligatorio"
                        })

                connection = app.get_db()
                if not connection:
                    return jsonify({
                        "success": False,
                        "message": "No se pudo conectar a la base de datos"
                    })

                try:
                    cursor = connection.cursor()
                    
                    query = """
                    INSERT INTO proyectos (
                        titulo,
                        descripcion,
                        meta_financiera,
                        monto_recaudado,
                        categoria,
                        imagen_url,
                        fecha_inicio,
                        fecha_fin,
                        estado,
                        organizaciones_id_organizacion
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    valores = (
                        data.get('titulo'),
                        data.get('descripcion'),
                        float(data.get('meta_financiera')),
                        0.0,  # monto_recaudado inicial en 0
                        data.get('categoria'),
                        data.get('imagen_url'),
                        data.get('fecha_inicio'),
                        data.get('fecha_fin'),
                        data.get('estado'),
                        int(data.get('organizaciones_id_organizacion'))
                    )
                    print("Valores a insertar:", valores)  # Log para verificar valores
                    
                    cursor.execute(query, valores)
                    id_proyecto = cursor.lastrowid
                    print("ID generado:", id_proyecto)  # Log para verificar ID
                    
                    connection.commit()
                    
                    # Verificar si se insertó correctamente
                    cursor.execute("""
                        SELECT 
                            p.id_proyecto,
                            p.titulo,
                            p.descripcion,
                            p.meta_financiera,
                            p.monto_recaudado,
                            p.categoria,
                            p.imagen_url,
                            p.fecha_inicio,
                            p.fecha_fin,
                            p.estado,
                            o.nombre as organizacion_nombre
                        FROM proyectos p
                        JOIN organizaciones o ON p.organizaciones_id_organizacion = o.id_organizacion
                        WHERE p.id_proyecto = ?
                    """, (id_proyecto,))
                    
                    proyecto = cursor.fetchone()
                    
                    if proyecto:
                        return jsonify({
                            "success": True,
                            "message": "Proyecto creado correctamente",
                            "proyecto": {
                                "id": proyecto[0],
                                "titulo": proyecto[1],
                                "descripcion": proyecto[2],
                                "meta_financiera": float(proyecto[3]),
                                "monto_recaudado": float(proyecto[4]),
                                "categoria": proyecto[5],
                                "imagen_url": proyecto[6],
                                "fecha_inicio": proyecto[7],
                                "fecha_fin": proyecto[8],
                                "estado": proyecto[9],
                                "organizacion_nombre": proyecto[10]
                            }
                        })
                    else:
                        return jsonify({
                            "success": False,
                            "message": "El proyecto se creó pero no se pudo recuperar la información"
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
        
        # Si es GET, obtener todos los proyectos
        elif request.method == 'GET':
            try:
                connection = app.get_db()
                cursor = connection.cursor()
                
                cursor.execute("""
                    SELECT 
                        p.id_proyecto,
                        p.titulo,
                        p.descripcion,
                        p.meta_financiera,
                        p.monto_recaudado,
                        p.categoria,
                        p.imagen_url,
                        p.fecha_inicio,
                        p.fecha_fin,
                        p.estado,
                        o.nombre as organizacion_nombre
                    FROM proyectos p
                    JOIN organizaciones o ON p.organizaciones_id_organizacion = o.id_organizacion
                """)
                
                proyectos = cursor.fetchall()
                
                return jsonify({
                    "success": True,
                    "proyectos": [{
                        "id": p[0],
                        "titulo": p[1],
                        "descripcion": p[2],
                        "meta_financiera": float(p[3]),
                        "monto_recaudado": float(p[4]),
                        "categoria": p[5],
                        "imagen_url": p[6],
                        "fecha_inicio": p[7],
                        "fecha_fin": p[8],
                        "estado": p[9],
                        "organizacion_nombre": p[10]
                    } for p in proyectos]
                })
                
            except Exception as e:
                print("Error al obtener proyectos:", str(e))
                return jsonify({
                    "success": False,
                    "message": "Error al obtener los proyectos",
                    "error": str(e)
                }), 500
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

        return render_template('pages/nuevoProyecto.html')

