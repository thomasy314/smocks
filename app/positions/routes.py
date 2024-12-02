from flask import Blueprint

from app.auth import authorize_request
from app.positions.service import get_account_positions

bp = Blueprint("positions", __name__)

@bp.get('/')
@authorize_request(add_account_id=True)
def get_positions(account_id):

    positions = get_account_positions(account_id=account_id)

    return [p.serialize for p in positions], 200


