from flask import Blueprint

from app.auth import authorize_request
from app.extensions import spotifyAPI

bp = Blueprint('artists', __name__)


@bp.route('/<string:artist_id>')
@authorize_request()
def getArtist(artist_id: str):
    artist_info = spotifyAPI.get_artist(artist_id)
    response_data = {
        'id': artist_info['id'],
        'name': artist_info['name'],
        'genres': artist_info['genres'],
        'popularity': artist_info['popularity'],
        'follower_count': artist_info['followers']['total']
    }
    return response_data, 200
