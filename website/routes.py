from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from datetime import datetime
import requests


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

def get_album(token, album_id):
    url=f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_artist(token, artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_artist_image(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        artist_data = response.json()
        images = artist_data.get('images', [])
        image_url = images[1]['url'] if images else 'N/A'
        return image_url
    else:
        print(f"Error fetching artist image. Status code: {response.status_code}")
        return 'N/A'
    
def get_artist_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=single%2Calbum&limit=7"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    albums_info = []
    for album in json_result.get('items', []):
        images = album.get('images', [])
        background = images[1]['url'] if images else 'N/A'
        id = album.get('id', 'N/A')
        album_name = album.get('name', 'N/A')

        release_date = album.get('release_date', 'N/A')
        parsed_date = datetime.strptime(release_date, "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%B %d, %Y")
        year = parsed_date.year

        albums_info.append({
            'background': background,
            'album_name': album_name,
            'formatted_date': formatted_date,
            'year': year,
            'id': id
        })

    return albums_info

def get_track_recommendations(token, artist_id, track_id):
    url = f'https://api.spotify.com/v1/recommendations?limit=5&market=US&seed_artists={artist_id}&seed_tracks={track_id}'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    # print(headers)
    # print(result)
    # print(json_result)

    recommendations = []
    for rec in json_result.get('tracks', []):
        images = rec.get('album', {}).get('images', [])
        background = images[1]['url'] if images else 'N/A'
        id = rec.get('album', {}).get('id', 'N/A')
        track_id = rec.get('id', 'N/A')
        album_name = rec.get('name', 'N/A')
        duration_ms = rec.get('duration_ms', 'N/A')
        seconds = duration_ms // 1000
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        formatted_time = f"{minutes}:{remaining_seconds:02d}"
        artists_info = [{'name': artist.get('name', 'N/A'), 'id': artist.get('id', 'N/A')} for artist in rec.get('artists', [])]
        explicit = rec.get('explicit', 'N/A')

        recommendations.append({
            'background': background,
            'album_name': album_name,
            'id': id,
            'formatted_time': formatted_time,
            'artists_info': artists_info,
            'explicit': explicit,
            'track_id': track_id,
        })
    
    return recommendations

def get_artist_top_tracks(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=us'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    top_tracks = []

    for track in json_result.get('tracks', []):
        images = track.get('album', {}).get('images', [])
        background = images[1]['url'] if images else 'N/A'
        id = track.get('album', {}).get('id', 'N/A')
        track_id = track.get('id', 'N/A')
        album_name = track.get('name', 'N/A')
        duration_ms = track.get('duration_ms', 'N/A')
        seconds = duration_ms // 1000
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        formatted_time = f"{minutes}:{remaining_seconds:02d}"
        artists_info = [{'name': artist.get('name', 'N/A'), 'id': artist.get('id', 'N/A')} for artist in track.get('artists', [])]
        explicit = track.get('explicit', 'N/A')

        top_tracks.append({
            'background': background,
            'album_name': album_name,
            'id': id,
            'formatted_time': formatted_time,
            'artists_info': artists_info,
            'explicit': explicit,
            'track_id': track_id,
        })
    return top_tracks

def get_similar_artists(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    top_artists = []
    for artist in json_result.get('artists', []):
        images = artist.get('images', [])
        background = images[1]['url'] if images else 'N/A'
        id = artist.get('id', 'N/A')
        name = artist.get('name', 'N/A')

        top_artists.append({
            'background': background,
            'id': id,
            'name': name,
        })

    return top_artists
        
# # Replace with actual values
# your_token = get_token()
# your_artist_id = '2LIk90788K0zvyj2JJVwkJ'
# # your_track_id = '4xhsWYTOGcal8zt0J161CU'

# # # Call the function
# results = get_artist_top_tracks(your_token, your_artist_id)

# print(results)



