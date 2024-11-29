from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app.accounts import Account
from app.extensions import db, spotifyAPI
from app.orders.models.orders import Order, OrderSide, OrderStatus
from app.positions import Position


def create_new_order(asset_id, account_id, side, quantity, notional, limit_price, stop_price, order_type):
    current_time = datetime.now()

    new_order = Order(
        asset_id=asset_id,
        account_id=account_id,
        side=side,
        created_at=current_time,
        updated_at=current_time,
        quantity=quantity,
        notional=notional,
        status=OrderStatus.created,
        limit_price=limit_price,
        stop_price=stop_price,
        type=order_type
    )

    db.session.add(new_order)
    db.session.commit()

    return new_order

def execute_market_order(original_order):
    """
    buying:
        1. get quantity
        2. update account balance (decrease for buying)
        3. update position (increase for buying)
        4. update status to completed
        5. commit
    """
    artist = spotifyAPI.get_artist(original_order.asset_id)

    side_mult = 1 if original_order.side == OrderSide.buy else -1

    quantity = original_order.quantity * side_mult

    if original_order.notional:
        quantity = original_order.notional//artist['popularity'] * side_mult

    account = Account.query.get_or_404(original_order.account_id)
    account.balance -= artist['popularity'] * quantity

    position = Position.query.get((original_order.account_id, original_order.asset_id))

    if not position:
        position = Position(
            asset_id=original_order.asset_id,
            account_id=original_order.account_id,
            quantity=quantity
        )
    else:
        position.quantity += quantity

    original_order.status = OrderStatus.completed

    try:
        if position.quantity == 0:
            db.session.delete(position)
        else:
            db.session.add(position)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        original_order.status = OrderStatus.failed
        db.session.commit()
        raise error