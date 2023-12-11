import instagrapi

import time
import datetime


def loginInstagrawm(username, password):
  print("Logging In...")
  api = instagrapi.Client()
  api.login(username, password)
  return api


def post_instagram(api, image_path, track_name, artist_names, album_name, genre):
  now = datetime.datetime.now()
  if now.hour == 0:
    thistime = "First"
  else:
    thistime = "Second"
  print("Uploading...")
  message = f"{artist_names} - {track_name}\nfrom the album {album_name}"
  api.photo_upload(
      image_path, f"{now.year}.{now.month}.{now.day} Today's {thistime} #{genre}\n{message}")
  time.sleep(5)
