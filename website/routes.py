from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from datetime import datetime


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
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_featured_playlists(token):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S")
    url = f"https://api.spotify.com/v1/browse/featured-playlists?country=Us&locale=sv_US&timestamp={formatted_time}&limit=20&offset=0"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_playlist_tracks(token, playlist_id):
    url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_track(token, track_id):
    url=f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_playlist(token, playlist_id):
    url=f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


token = get_token()

# get_playlist_tracks(token, '37i9dQZF1DWWY64wDtewQt' )
playlist_id = '37i9dQZF1DXcBWIGoYBM5M'
track_id = '2FDTHlrBguDzQkp7PVj16Q'

# track = get_track(token, track_id)
# print(track)

# playlist = get_playlist(token, playlist_id)

# tracks = playlist.get('tracks', {}).get('items', [])

# description = playlist.get('description', 'N/A')
# likes = playlist.get('followers').get('total', 'N/A')
# songs = playlist.get('tracks').get('total', 'N/A')
# print(description, likes, songs)

# print(playlist.get('tracks', []))

# print(tracks)

# track_info = []

# for track in tracks:
#     name = track.get('track', {}).get('name', 'N/A')
#     artist = ", ".join([artist.get('name', 'N/A') for artist in track.get('track', {}).get('artists', [])])
#     album = track.get('track', {}).get('album', {}).get('name', 'N/A')
#     id = track.get('track', {}).get('id', 'N/A')


#     duration_ms = track.get('track', {}).get('duration_ms', 'N/A')

#     seconds = duration_ms // 1000
#     minutes = seconds // 60
#     remaining_seconds = seconds % 60

#     images = track.get('track', {}).get('album', {}).get('images', [])
#     image_url = images[2]['url'] if images else 'N/A'

#     print(f"Name: {name}")
#     print(f"artist: {artist}")
#     print(f"album: {album}")
#     print(f"Id: {id}")
#     print(f"Image URL: {image_url}")
#     print(f"{minutes} minutes and {remaining_seconds} seconds")

# result = search_for_artist(token, "ACDC")
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)

# for idx, song in enumerate(songs):
#     print(f"{idx + 1}. {song['name']}")
# print(songs)
# print(result["name"])
# print(get_featured_playlists(token))

# featured_playlists = get_featured_playlists(token)

# playlists = featured_playlists.get('playlists', {}).get('items', [])

# for playlist in playlists:
#     name = playlist.get('name', 'N/A')
#     description = playlist.get('description', 'N/A')
#     id = playlist.get('id', 'N/A')

#     images = playlist.get('images', [])
#     image_url = images[0]['url'] if images else 'N/A'

#     print(f"Name: {name}")
#     print(f"Description: {description}")
#     print(f"Image URL: {image_url}")
#     print(f"Id: {id}")

#     print("\n")


