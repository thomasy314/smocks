import logging

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from app.auth import authorize_request, unmask_value
from app.orders.exceptions import NotEnoughFundsException
from app.orders.service import create_new_order, excecute_order, get_order_by_id
from app.orders.validators.create_order_request import CreateOrderRequest
from app.request_validator import validate_request
from app.smock_response import SmockResponse

bp = Blueprint('orders', __name__)

@bp.get('/<string:order_id>')
@authorize_request(add_account_id=True)
def get_order(account_id, order_id):
    order = get_order_by_id(order_id=unmask_value(order_id))

    if order.account_id != account_id:
        return 'Forbidden', 403

    return order.serialize, 200

@bp.post('/buy')
@bp.post('/sell')
@validate_request(CreateOrderRequest())
@authorize_request(add_account_id=True)
def create_order(account_id):
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

        response = SmockResponse(new_order.serialize, 201)
        response.headers['Location'] = f'/orders/{new_order.masked_id}'
        return response
    except IntegrityError:
        return SmockResponse(new_order.serialize, 400)
    except NotEnoughFundsException:
        return SmockResponse(new_order.serialize, 400)


