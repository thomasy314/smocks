from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app.accounts import Account
from app.extensions import db, spotifyAPI
from app.orders.models.orders import Order, OrderSide, OrderStatus, OrderType
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


def execute_market_order(order):
    """
    buying:
        1. get quantity
        2. update account balance (decrease for buying)
        3. update position (increase for buying)
        4. update status to completed
        5. commit
    """
    artist = spotifyAPI.get_artist(order.asset_id)
    smock_price = artist['popularity']

    side_mult = 1 if order.side == OrderSide.buy else -1

    quantity = order.quantity * side_mult

    if order.notional:
        quantity = order.notional//smock_price * side_mult

    account = Account.query.get_or_404(order.account_id)
    account.balance -= artist['popularity'] * quantity

    position = Position.query.get((order.account_id, order.asset_id))

    if not position:
        position = Position(
            asset_id=order.asset_id,
            account_id=order.account_id,
            quantity=quantity,
            average_entry_price=smock_price
        )
    else:
        position.quantity += quantity
        position.average_entry_price += (smock_price - position.average_entry_price)/(position.quantity)

    order.status = OrderStatus.completed

    try:
        if position.quantity == 0:
            db.session.delete(position)
        else:
            db.session.add(position)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        order.status = OrderStatus.failed
        db.session.commit()
        raise error

def excecute_order(order):
    order_type_funcs = {
        OrderType.market: execute_market_order
    }

    order_type_funcs[order.type](order)