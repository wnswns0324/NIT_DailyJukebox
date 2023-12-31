import time
import datetime
import os

import firebase_admin
from firebase_admin import credentials, db

from envManager import *
from spotify import *
from instagram import *

now = datetime.datetime.now()
cred = credentials.Certificate(creddata)
firebase_admin.initialize_app(cred, {'databaseURL':firebase_url})

track_name = [[] for _ in range(3)]
artists = [[] for _ in range(3)]
artist_names = [[] for _ in range(3)]
album_name = [[] for _ in range(3)]
album_image_url = [[] for _ in range(3)]
preview_url = [[] for _ in range(3)]
image_path = [[] for _ in range(3)]



def download_song_data():
    global playlist_id, playlist_data, tracks, track_name, artists, artist_names, album_name, album_image_url, preview_url

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
            preview_url[i].append(track['track']['preview_url'])
            image_path[i].append(os.path.join("album", f"{genre[i]}_{idx}.jpg"))

            '''
            with open(image_path, 'wb') as f:
                response = get(album_image_url[i][idx])
                f.write(response.content)
            '''
                
            print(f"{idx+1}. {track_name[i][-1]} - {artist_names[i][-1]}")



def upload_instagram(api):
    global count
    post_instagram(api, image_path, track_name, artist_names, album_name, preview_url, count)
    count += 1
    dir = db.reference("")
    dir.update({'count':count})


playlist_id = ["6Il6PFSWjgjOU7PzA7w4GX", "47qCrjU2wU4YxN5Vh6yvpH", "60u1afVzJndAh2pS1Rxrd6"]
playlist_data = []
tracks = []
genre = ['Jazz', 'POP', 'EDM']

token = get_token()

dir = db.reference('count')
count = int(dir.get())
api = login_instagram(instagram_username, instagram_password)
print("logged in")
print(count)
download_song_data()

try:
    while True:
        now = datetime.datetime.now()
        if now.hour == 6 and now.minute == 0:
            upload_instagram(api)
            print(f"{now.hour}:{now.minute}. Upload Completed")
            time.sleep(60)

        if db.reference("cmd").get() == "upload_manual":
            db.reference("").update({"cmd":""})
            upload_instagram(api)
        elif db.reference("cmd").get() == "download_manual":
            db.reference("").update({"cmd":""})
            download_song_data()
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    api.logout()
    print("Logout Successful")