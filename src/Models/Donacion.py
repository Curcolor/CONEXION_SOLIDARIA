from datetime import datetime
from __init__ import db

class Donacion(db.Model):
    __tablename__ = 'donaciones'
    id_donacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    monto = db.Column(db.Float, nullable=False)
    fecha_donacion = db.Column(db.DateTime, default=datetime.utcnow)
    tipo_ayuda = db.Column(db.String(50))
    usuarios_id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    proyectos_id_proyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id_proyecto'), nullable=False)
