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

def obtener_canciones_similares(nombre_cancion, nombre_artista, limit=10):
    """
    Obtiene una lista de canciones similares a una canción específica utilizando la API de Last.fm.
    """
    params = {
        'method': 'track.getsimilar',
        'artist': nombre_artista,
        'track': nombre_cancion,
        'api_key': API_KEY,
        'format': 'json',
        'limit': limit
    }

    response = requests.get(BASE_URL, params=params)
    print("Respuesta de Last.fm para canciones similares:", response.status_code, response.text)  # Depuración
    if response.status_code == 200:
        data = response.json()
        if 'similartracks' in data and 'track' in data['similartracks']:
            canciones_similares = []
            for track in data['similartracks']['track']:
                canciones_similares.append({
                    'nombre': track['name'],
                    'artista': [track['artist']['name']]
                })
            return canciones_similares
    return None
