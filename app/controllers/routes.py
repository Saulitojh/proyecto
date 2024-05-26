from flask import Blueprint, render_template, request, jsonify
from services.lastfm_service import buscar_informacion_cancion, calcular_similitud, obtener_recomendaciones

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
    canciones_info = []
    
    for cancion in canciones_favoritas:
        try:
            nombre_cancion, nombre_artista = cancion.split(' - ')
            print(f"Buscando información para: {nombre_cancion} - {nombre_artista}")  # Depuración
            info_cancion = buscar_informacion_cancion(nombre_cancion, nombre_artista)
            if info_cancion:
                canciones_info.append(info_cancion)
                print("Información de la canción encontrada:", info_cancion)  # Depuración
        except ValueError:
            print(f"Formato incorrecto para la canción: {cancion}")  # Depuración
            return jsonify({'error': f'Formato incorrecto para la canción: {cancion}'}), 400

    todas_las_canciones = [
        {'nombre': 'Song 1', 'artista': ['Artist A']},
        {'nombre': 'Song 2', 'artista': ['Artist B']},
        {'nombre': 'Song 3', 'artista': ['Artist C']},
        {'nombre': 'Song 4', 'artista': ['Artist D']},
        # Agrega aquí más canciones posibles para las recomendaciones
    ]

    print("Calculando similitudes...")  # Depuración
    similitudes = calcular_similitud(canciones_info, todas_las_canciones)
    print("Similitudes calculadas:", similitudes)  # Depuración

    # Obtener múltiples recomendaciones únicas
    recomendaciones_finales = []
    for cancion_info in canciones_info:
        recomendaciones_finales.extend(obtener_recomendaciones(similitudes, num_recomendaciones=4))

    # Eliminar duplicados en la lista final
    recomendaciones_unicas = []
    nombres_vistos = set()
    for recomendacion in recomendaciones_finales:
        if recomendacion['nombre'] not in nombres_vistos:
            recomendaciones_unicas.append(recomendacion)
            nombres_vistos.add(recomendacion['nombre'])

    print("Recomendaciones finales obtenidas:", recomendaciones_unicas)  # Depuración

    return jsonify(recomendaciones_unicas)