# -*- coding: utf-8 -*-
import pandas as pd
import requests
import json
import csv

username = "lovelypepa"
apikey = ""

# Obtener canales por usuario
url_channels = "https://www.googleapis.com/youtube/v3/channels?key="+apikey+"&forUsername="+username

response_channels = requests.get(url_channels)
data_channels = response_channels.json()

# Obtenemos el primer Id
channelid = data_channels['items'][0]['id']

# OBTENER TODOS LOS VIDEOS DE UN CANAL DE YOUTUBE
# Parámetros iniciales

API_KEY = "AIzaSyAZQTRMYxDQGIqU7Q5vnFezImkFiLe5FIU"
url = f"https://www.googleapis.com/youtube/v3/search"
all_videos = []

# Función para obtener videos
def get_all_videos():
    videos = []
    next_page_token = None
    params = {
        "part": "snippet,id",
        "channelId": channelid,
        "order": "date",
        "maxResults": 50, # Máximo permitido por la API
        "key": API_KEY,
        "type": "video"
        }
    while True:
        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(url, params=params)
        data = response.json()

        # Extraer videos
        for item in data['items']:
          videoid = item['id']['videoId']
          title = item['snippet']['title']
          date = item['snippet']['publishedAt']
          videos.append({
              "videoid": videoid,
              "title": title,
              "date": date
          })

        # Verificar si hay un nextPageToken para continuar
        next_page_token = data.get("nextPageToken")

        if not next_page_token: # Si no hay más páginas, detener el bucle
            break

    return videos

# Obtener los videos del canal actual
all_videos = get_all_videos()

print(f"Channel ID: {channelid} - Se obtuvieron {len(all_videos)} videos.")

# Mostramos todos los videos guardados en all_videos
print(f"En total se obtuvieron {len(all_videos)} videos en el canal.")

# Creamos un dataset con los videos, su título y fecha de publicación
df_video = pd.DataFrame(columns=('videoid', 'title','date'))
df_video = pd.DataFrame(all_videos)


# Obtener todos los comentarios de un video

# Parámetros iniciales

API_KEY = "AIzaSyAZQTRMYxDQGIqU7Q5vnFezImkFiLe5FIU"
url = f"https://www.googleapis.com/youtube/v3/commentThreads"
all_comments = []

# Función para obtener comentarios
def get_all_comments(video_id):
    comments = []
    next_page_token = None
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": 50, # Máximo permitido por la API
        "key": API_KEY
    }
    while True:
        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(url, params=params)
        data = response.json()
        # Extraer comentarios
        for item in data["items"]:
                  videoid = item['snippet']['videoId']
                  comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                  date = item['snippet']['topLevelComment']['snippet']['publishedAt']
                  comments.append({
                      "videoid": videoid,
                      "comment": comment,
                      "date": date
          })

        # Verificar si hay un nextPageToken para continuar
        next_page_token = data.get("nextPageToken")

        if not next_page_token: # Si no hay más páginas, detener el bucle
            break

    return comments

# Llamar a la función y obtener los comentarios
for video in all_videos:
    video_id = video['videoid'] # Extraer el ID del video
    comments = get_all_comments(video_id) # Obtener los comentarios del video actual
    all_comments.extend(comments) # Agregar los comentarios del video actual a la lista general
    print(f"Video ID: {video_id} - Se obtuvieron {len(comments)} comentarios.")

# Obtenemos todos los comentarios guardados en all_comments
print(f"En total se obtuvieron {len(all_comments)} comentarios de todos los videos.")

# Guardamos el resultado en un archivo

with open('VideoComments.json', 'w') as f:
   json.dump(all_comments, f, indent=4)

# Guardamos el archive como CSV
with open('VideoComments.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  for comment_data in all_comments:
    videoid = comment_data.get('videoid') # Obtener el videoid
    comment = comment_data.get('comment') # Obtener el comentario
    date = comment_data.get('date') # Obtener la fecha

    writer.writerow([videoid, comment, date])

print("Data saved to VideoComments.json and VideoComments.csv")

# Crear dataset para utilizar en el EDA

df = pd.DataFrame(columns=('videoid', 'comment','date'))
df = pd.DataFrame(all_comments)
