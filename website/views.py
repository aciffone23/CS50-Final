from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website.routes import get_featured_playlists, get_token

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

        images = playlist.get('images', [])
        image_url = images[0]['url'] if images else 'N/A'

        playlist_info.append({
            'name': name,
            'description': description,
            'image_url': image_url
        })

    return render_template("home.html", user=current_user, playlists=playlist_info)



@views.route('/search', methods=['GET', 'POST'])
# @login_required
def search():
        return render_template("search.html", user=current_user)
