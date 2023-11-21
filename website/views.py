from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website.routes import get_featured_playlists, get_token, get_playlist_tracks, get_track, get_playlist

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
        name = playlist.get('name', 'N/A')
        background = playlist.get('images', [{}])[0].get('url')

        tracks = playlist.get('items', [])

        track_info = []

        for track in tracks:
                name = track.get('track', {}).get('name', 'N/A')
                artist = ", ".join([artist.get('name', 'N/A') for artist in track.get('track', {}).get('artists', [])])
                album = track.get('track', {}).get('album', {}).get('name', 'N/A')
                id = track.get('track', {}).get('id', 'N/A')



                duration_ms = track.get('track', {}).get('duration_ms', 'N/A')

                seconds = duration_ms // 1000
                minutes = seconds // 60
                remaining_seconds = seconds % 60

                images = track.get('track', {}).get('album', {}).get('images', [])
                image_url = images[2]['url'] if images else 'N/A'

                formatted_time = f"{minutes} : {remaining_seconds} "

                track_info.append({
                        'name': name,
                        'artist': artist,
                        'album': album,
                        'image_url': image_url,
                        'id': id,
                        'duration': formatted_time
                })

        return render_template("home.html", user=current_user, tracks=track_info, name=name,  description=description, likes=likes, songs=songs, current_page=f"/playlist/{playlist_id}", background=background)
