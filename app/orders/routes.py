from flask import Blueprint, make_response, request
from sqlalchemy.exc import IntegrityError

from app.auth import authorize_request, unmask_value
from app.orders.service import create_new_order, excecute_order, get_order_by_id
from app.orders.validators.buy_order_validator import BuyOrderBody
from app.request_validator import validate_request

bp = Blueprint('orders', __name__)

@bp.route('/<string:order_id>')
@authorize_request(add_account_id=True)
def get_order(account_id, order_id):
    order = get_order_by_id(order_id=unmask_value(order_id))

    return order.serialize, 200

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


        response = make_response("", 201)
        # TODO: Change to full path
        response.headers['Location'] = f'/orders/{new_order.masked_id}'
        return response, 201
    except IntegrityError as error:
        return str(error.orig), 400

