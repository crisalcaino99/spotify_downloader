from pytube import YouTube
from pydub import AudioSegment
import os
from unidecode import unidecode
import csv
from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

def isalnumspace(letter):
    if letter.isalnum():
        return True
    elif letter == " ":
        return True
    else:
        return False
# La siguiente funcion descarga un video segun una URL en mp3
def descargar_youtube_mp3(url, output_path = ""):
    # Descargar video de Youtube
    yt = YouTube(url)
    yt.title = unidecode(yt.title)
    yt.title = "".join(e for e in yt.title if isalnumspace(e))
    yt.title = yt.title.replace("'", "")
    video = yt.streams.filter(only_audio=True).first()
    video.download(output_path)
    # Convertir video a formato mp3
    name = unidecode(yt.title)
    name = "".join(e for e in name if isalnumspace(e))
    name = name.replace("'", "")
    print(name)
    video_path = os.path.join(output_path, f"{name}.mp4")
    print(f"{name}")
    audio = AudioSegment.from_file(video_path, format="mp4")
    mp3_path = os.path.join(output_path, f"{name}.mp3")
    audio.export(mp3_path, format="mp3")
    # Eliminar el archivo de video original
    os.remove(video_path)
    print("success")

# Aqui buscaremos el mejor video
def buscar_youtube_video(api_key, query, order_by = "viewCount"):
    youtube = build("youtube", "v3", developerKey = api_key)
    # Realizar la búsqueda:
    search_response = youtube.search().list(
        q = query,
        part = 'id',
        type = 'video', 
        order = 'relevance',
        maxResults = 1
    ).execute()
    # Obtener ID del video:
    print("Search Response:", search_response)
    video_id = search_response['items'][0]['id']['videoId']
    # Obtener la URL del video usando pytube
    url = f'https://www.youtube.com/watch?v={video_id}'
    print(url)
    return url

# Extraer una playlist de Spotify (pendiente)
def exportar_a_csv(username, playlist_id, client_id, client_secret, csv_filename):
    # Configurar las credenciales de la aplicación
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # Obtener info de la playlist
    playlist = sp.user_playlist_tracks(username, playlist_id)
    # Escribir sobre una playlist
    # Extraer info sobre cada pista:
    with open(csv_filename, "w", newline= '', encoding = "utf-8") as csvfile:
        fieldnames = ["Canción", "Artista"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Escribir la fila de encabezado (?):
        writer.writeheader()
        # Escribir info sobre cada pista
        for track in playlist["items"]:
            nombre_cancion = track["track"]["name"]
            artista = track["track"]["artists"][0]["name"]
            # Escribir la info de la pista en el CSV:
            writer.writerow({'Canción': nombre_cancion, 'Artista': artista})
    
    return print("exportacion de playlist exitosa")

keys = {"client_id_sp": "767bf032d25042e0a2246f1c10ebf0d7",
        "client_secret_sp": "655f4fc8750a4d1db6f0d75244facbb1",
        "yt_key": "AIzaSyCm1u1fiNxltO0IJhSTKJXgEUctOJSz5X4",
        "username": "cristobal_a91"}

def show_playlists(username, client_id, client_secret):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost:8888/callback/", scope='user-library-read'))
    playlists = []
    offset = 0
    while True:
        result = sp.user_playlists(username, limit=50, offset=offset)
        playlists.extend(result['items'])
        # Verifica si hay más playlists
        if not result['next']:
            break
        # Actualiza el offset para la próxima página
        offset += 50
    return [{"name": playlist['name'], "id": playlist['id']} for playlist in playlists]

def ver_playlists(user_input):
    client_id = keys["client_id_sp"]
    client_secret = keys["client_secret_sp"]
    return show_playlists(user_input, client_id, client_secret)

def watch_playlists():
    client_id = keys["client_id_sp"]
    client_secret = keys["client_secret_sp"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost:8888/callback/", scope='user-library-read'))
    return sp.current_user_playlists()

def ver_playlist_detallada(playlist_id):
    client_id = keys["client_id_sp"]
    client_secret = keys["client_secret_sp"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost:8888/callback/", scope='user-library-read'))
    return sp.playlist(playlist_id)

