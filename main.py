from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import instagrapi
from instagrapi import Client

import time
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



user = []
userid = []

now = datetime.datetime.now()
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
creddata = os.getenv("CRED_LOCATION")
firebase_url = os.getenv("FIREBASE_URL")

instagram_username = os.getenv("IG_ID")
instagram_password = os.getenv("IG_PW")

cred = credentials.Certificate(creddata)
firebase_admin.initialize_app(cred, {'databaseURL':firebase_url})





# Basic data
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

def post_instagram(api, image_path, track_name, artist_names, album_name, i):
    now = datetime.datetime.now()
    if now.hour == 0:
        thistime = "First"
    else:
        thistime = "Second"
    print("Uploading...")
    message = f"{artist_names} - {track_name}\nfrom the album {album_name}"
    api.photo_upload(image_path, f"{now.year}.{now.month}.{now.day} Today's {thistime} #{genre[i]}\n{message}")
    time.sleep(5)






track_name = [[] for _ in range(3)]
artists = [[] for _ in range(3)]
artist_names = [[] for _ in range(3)]
album_name = [[] for _ in range(3)]
album_image_url = [[] for _ in range(3)]

def download():
    global playlist_id, playlist_data, tracks, track_name, artists, artist_names, album_name, album_image_url

    track_name = [[] for _ in range(3)]
    artists = [[] for _ in range(3)]
    artist_names = [[] for _ in range(3)]
    album_name = [[] for _ in range(3)]
    album_image_url = [[] for _ in range(3)]

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
            image_path = f"album\\{genre[i]}_{idx}.jpg"

            with open(image_path, 'wb') as f:
                response = get(album_image_url[i][idx])
                f.write(response.content)
            
            print(f"{idx+1}. {track_name[i][-1]} - {artist_names[i][-1]}")

def upload(api):
    global count
    for i in range(3):
        selected_track_name = track_name[i][count]
        selected_artist_names = artist_names[i][count]
        selected_album_name = album_name[i][count]
        image_path = f"album\\{genre[i]}_{count}.jpg"
        post_instagram(api, image_path, selected_track_name, selected_artist_names, selected_album_name, i)
    count += 1
    dir = db.reference('')
    dir.update({'count',count})
    senddirect(api)

def senddirect(api):
    global now
    dir = db.reference('usercount')
    usercount = int(dir.get())

    for i in range(1, usercount+1):
        dir = db.reference(str(i))
        user.append(dir.get())
    for id in user:
        if id[0] == '\"':
            id = id[1:len(id)-1]
        userid.append(api.user_id_from_username(id))
    
    if now.hour>10:
        text= f"{now.month}월 {now.day}일 두 번째 플레이리스트가 업로드되었습니다. 확인해 보세요!"
    else:
        text= f"{now.month}월 {now.day}일 첫 번째 플레이리스트가 업로드되었습니다. 확인해 보세요!"
    
    for user_id in userid:
        api.direct_send(user_ids=[user_id], text=text)
        print(f"Direct Message Sent Successfully to {user_id}")






playlist_id = []
playlist_data = []
tracks = []
genre = ['Jazz', 'POP', 'EDM']

token = get_token()

playlist_id.append("6Il6PFSWjgjOU7PzA7w4GX")
playlist_id.append("47qCrjU2wU4YxN5Vh6yvpH")
playlist_id.append("60u1afVzJndAh2pS1Rxrd6")

dir = db.reference('count')
count = int(dir.get())
api = login_instagram(instagram_username, instagram_password)
print(count)
download()
while True:
    now = datetime.datetime.now()
    if now.hour == 5 and now.minute == 0:
        download()
        upload(api)
        print(f"{now.hour}:{now.minute}. Upload Completed")
        time.sleep(60)
    elif now.hour == 12 and now.minute == 00:
        upload(api)
        print(f"{now.hour}:{now.minute}. Upload Completed")
        time.sleep(60)
    elif now.hour == 0 and now.minute == 00:
        download()