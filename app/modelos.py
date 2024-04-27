# modelos.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cancion(db.Model):
    __tablename__ = 'canciones'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    artista = db.Column(db.String(100))
    genero = db.Column(db.String(50))

    def __repr__(self):
        return f"<Cancion {self.titulo}>"