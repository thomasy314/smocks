import logging

from flask import Blueprint, request

from app.auth import authorize_request
from app.positions.service import get_account_positions

bp = Blueprint("positions", __name__)

@bp.get('/')
@authorize_request(add_account_id=True)
def get_positions(account_id):

    expand_values = request.args.get('expand[]', default='').split(",")

    expand_asset = 'asset' in expand_values

    positions = get_account_positions(account_id=account_id, expand_asset=expand_asset)

    return [p.serialize for p in positions], 200


