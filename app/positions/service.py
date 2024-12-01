from functools import reduce

from app.positions.models.position import Position


def get_account_positions(account_id):
    return Position.query.filter_by(account_id=account_id).all()

def get_account_market_value(account_id):
    positions = get_account_positions(account_id)

    return reduce(lambda a, b: a + b.quantity * b.asset_info['popularity'], positions, 0)
