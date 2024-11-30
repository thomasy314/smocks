
from pprint import pprint

from flask import Blueprint, jsonify

from app.auth import authorize_request
from app.extensions import spotifyAPI
from app.orders.validators.buy_order_validator import BuyOrderBody
from app.positions.models.position import Position
from app.request_validator import validate_request

bp = Blueprint("positions", __name__)

@bp.route('/')
@validate_request(BuyOrderBody())
@authorize_request(add_account_id=True)
def get_positions(account_id):
    positions = Position.query.filter_by(account_id=account_id).all()

    return [p.serialize for p in positions], 200


