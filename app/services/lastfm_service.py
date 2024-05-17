import requests

API_KEY = '36c3b174617c3d2c2da5188febf39980'

def buscar_informacion_cancion(nombre_cancion, nombre_artista):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'track.getInfo',
        'track': nombre_cancion,
        'artist': nombre_artista,
        'api_key': API_KEY,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        track_info = data.get('track', {})
        if track_info:
            info = {
                'nombre': track_info.get('name', 'Desconocido'),
                'artista': [track_info.get('artist', {}).get('name', 'Desconocido')],
                'album': track_info.get('album', {}).get('title', 'Desconocido'),
                'url': track_info.get('url', '#'),
            }
            return info
        else:
            return None
    else:
        return None

def calcular_similitud_entre_canciones(artistas_cancion1, cancion2):
    artistas_cancion2 = cancion2['artista']
    artistas_coincidentes = set(artistas_cancion1).intersection(artistas_cancion2)
    similitud = len(artistas_coincidentes) / len(artistas_cancion1) if len(artistas_cancion1) > 0 else 0
    return similitud

def calcular_similitud(canciones_favoritas, todas_las_canciones, num_recomendaciones=4):
    recomendaciones_por_cancion = {}
    for cancion_favorita in canciones_favoritas:
        artistas_cancion_favorita = cancion_favorita['artista']
        similitudes = []
        for otra_cancion in todas_las_canciones:
            if otra_cancion != cancion_favorita:
                similitud = calcular_similitud_entre_canciones(artistas_cancion_favorita, otra_cancion)
                similitudes.append((otra_cancion, similitud))
        similitudes = sorted(similitudes, key=lambda x: x[1], reverse=True)[:num_recomendaciones]
        recomendaciones_por_cancion[cancion_favorita['nombre']] = similitudes
    return recomendaciones_por_cancion

def obtener_recomendaciones(similitudes_por_cancion, num_recomendaciones=4):
    recomendaciones = {}
    for cancion, similitudes in similitudes_por_cancion.items():
        mejores_recomendaciones = [cancion_similar[0] for cancion_similar in similitudes[:num_recomendaciones]]
        recomendaciones[cancion] = mejores_recomendaciones
    return recomendaciones