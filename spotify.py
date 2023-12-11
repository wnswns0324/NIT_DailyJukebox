import base64
from env import client_id, client_secret
from requests import post, get
import json


def getSongsFromPlaylists(token, playlist_id):
  url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
  headers = getSpotifyAuthHeader(token)
  result = get(url, headers=headers)
  json_result = json.loads(result.content)
  return json_result


def getSpotifyToken():
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


def getSpotifyAuthHeader(token):
  return {"Authorization": "Bearer " + token}
