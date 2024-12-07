from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from app.accounts import Account
from app.extensions import db
from app.artists import artistService
from app.orders.models.orders import Order, OrderSide, OrderStatus, OrderType
from app.positions import Position


def get_order_by_id(order_id):
    return Order.query.get(order_id)


def create_new_order(asset_id, account_id, side, quantity, notional, limit_price, stop_price, order_type):
    current_time = datetime.now(timezone.utc)

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
    artist = artistService.get_artist_from_id(order.asset_id)

    side_mult = 1 if order.side == OrderSide.buy else -1

    quantity = order.quantity * side_mult

    if order.notional:
        quantity = order.notional//artist.smock_price * side_mult

    account = Account.query.get_or_404(order.account_id)
    account.balance -= artist.smock_price * quantity

    position = Position.query.get((order.account_id, order.asset_id))

    if not position:
        position = Position(
            asset_id=order.asset_id,
            account_id=order.account_id,
            quantity=quantity,
            average_entry_price=artist.smock_price
        )
    else:
        position.quantity += quantity
        if position.quantity != 0:
            position.average_entry_price += (artist.smock_price - position.average_entry_price)/(position.quantity)
        else:
            position.average_entry_price = 0

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