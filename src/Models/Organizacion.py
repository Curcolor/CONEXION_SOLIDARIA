from datetime import datetime
from __init__ import db

class Organizacion(db.Model):
    __tablename__ = 'organizaciones'
    id_organizacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(50))
    imagen_url = db.Column(db.String(255))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    usuarios_id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

    proyectos = db.relationship('Proyecto', backref='organizacion', lazy=True)