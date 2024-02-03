from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website.routes import get_featured_playlists, get_token, get_album, get_playlist, get_artist, get_track, get_artist_image, get_artist_albums, get_track_recommendations, get_artist_top_tracks, get_similar_artists
from datetime import datetime
import math, requests
from colorthief import ColorThief
from PIL import Image
from io import BytesIO


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
        tracks = playlist.get('tracks', {}).get('items', [])
        album_type= playlist.get('album_type', 'N/A')
        total_duration_seconds = 0

        background = playlist.get('images', [{}])[0].get('url')
        response = requests.get(background)
        image = Image.open(BytesIO(response.content))

        image_buffer = BytesIO()
        image.save(image_buffer, format="JPEG")
        
        color_thief = ColorThief(image_buffer)

        palette = color_thief.get_palette(color_count=2, quality=1)

        second_dominant_color = palette[0]

        hex_color = "#{:02x}{:02x}{:02x}".format(*second_dominant_color)

        track_info = []
        for track in tracks:
                name = track.get('track', {}).get('name') if track and track.get('track') else 'N/A'
                if name == 'N/A':
                        continue 
                artists_info = [{'name': artist.get('name', 'N/A'), 'id': artist.get('id', 'N/A')} for artist in (track.get('track', {}) or {}).get('artists', [])]
                album = (track.get('track', {}) or {}).get('album', {}).get('name', 'N/A')
                id = (track.get('track', {}) or {}).get('album', {}).get('id', 'N/A')
                explicit = (track.get('track', {}) or {}).get('explicit', 'N/A')
                added = track.get('added_at', 'N/A')
                track_id = (track.get('track', {}) or {}).get('id', 'N/A')
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
                        'artists_info': artists_info,
                        'album': album,
                        'image_url': image_url,
                        'id': id,
                        'duration': formatted_time,
                        'explicit': explicit,
                        'added': added_info, 
                        'track_id': track_id,
                })
                total_duration_seconds += seconds
        
        minutes = math.ceil(total_duration_seconds / 60) 
        hours = minutes // 60
        remaining_minutes = minutes % 60
        total_time = f"{hours} hr {remaining_minutes} min"
                
        return render_template("home.html", user=current_user, tracks=track_info, album_name=album_name,  description=description, 
                               likes=likes, songs=songs, current_page=f"/playlist/{playlist_id}", background=background, album_type=album_type,
                               total_time=total_time, hex_color=hex_color, )

@views.route('/album/<album_id>', methods=['GET'])
# @login_required
def album_detail(album_id):
        token = get_token()
        album = get_album(token, album_id)

        songs = album.get('total_tracks')
        album_name = album.get('name', 'N/A')
        tracks = album.get('tracks', {}).get('items', [])

        images = album.get('images', [])
        album_type= album.get('album_type', 'N/A')
        first_artist = album.get('artists', [{}])[0]
        artist_id = first_artist.get('id', 'N/A')
        artist_name = first_artist.get('name', 'N/A')

        release_date = album.get('release_date', 'N/A')
        parsed_date = datetime.strptime(release_date, "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%B %d, %Y")
        year = parsed_date.year

        background = images[1]['url'] if images else 'N/A'
        response = requests.get(background)
        image = Image.open(BytesIO(response.content))

        image_buffer = BytesIO()
        image.save(image_buffer, format="JPEG")
        
        color_thief = ColorThief(image_buffer)

        palette = color_thief.get_palette(color_count=5, quality=1)

        second_dominant_color = palette[0]

        hex_color = "#{:02x}{:02x}{:02x}".format(*second_dominant_color)

        artist = get_artist(token, artist_id)
        artist_images = artist.get('images', [])
        artist_image = artist_images[1]['url'] if artist_images else 'N/A'

        copyrights = album.get('copyrights', [])

        total_duration_seconds = 0

        albums_data = get_artist_albums(token, artist_id)

        album_info = []
        for track in tracks:
                name = track.get('name', 'N/A')
                artists_info = [{'name': artist.get('name', 'N/A'), 'id': artist.get('id', 'N/A')} for artist in track.get('artists', [])]
                id = track.get('id', 'N/A')
                explicit = track.get('explicit', 'N/A')
                duration_ms = track.get('duration_ms', 'N/A')
                seconds = duration_ms // 1000
                minutes = seconds // 60
                remaining_seconds = seconds % 60
                formatted_time = f"{minutes}:{remaining_seconds:02d}"

                album_info.append({
                        'name': name,
                        'artists_info': artists_info,
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
                               artist_name=artist_name, year=year, total_time=total_time, hex_color=hex_color, formatted_date=formatted_date,
                               copyrights=copyrights, albums_data=albums_data)


@views.route('/track/<track_id>', methods=['GET'])
# @login_required
def track_detail(track_id):
        token = get_token()
        track = get_track(token, track_id)

        track_name = track.get('name', 'N/A')

        album_info = track.get('album', {})
        images = album_info.get('images', [])
        track_type = album_info.get('album_type', 'N/A')
        album_name = album_info.get('name', 'N/A')
        album_id = album_info.get('id', 'N/A')

        first_artist = track.get('artists', [{}])[0]
        first_artist_id = first_artist.get('id', 'N/A')
        first_artist_name = first_artist.get('name', 'N/A')
        first_artist_picture = get_artist_image(token, first_artist_id)

        artists = track.get('artists', [])
        artist_data = []
        
        recommended_data = get_track_recommendations(token, first_artist_id, track_id )
        top_tracks = get_artist_top_tracks(token, first_artist_id)
        similar_artists = get_similar_artists(token, first_artist_id)

        for artist in artists:
                artist_id = artist.get('id', 'N/A')
                artist_name = artist.get('name', 'N/A')
                artist_image = get_artist_image(token, artist_id)
                artist_data.append({
                        'id': artist_id,
                        'name': artist_name,
                        'image': artist_image,
                })
        release_date = album_info.get('release_date', 'N/A')
        parsed_date = datetime.strptime(release_date, "%Y-%m-%d")
        year = parsed_date.year

        background = images[1]['url'] if images else 'N/A'
        response = requests.get(background)
        image = Image.open(BytesIO(response.content))
        image_buffer = BytesIO()
        image.save(image_buffer, format="JPEG")
        color_thief = ColorThief(image_buffer)
        palette = color_thief.get_palette(color_count=5, quality=1)
        second_dominant_color = palette[0]
        hex_color = "#{:02x}{:02x}{:02x}".format(*second_dominant_color)

        duration_ms = track.get('duration_ms', 'N/A')
        seconds = duration_ms // 1000
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        formatted_time = f"{minutes}:{remaining_seconds:02d}"

        return render_template("home.html", user=current_user, track_name=track_name, current_page=f"/track/{track_id}",
                                background=background, track_type=track_type, artist_data=artist_data, album_name=album_name,
                                album_id=album_id, year=year, total_time=formatted_time, hex_color=hex_color, first_artist_id=first_artist_id,
                                first_artist_name=first_artist_name, first_artist_picture=first_artist_picture, recommended_data=recommended_data,
                                top_tracks=top_tracks, similar_artists=similar_artists)

@views.route('/artist/<artist_id>', methods=['GET'])
# @login_required
def artist_detail(artist_id):
        token = get_token()
        artist = get_artist(token, artist_id)

        artist_name = artist.get('name', 'N/A')
        images = artist.get('images', [])
        background = images[0]['url'] if images else 'N/A'
        response = requests.get(background)
        image = Image.open(BytesIO(response.content))
        image_buffer = BytesIO()
        image.save(image_buffer, format="JPEG")
        color_thief = ColorThief(image_buffer)
        palette = color_thief.get_palette(color_count=5, quality=1)
        second_dominant_color = palette[0]
        hex_color = "#{:02x}{:02x}{:02x}".format(*second_dominant_color)

        top_tracks = get_artist_top_tracks(token, artist_id)
        similar_artists = get_similar_artists(token, artist_id)


        return render_template("home.html", user=current_user, artist_name=artist_name, current_page=f"/artist/{artist_id}",
                               background=background, hex_color=hex_color, top_tracks=top_tracks, similar_artists=similar_artists)