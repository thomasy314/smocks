from flask import Blueprint

from app.auth import authorize_request
from app.artists.service import artistService

bp = Blueprint('artists', __name__)


@bp.route('/<string:artist_id>')
@authorize_request()
def getArtist(artist_id: str):
    artist_info = artistService.get_artist_from_id(artist_id=artist_id)

    return artist_info.serialize, 200
