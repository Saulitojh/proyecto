# controladores.py
from .modelos import Cancion

def obtener_todas_las_canciones():
    return Cancion.query.all()

def obtener_cancion_por_id(id):
    return Cancion.query.get(id)