# vistas.py
from flask import render_template
from .controladores import obtener_todas_las_canciones, obtener_cancion_por_id

@app.route('/')
def index():
    canciones = obtener_todas_las_canciones()
    return render_template('index.html', canciones=canciones)

@app.route('/canciones/<int:id>')
def obtener_cancion_por_id_vista(id):
    cancion = obtener_cancion_por_id(id)
    if cancion:
        return render_template('detalle_cancion.html', cancion=cancion)
    else:
        return jsonify({'mensaje': 'Canción no encontrada'}), 404