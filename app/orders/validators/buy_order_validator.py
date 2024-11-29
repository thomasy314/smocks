from marshmallow import Schema, fields

from app.orders.models.orders import OrderSide, OrderType


class BuyOrderBody(Schema):
    """ Schema for buy order request """
    asset_id = fields.Str(required=True)
    quantity = fields.Int()
    notional = fields.Float()
    limit_price = fields.Float()
    stop_price = fields.Float()
    type = fields.Enum(OrderType, required=True)