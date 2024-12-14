from functools import reduce
from typing import List

from app.artists import artistService
from app.positions.models.position import Position


def get_account_positions(account_id, expand_asset=False):

    positions: List[Position] = Position.query.filter_by(account_id=account_id).all()

    if expand_asset:
        for pos in positions:
            pos.asset_info = artistService.get_artist_from_id(pos.asset_id)

    return positions


def get_account_market_value(account_id):
    positions = get_account_positions(account_id, expand_asset=True)

    return reduce(lambda a, b: a + b.quantity * b.asset_info.smock_price, positions, 0)