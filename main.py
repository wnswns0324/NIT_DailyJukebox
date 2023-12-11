from requests import get

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import datetime
import threading

from instagram import loginInstagrawm, post_instagram
from env import creddata, firebase_url, instagram_password, instagram_username
from spotify import getSpotifyToken, getSongsFromPlaylists


class Track:
  def __init__(self, name, artistNames, albumName, albumImageURL, imagePath):
    self.name = name
    self.artistNames = artistNames
    self.albumName = albumName
    self.albumImageURL = albumImageURL
    self.imagePath = imagePath


def downlodAlbums(playlistIDs):
  genreTracks = []

  for genreIndex, currentGenre in enumerate(genre):
    genreTracks.append([])

    print(f"Genre: {currentGenre}")

    playlistData = getSongsFromPlaylists(token, playlistIDs[genreIndex])
    tracks = playlistData['items']

    for trackIndex, track in enumerate(tracks):
      trackName = track['track']['name']
      artistNames = ', '.join([artist['name']
                              for artist in track['track']['artists']])
      albumName = track['track']['album']['name']
      albumImageURL = track['track']['album']['images'][0]['url']
      imagePath = f"album\\{currentGenre}_{trackIndex}.jpg"

      genreTracks[genreIndex].append(
          Track(trackName, artistNames, albumName, albumImageURL, imagePath))

      with open(imagePath, 'wb') as f:
        response = get(albumImageURL)
        f.write(response.content)

      print(
          f"{trackIndex+1}. {trackName} - {artistNames}")

  return genreTracks


def uploadToFeed(instagramAPI, genreTracks):
  global count
  for genreIndex, genreTrack in genreTracks:
    track = genreTracks[count]

    trackName = track.name
    artistName = track.artistName
    albumName = track.albumName
    imagePath = track.imagePath
    post_instagram(instagramAPI, imagePath, trackName,
                   artistName, albumName, genre[genreIndex])
  count += 1
  dir = db.reference('')
  dir.update({'count', count})
  sendDM(instagramAPI)


def sendDM(instagramAPI):
  dir = db.reference('usercount')
  usercount = int(dir.get())
  users = []
  userIDs = []

  for i in range(1, usercount+1):
    dir = db.reference(str(i))
    users.append(dir.get())

  for id in users:
    # if userID starts quote
    if id[0] == '\"':
      id = id[1:len(id)-1]

    userIDs.append(instagramAPI.user_id_from_username(id))

  now = datetime.datetime.now()
  if now.hour > 10:
    text = f"{now.month}월 {now.day}일 두 번째 플레이리스트가 업로드되었습니다. 확인해 보세요!"
  else:
    text = f"{now.month}월 {now.day}일 첫 번째 플레이리스트가 업로드되었습니다. 확인해 보세요!"

  for userID in userIDs:
    instagramAPI.direct_send(user_ids=[userID], text=text)
    print(f"Direct Message Sent Successfully to {userID}")


def setInterval(func, sec, *args):
  def wrapper():
    setInterval(func, sec)
    func(args)
  t = threading.Timer(sec, wrapper)
  t.start()
  return t


def intervalFunc(playlistIDs):
  global genreTracks

  now = datetime.datetime.now()
  if now.hour == 5 and now.minute == 0:
    genreTracks = downlodAlbums()
    uploadToFeed(instagramAPI, genreTracks)
    print(f"{now.hour}:{now.minute}. Upload Completed")
  elif now.hour == 12 and now.minute == 00:
    if genreTracks is None:
      genreTracks = downlodAlbums()

    uploadToFeed(instagramAPI, genreTracks)
    print(f"{now.hour}:{now.minute}. Upload Completed")
  elif now.hour == 0 and now.minute == 00:
    downlodAlbums(playlistIDs)


if __name__ == "__main__":
  playlistIDs = []
  tracks = []
  genre = ['Jazz', 'POP', 'EDM']

  cred = credentials.Certificate(creddata)
  firebase_admin.initialize_app(cred, {'databaseURL': firebase_url})

  token = getSpotifyToken()

  # playlist IDs
  playlistIDs.append("6Il6PFSWjgjOU7PzA7w4GX")
  playlistIDs.append("47qCrjU2wU4YxN5Vh6yvpH")
  playlistIDs.append("60u1afVzJndAh2pS1Rxrd6")

  dir = db.reference('count')
  count = int(dir.get())
  instagramAPI = loginInstagrawm(instagram_username, instagram_password)
  print(count)
  downlodAlbums(playlistIDs)

  setInterval(intervalFunc, 60, playlistIDs)
