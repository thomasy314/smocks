from flask import Blueprint

from app.auth import authorize_request
from app.extensions import spotifyAPI
from app.positions.models.position import Position

bp = Blueprint("positions", __name__)

@bp.route('/')
@authorize_request(add_account_id=True)
def get_positions(account_id):
    positions = Position.query.filter_by(account_id=account_id).all()

    results = []

    for p in positions:
        artist_info = spotifyAPI.get_artist(p.asset_id)

        artist_result_data = {
            "id": artist_info['id'],
            "url": artist_info['external_urls']['spotify'],
            "followers": artist_info['followers']['total'],
            "name": artist_info['name'],
            "popularity": artist_info['popularity'],
            "type": artist_info['type']
        }

        new_result = p.serialize

        del new_result['asset_id']
        new_result['asset_info'] = artist_result_data

        results.append(new_result)


    return results, 200


