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


playlist_id = []
playlist_data = []
tracks = []
genre = ['jazz', 'pop', 'edm']

instagram_username = "IG ID here"
instagram_password = "IG PW here"

if __name__ == "__main__":
    token = get_token()

    playlist_id.append("Your Playlist ID Here")
    playlist_id.append("Your Playlist ID Here")
    playlist_id.append("Your Playlist ID Here")

    
    index = int(input("Enter the index of the track you want to post on Instagram (1 to N): "))

    for i in range(3):
        print(f"Genre:{genre[i]}")
        playlist_data = get_songs_from_playlists(token, playlist_id[i])
        tracks = playlist_data['items']
        for idx, track in enumerate(tracks):
            track_name = track['track']['name']
            artists = track['track']['artists']
            artist_names = ', '.join([artist['name'] for artist in artists])
            album_name = track['track']['album']['name']
            album_image_url = track['track']['album']['images'][0]['url']
            image_path = f"{genre[i]}_{idx}.jpg"
            with open(image_path, 'wb') as f:
                response = get(album_image_url)
                f.write(response.content)

            print(f"{idx+1}. {track_name} - {artist_names}")

        if 1 <= index <= len(tracks):
            selected_track = tracks[index - 1]
            track_name = selected_track['track']['name']
            artists = selected_track['track']['artists']
            artist_names = ', '.join([artist['name'] for artist in artists])
            album_name = selected_track['track']['album']['name']
            album_image_url = selected_track['track']['album']['images'][0]['url']
            image_path = f"{genre[i]}_{index-1}.jpg"

            api = login_instagram(instagram_username, instagram_password)
            post_instagram_story(api, image_path, track_name, artist_names, album_name, i)
            logout_instagram(api)
            print("Instagram feed posted successfully!")
