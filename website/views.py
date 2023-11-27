from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website.routes import get_featured_playlists, get_token, get_playlist_tracks, get_track, get_playlist
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    token = get_token()
    featured_playlists = get_featured_playlists(token)

    playlists = featured_playlists.get('playlists', {}).get('items', [])

    playlist_info = []

    for playlist in playlists:
        name = playlist.get('name', 'N/A')
        description = playlist.get('description', 'N/A')
        id = playlist.get('id', 'N/A')

        images = playlist.get('images', [])
        image_url = images[0]['url'] if images else 'N/A'

        playlist_info.append({
                'name': name,
                'description': description,
                'image_url': image_url,
                'id': id
        })

    return render_template("home.html", user=current_user, playlists=playlist_info, current_page="/")



@views.route('/search', methods=['GET', 'POST'])
# @login_required
def search():
        return render_template("search.html", user=current_user)

@views.route('/playlist/<playlist_id>', methods=['GET'])
# @login_required
def playlist_detail(playlist_id):
        token = get_token()
        playlist = get_playlist(token, playlist_id)

        description = playlist.get('description', 'N/A')
        likes = playlist.get('followers').get('total', 'N/A')
        songs = playlist.get('tracks').get('total', 'N/A')
        album_name = playlist.get('name', 'N/A')
        background = playlist.get('images', [{}])[0].get('url')

        tracks = playlist.get('tracks', {}).get('items', [])

        track_info = []
        for track in tracks:
                name = track.get('track', {}).get('name', 'N/A')
                artist = ", ".join([artist.get('name', 'N/A') for artist in track.get('track', {}).get('artists', [])])
                album = track.get('track', {}).get('album', {}).get('name', 'N/A')
                id = track.get('track', {}).get('id', 'N/A')
                explicit = track.get('track', {}).get('explicit', 'N/A')
                added = track.get('added_at', 'N/A')

                if added != 'N/A':
                        added_value = datetime.strptime(added, '%Y-%m-%dT%H:%M:%SZ')
                        current_date = datetime.now()

                        time_delta = current_date - added_value

                        days = time_delta.days
                        remaining_seconds = time_delta.seconds

                        if remaining_seconds > 0:
                                days += 1

                        weeks = days // 7

                        if weeks > 0:
                                added_info = f"{weeks} weeks ago"
                        else:
                                added_info = f"{days} days ago"
                else:
                        added_info = 'N/A'


                duration_ms = track.get('track', {}).get('duration_ms', 'N/A')

                seconds = duration_ms // 1000
                minutes = seconds // 60
                remaining_seconds = seconds % 60
                formatted_time = f"{minutes}:{remaining_seconds:02d}"

                images = track.get('track', {}).get('album', {}).get('images', [])
                image_url = images[2]['url'] if images else 'N/A'


                track_info.append({
                        'name': name,
                        'artist': artist,
                        'album': album,
                        'image_url': image_url,
                        'id': id,
                        'duration': formatted_time,
                        'explicit': explicit,
                        'added': added_info, 
                })
                
        return render_template("home.html", user=current_user, tracks=track_info, album_name=album_name,  description=description, likes=likes, songs=songs, current_page=f"/playlist/{playlist_id}", background=background)
