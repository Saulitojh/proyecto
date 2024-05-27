from flask import Blueprint, render_template, request, jsonify
from services.lastfm_service import buscar_informacion_cancion, obtener_canciones_similares

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/recomendar', methods=['POST'])
def recomendar():
    data = request.get_json()
    print("Datos recibidos:", data)  # Depuración
    if not data or 'canciones_favoritas' not in data:
        print("No se proporcionaron canciones favoritas")  # Depuración
        return jsonify({'error': 'No se proporcionaron canciones favoritas'}), 400
    
    canciones_favoritas = data.get('canciones_favoritas', [])
    print("Canciones favoritas:", canciones_favoritas)  # Depuración
    recomendaciones_finales = []
    
    for cancion in canciones_favoritas:
        try:
            nombre_cancion, nombre_artista = cancion.split(' - ')
            print(f"Buscando canciones similares para: {nombre_cancion} - {nombre_artista}")  # Depuración
            canciones_similares = obtener_canciones_similares(nombre_cancion, nombre_artista)
            if canciones_similares:
                recomendaciones_finales.extend(canciones_similares)
                print("Canciones similares encontradas:", canciones_similares)  # Depuración
        except ValueError:
            print(f"Formato incorrecto para la canción: {cancion}")  # Depuración
            return jsonify({'error': f'Formato incorrecto para la canción: {cancion}'}), 400

    # Eliminar duplicados en la lista final
    recomendaciones_unicas = []
    nombres_vistos = set()
    for recomendacion in recomendaciones_finales:
        if recomendacion['nombre'] not in nombres_vistos:
            recomendaciones_unicas.append(recomendacion)
            nombres_vistos.add(recomendacion['nombre'])

    print("Recomendaciones finales obtenidas:", recomendaciones_unicas)  # Depuración

    return jsonify(recomendaciones_unicas)
