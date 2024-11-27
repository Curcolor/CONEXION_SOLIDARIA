import sqlite3

class BaseDatos:
    def __init__(self, ruta_db="database/prueba.sqlite"):
        self.ruta_db = ruta_db
        self.inicializar_base_datos()

    def inicializar_base_datos(self):
        try:
            with self.get_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.executescript("""
                    PRAGMA foreign_keys = ON;

-- -----------------------------------------------------
-- Table usuarios
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre_completo TEXT NOT NULL,
  dni TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  telefono TEXT DEFAULT NULL,
  fecha_nacimiento DATE DEFAULT NULL,
  contraseña TEXT NOT NULL,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table organizaciones
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS organizaciones (
  id_organizacion INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  descripcion TEXT DEFAULT NULL,
  categoria TEXT DEFAULT NULL,
  imagen_url TEXT DEFAULT NULL,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  usuarios_id_usuario INTEGER NOT NULL,
  FOREIGN KEY (usuarios_id_usuario) REFERENCES usuarios (id_usuario) ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- -----------------------------------------------------
-- Table proyectos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS proyectos (
  id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  descripcion TEXT DEFAULT NULL,
  meta_financiera REAL DEFAULT NULL,
  monto_recaudado REAL DEFAULT 0.00,
  categoria TEXT DEFAULT NULL,
  imagen_url TEXT DEFAULT NULL,
  fecha_inicio DATE DEFAULT NULL,
  fecha_fin DATE DEFAULT NULL,
  estado TEXT DEFAULT NULL,
  organizaciones_id_organizacion INTEGER NOT NULL,
  FOREIGN KEY (organizaciones_id_organizacion) REFERENCES organizaciones (id_organizacion) ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- -----------------------------------------------------
-- Table donaciones
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS donaciones (
  id_donacion INTEGER PRIMARY KEY AUTOINCREMENT,
  monto REAL NOT NULL,
  fecha_donacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  tipo_ayuda TEXT DEFAULT NULL,
  usuarios_id_usuario INTEGER NOT NULL,
  proyectos_id_proyecto INTEGER NOT NULL,
  FOREIGN KEY (usuarios_id_usuario) REFERENCES usuarios (id_usuario) ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY (proyectos_id_proyecto) REFERENCES proyectos (id_proyecto) ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- -----------------------------------------------------
-- Table intereses_usuario
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intereses_usuario (
  id_interes INTEGER PRIMARY KEY AUTOINCREMENT,
  categoria TEXT DEFAULT NULL UNIQUE,
  usuarios_id_usuario INTEGER NOT NULL,
  FOREIGN KEY (usuarios_id_usuario) REFERENCES usuarios (id_usuario) ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- -----------------------------------------------------
-- Table solicitudes_ayuda
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS solicitudes_ayuda (
  id_solicitud INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  descripcion TEXT DEFAULT NULL,
  meta_financiera REAL DEFAULT NULL,
  imagen_url TEXT DEFAULT NULL,
  informacion_contacto TEXT DEFAULT NULL,
  estado TEXT DEFAULT NULL,
  fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  usuarios_id_usuario INTEGER NOT NULL,
  FOREIGN KEY (usuarios_id_usuario) REFERENCES usuarios (id_usuario) ON DELETE NO ACTION ON UPDATE NO ACTION
);
                """)
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")

    def get_conexion(self):
        try:
            return sqlite3.connect(self.ruta_db)
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    # Ejemplo de insertar usuario
    def crear_usuario(
        self, nombre_completo, dni, email, telefono, fecha_nacimiento, contraseña
    ):
        try:
            with self.get_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    INSERT INTO usuarios (nombre_completo, dni, email, telefono, fecha_nacimiento, contraseña)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        nombre_completo,
                        dni,
                        email,
                        telefono,
                        fecha_nacimiento,
                        contraseña,
                    ),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al crear usuario: {e}")
            return None

    # Ejemplo de buscar usuario
    def buscar_usuario_por_email(self, email):
        try:
            with self.get_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al buscar usuario: {e}")
            return None

    # Ejemplo de crear organización
    def crear_organizacion(
        self, nombre, descripcion, categoria, imagen_url, usuario_id
    ):
        try:
            with self.get_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    INSERT INTO organizaciones (nombre, descripcion, categoria, imagen_url, usuarios_id_usuario)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (nombre, descripcion, categoria, imagen_url, usuario_id),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al crear organización: {e}")
            return None

    # Ejemplo de crear proyecto
    def crear_proyecto(
        self,
        titulo,
        descripcion,
        meta_financiera,
        categoria,
        imagen_url,
        fecha_inicio,
        fecha_fin,
        estado,
        organizacion_id,
    ):
        try:
            with self.get_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    INSERT INTO proyectos (titulo, descripcion, meta_financiera, categoria, 
                    imagen_url, fecha_inicio, fecha_fin, estado, organizaciones_id_organizacion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        titulo,
                        descripcion,
                        meta_financiera,
                        categoria,
                        imagen_url,
                        fecha_inicio,
                        fecha_fin,
                        estado,
                        organizacion_id,
                    ),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al crear proyecto: {e}")
            return None

    # Ejemplo de registrar donación
    def registrar_donacion(self, monto, tipo_ayuda, usuario_id, proyecto_id):
        try:
            with self.get_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    INSERT INTO donaciones (monto, tipo_ayuda, usuarios_id_usuario, proyectos_id_proyecto)
                    VALUES (?, ?, ?, ?)
                """,
                    (monto, tipo_ayuda, usuario_id, proyecto_id),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al registrar donación: {e}")
            return None

    def actualizar_imagen_organizacion(self, organizacion_id, imagen_url):
        try:
            with self.get_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    UPDATE organizaciones 
                    SET imagen_url = ? 
                    WHERE id_organizacion = ?
                """,
                    (imagen_url, organizacion_id),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar imagen de organización: {e}")
            return False

    def actualizar_imagen_proyecto(self, proyecto_id, imagen_url):
        try:
            with self.get_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    UPDATE proyectos 
                    SET imagen_url = ? 
                    WHERE id_proyecto = ?
                """,
                    (imagen_url, proyecto_id),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar imagen de proyecto: {e}")
            return False

    def actualizar_imagen_solicitud(self, solicitud_id, imagen_url):
        try:
            with self.get_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    UPDATE solicitudes_ayuda 
                    SET imagen_url = ? 
                    WHERE id_solicitud = ?
                """,
                    (imagen_url, solicitud_id),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar imagen de solicitud: {e}")
            return False


# Ejemplo de uso
if __name__ == "__main__":
    db = BaseDatos()

    # Ejemplo de crear un usuario
    usuario_id = db.crear_usuario(
        nombre_completo="Juan Pérez",
        dni="12345678",
        email="juan@ejemplo.com",
        telefono="123456789",
        fecha_nacimiento="1990-01-01",
        contraseña="contraseña123",
    )

    if usuario_id:
        print(f"Usuario creado con ID: {usuario_id}")

        # Crear una organización para el usuario
        org_id = db.crear_organizacion(
            nombre="ONG Ejemplo",
            descripcion="Una organización de ejemplo",
            categoria="Social",
            imagen_url=None,  # Inicialmente sin imagen
            usuario_id=usuario_id,
        )

        if org_id:
            print(f"Organización creada con ID: {org_id}")

            # Actualizar la imagen de la organización
            imagen_url = "/static/uploads/1234567890_imagen.jpg"
            if db.actualizar_imagen_organizacion(org_id, imagen_url):
                print(f"Imagen actualizada: {imagen_url}")
