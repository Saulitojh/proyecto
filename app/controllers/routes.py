from flask import Blueprint, render_template, request
from services.lastfm_service import buscar_informacion_cancion, calcular_similitud, obtener_recomendaciones

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/recomendar', methods=['POST'])
def recomendar():
    canciones_favoritas = request.form.getlist('cancion')
    
    canciones_info = []
    for cancion in canciones_favoritas:
        nombre_cancion, nombre_artista = cancion.split(' - ')
        info_cancion = buscar_informacion_cancion(nombre_cancion, nombre_artista)
        if info_cancion:
            canciones_info.append(info_cancion)
    
    todas_las_canciones = [
        {'nombre': 'Song 1', 'artista': ['Artist A']},
        {'nombre': 'Song 2', 'artista': ['Artist B']},
        {'nombre': 'Song 3', 'artista': ['Artist C']},
        {'nombre': 'Song 4', 'artista': ['Artist D']},
    ]
    
    similitudes = calcular_similitud(canciones_info, todas_las_canciones)
    
    recomendaciones = obtener_recomendaciones(similitudes)
    
    return render_template('recomendaciones.html', recomendaciones=recomendaciones)