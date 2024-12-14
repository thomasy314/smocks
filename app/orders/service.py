from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from app.accounts import Account
from app.artists import artistService
from app.extensions import db
from app.orders.exceptions import NotEnoughFundsException
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


def execute_market_order(order: Order):
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

    order_cost = artist.smock_price * quantity

    account: Account = Account.query.get_or_404(order.account_id)

    if account.balance - order_cost < 0:
        order.status_reason = "Not enough funds"
        raise NotEnoughFundsException()

    account.balance -= order_cost

    position: Position = Position.query.get((order.account_id, order.asset_id))

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
        # TODO: Improve error message passed to user
        order.status_reason = str(error.orig)
        raise error

def excecute_order(order: Order):
    order_type_funcs = {
        OrderType.market: execute_market_order
    }

    try:
        order_type_funcs[order.type](order)
    except Exception as e:
        order.status = OrderStatus.failed
        db.session.commit()
        raise e