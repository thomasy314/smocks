from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from app.auth import authorize_request
from app.orders.order_funcs import create_new_order, excecute_order
from app.orders.validators.buy_order_validator import BuyOrderBody
from app.request_validator import validate_request

bp = Blueprint('orders', __name__)

@bp.route('/buy', methods=['POST'])
@bp.route('/sell', methods=['POST'])
@validate_request(BuyOrderBody())
@authorize_request(add_account_id=True)
def buy_order(account_id):
    """ create smock buy order"""

    side = request.path.split('/')[-1]

    # Create new Order
    asset_id = request.json.get("asset_id")
    quantity = request.json.get("quantity")
    notional = request.json.get("notional")
    limit_price = request.json.get("limit_price")
    stop_price = request.json.get("stop_price")
    order_type = request.json.get("type")


    new_order = create_new_order(
        asset_id=asset_id, 
        account_id=account_id, 
        side=side,
        quantity=quantity, 
        notional=notional, 
        limit_price=limit_price, 
        stop_price=stop_price, 
        order_type=order_type
        )

    try:
        excecute_order(new_order)    
        return "", 200
    except IntegrityError as error:
        return str(error.orig), 400

