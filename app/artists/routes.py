from flask import Blueprint

from app.auth import authorize_request
from app.extensions import spotifyAPI
from app.smock_response import SmockResponse

bp = Blueprint('artists', __name__)


@bp.route('/<string:artist_id>')
@authorize_request()
def getArtist(artist_id: str):
    artist_info = spotifyAPI.get_artist(artist_id)

    if 'error' in artist_info:
        return "unable to find artist", 404

    response_data = {
            "id": artist_info['id'],
            "url": artist_info['external_urls']['spotify'],
            "followers": artist_info['followers']['total'],
            "name": artist_info['name'],
            "popularity": artist_info['popularity'],
            "type": artist_info['type'],
            "images": artist_info['images']
        }
    return response_data, 200
