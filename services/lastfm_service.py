import requests
import random

API_KEY = '36c3b174617c3d2c2da5188febf39980'  # Reemplaza esto con tu API key de Last.fm
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

def buscar_informacion_cancion(nombre_cancion, nombre_artista):
    """
    Busca información de una canción específica utilizando la API de Last.fm.
    """
    params = {
        'method': 'track.getInfo',
        'api_key': API_KEY,
        'artist': nombre_artista,
        'track': nombre_cancion,
        'format': 'json'
    }

    response = requests.get(BASE_URL, params=params)
    print("Respuesta de Last.fm:", response.status_code, response.text)  # Depuración
    if response.status_code == 200:
        data = response.json()
        if 'track' in data:
            return {
                'nombre': data['track']['name'],
                'artista': [data['track']['artist']['name']]
            }
    return None

def calcular_similitud(canciones_info, todas_las_canciones):
    """
    Calcula la similitud entre las canciones favoritas del usuario y una lista de todas las canciones disponibles.
    """
    similitudes = []

    for cancion_info in canciones_info:
        for cancion in todas_las_canciones:
            similitud = some_similarity_metric(cancion_info, cancion)
            similitudes.append({
                'nombre': cancion['nombre'],
                'artista': cancion['artista'],
                'similitud': similitud
            })

    return similitudes

def some_similarity_metric(cancion_info, cancion):
    """
    Métrica simple de similitud entre dos canciones. En este ejemplo, se utiliza un valor aleatorio.
    """
    return random.random()

def obtener_recomendaciones(similitudes, num_recomendaciones=4):
    """
    Ordena las canciones por similitud y devuelve recomendaciones únicas.
    """
    recomendaciones_ordenadas = sorted(similitudes, key=lambda x: x['similitud'], reverse=True)
    recomendaciones_unicas = []
    nombres_vistos = set()

    for recomendacion in recomendaciones_ordenadas:
        if len(recomendaciones_unicas) >= num_recomendaciones:
            break
        if recomendacion['nombre'] not in nombres_vistos:
            recomendaciones_unicas.append(recomendacion)
            nombres_vistos.add(recomendacion['nombre'])

    return recomendaciones_unicas