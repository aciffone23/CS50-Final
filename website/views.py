from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website.routes import get_featured_playlists, get_token, get_album, get_playlist, get_artist
from datetime import datetime
import math

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
        likes_total = playlist.get('followers').get('total', 'N/A')
        likes = "{:,}".format(likes_total)
        songs = playlist.get('tracks').get('total', 'N/A')
        album_name = playlist.get('name', 'N/A')
        background = playlist.get('images', [{}])[0].get('url')
        tracks = playlist.get('tracks', {}).get('items', [])
        album_type= playlist.get('album_type', 'N/A')
        total_duration_seconds = 0


        track_info = []
        for track in tracks:
                name = track.get('track', {}).get('name', 'N/A')
                artist = ", ".join([artist.get('name', 'N/A') for artist in track.get('track', {}).get('artists', [])])
                album = track.get('track', {}).get('album', {}).get('name', 'N/A')
                id = track.get('track', {}).get('album', {}).get('id', 'N/A')
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
                print(id)

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
                total_duration_seconds += seconds
        
        minutes = math.ceil(total_duration_seconds / 60) 
        hours = minutes // 60
        remaining_minutes = minutes % 60
        total_time = f"{hours} hr {remaining_minutes} min"
                
        return render_template("home.html", user=current_user, tracks=track_info, album_name=album_name,  description=description, 
                               likes=likes, songs=songs, current_page=f"/playlist/{playlist_id}", background=background, album_type=album_type,
                               total_time=total_time)

@views.route('/album/<album_id>', methods=['GET'])
# @login_required
def album_detail(album_id):
        token = get_token()
        album = get_album(token, album_id)

        songs = album.get('total_tracks')
        album_name = album.get('name', 'N/A')
        tracks = album.get('tracks', {}).get('items', [])

        images = album.get('images', [])
        background = images[1]['url'] if images else 'N/A'
        album_type= album.get('album_type', 'N/A')
        first_artist = album.get('artists', [{}])[0]
        artist_id = first_artist.get('id', 'N/A')
        artist_name = first_artist.get('name', 'N/A')
        release_date = album.get('release_date', 'N/A')
        parsed_date = datetime.strptime(release_date, "%Y-%m-%d")
        year = parsed_date.year

        artist = get_artist(token, artist_id)
        artist_images = artist.get('images', [])
        artist_image = artist_images[1]['url'] if artist_images else 'N/A'

        total_duration_seconds = 0

        album_info = []
        for track in tracks:
                name = track.get('name', 'N/A')
                artist = ", ".join([artist.get('name', 'N/A') for artist in track.get('artists', [])])
                id = track.get('id', 'N/A')
                explicit = track.get('explicit', 'N/A')
                duration_ms = track.get('duration_ms', 'N/A')
                seconds = duration_ms // 1000
                minutes = seconds // 60
                remaining_seconds = seconds % 60
                formatted_time = f"{minutes}:{remaining_seconds:02d}"
                print(artist)

                album_info.append({
                        'name': name,
                        'artist': artist,
                        'id': id,
                        'duration': formatted_time,
                        'explicit': explicit,
                })
                total_duration_seconds += seconds

        if total_duration_seconds >= 3600:
                minutes = math.ceil(total_duration_seconds / 60)
                hours = minutes // 60
                remaining_minutes = minutes % 60
                total_time = f"{hours} hr {remaining_minutes} min"
        else:
                minutes = total_duration_seconds // 60
                seconds = total_duration_seconds % 60
                total_time = f"{minutes} min {seconds} sec"
                
        return render_template("home.html", user=current_user, tracks=album_info, album_name=album_name, songs=songs, 
                               current_page=f"/album/{album_id}", background=background, album_type=album_type, artist_image=artist_image, 
                               artist_name=artist_name, year=year, total_time=total_time)
