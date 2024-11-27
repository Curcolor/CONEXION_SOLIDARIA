from datetime import datetime
from __init__ import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    contraseña = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    organizaciones = db.relationship('Organizacion', backref='usuario', lazy=True)
    intereses = db.relationship('InteresUsuario', backref='usuario', lazy=True)
    donaciones = db.relationship('Donacion', backref='usuario', lazy=True)