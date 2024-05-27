from flask import Blueprint, render_template, request, jsonify, session
from services.lastfm_service import buscar_informacion_cancion, calcular_similitud, obtener_recomendaciones

bp = Blueprint('main', __name__)
PLAYLIST_SESSION_KEY = 'playlist'

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/recomendar', methods=['POST'])
def recomendar():
    data = request.get_json()
    if not data or 'canciones_favoritas' not in data:
        return jsonify({'error': 'No se proporcionaron canciones favoritas'}), 400

    canciones_favoritas = data.get('canciones_favoritas', [])
    if not isinstance(canciones_favoritas, list) or not all(isinstance(c, str) for c in canciones_favoritas):
        return jsonify({'error': 'El formato de canciones favoritas es incorrecto'}), 400

    canciones_info = []

    for cancion in canciones_favoritas:
        try:
            nombre_cancion, nombre_artista = cancion.split(' - ')
            info_cancion = buscar_informacion_cancion(nombre_cancion, nombre_artista)
            if info_cancion:
                canciones_info.append(info_cancion)
        except ValueError:
            return jsonify({'error': f'Formato incorrecto para la canción: {cancion}'}), 400
        except Exception as e:
            print(f"Error buscando información para la canción {cancion}: {str(e)}")
            continue  # Continuar con la siguiente canción en caso de error

    todas_las_canciones = cargar_todas_las_canciones()

    similitudes = calcular_similitud(canciones_info, todas_las_canciones)

    recomendaciones_finales = []
    for cancion_info in canciones_info:
        recomendaciones_finales.extend(obtener_recomendaciones(similitudes, num_recomendaciones=4))

    recomendaciones_unicas = []
    nombres_vistos = set()
    for recomendacion in recomendaciones_finales:
        if recomendacion['nombre'] not in nombres_vistos:
            recomendaciones_unicas.append(recomendacion)
            nombres_vistos.add(recomendacion['nombre'])

    # Guardar recomendaciones en la playlist de la sesión
    if PLAYLIST_SESSION_KEY not in session:
        session[PLAYLIST_SESSION_KEY] = []
    session[PLAYLIST_SESSION_KEY].extend(recomendaciones_unicas)
    session.modified = True

    return jsonify(recomendaciones_unicas)

@bp.route('/playlist')
def playlist():
    playlist = session.get(PLAYLIST_SESSION_KEY, [])
    return render_template('playlist.html', playlist=playlist)

def cargar_todas_las_canciones():
    # Ejemplo de carga de canciones desde un archivo JSON
    import json
    with open('data/songs.json', 'r') as f:
        return json.load(f)
