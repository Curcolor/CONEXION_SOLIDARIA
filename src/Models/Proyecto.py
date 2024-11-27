from __init__ import db

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id_proyecto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    meta_financiera = db.Column(db.Float)
    monto_recaudado = db.Column(db.Float, default=0.00)
    categoria = db.Column(db.String(50))
    imagen_url = db.Column(db.String(255))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(20))
    organizaciones_id_organizacion = db.Column(db.Integer, db.ForeignKey('organizaciones.id_organizacion'), nullable=False)
