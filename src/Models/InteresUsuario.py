from __init__ import db

class InteresUsuario(db.Model):
    __tablename__ = 'intereses_usuario'
    id_interes = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria = db.Column(db.String(50), nullable=True)
    usuarios_id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
