from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import instagrapi
import time
import datetime

now = datetime.datetime.now()
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def get_songs_from_playlists(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def login_instagram(username, password):
    print("Logging In...")
    api = instagrapi.Client()
    api.login(username, password)
    return api

def logout_instagram(api):
    print("Logging Out...")
    api.logout()

def post_instagram_story(api, image_path, track_name, artist_names, album_name, i):
    print("Uploading...")
    message = f"Now playing: {artist_names} - {track_name}\nfrom the album {album_name}"
    api.photo_upload(image_path, f"{now.year}.{now.month}.{now.day} Today's #{genre[i]}\n{message}")
    time.sleep(5)



track_name = [[] for _ in range(3)]
artists = [[] for _ in range(3)]
artist_names = [[] for _ in range(3)]
album_name = [[] for _ in range(3)]
album_image_url = [[] for _ in range(3)]

def download():
    global playlist_id, playlist_data, tracks, track_name, artists, artist_names, album_name, album_image_url
    for i in range(3):
        print(f"Genre: {genre[i]}")
        playlist_data = get_songs_from_playlists(token, playlist_id[i])
        tracks = playlist_data['items']
        for idx, track in enumerate(tracks):
            track_name[i].append(track['track']['name'])
            artists[i].append(track['track']['artists'])
            artist_names[i].append(', '.join([artist['name'] for artist in track['track']['artists']]))
            album_name[i].append(track['track']['album']['name'])
            album_image_url[i].append(track['track']['album']['images'][0]['url'])
            image_path = f"{genre[i]}_{idx}.jpg"
            with open(image_path, 'wb') as f:
                response = get(album_image_url[i][idx])
                f.write(response.content)
            print(f"{idx+1}. {track_name[i][-1]} - {artist_names[i][-1]}")

def upload():
    global count
    api = login_instagram(instagram_username, instagram_password)
    for i in range(3):
        selected_track_name = track_name[i][count]
        selected_artists = artists[i][count]
        selected_artist_names = artist_names[i][count]
        selected_album_name = album_name[i][count]
        image_path = f"{genre[i]}_{count}.jpg"
        post_instagram_story(api, image_path, selected_track_name, selected_artist_names, selected_album_name, i)
    count += 1

playlist_id = []
playlist_data = []
tracks = []


genre = ['jazz', 'pop', 'edm']

instagram_username = "Instagram ID"
instagram_password = "Instagram PW"
token = get_token()

playlist_id.append("Playlist ID")
playlist_id.append("Playlist ID")
playlist_id.append("Playlist ID")

count = 0
download()
while True:
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0:
        upload()
        print(f"{now.hour}:{now.minute}. Upload Completed")
        time.sleep(60)
