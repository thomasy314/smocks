from enum import Enum

from sqlalchemy import CheckConstraint, ForeignKey

from app.accounts import Account
from app.auth import mask_value
from app.extensions import db


class OrderType(Enum):
    """ Types of orders you can make when buying or selling smocks """
    market='market'
    # limit=2
    # stop=3
    # stop_limit=4

class OrderStatus(Enum):
    """ States for the status of an order"""
    created='created'
    completed='completed'
    cancelled='concelled'
    failed='failed'

class OrderSide(Enum):
    """ Sides of an order """
    buy='buy'
    sell='sell'


class Order(db.Model):
    """ Schema for order database """
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, ForeignKey(Account.id), nullable=False)
    asset_id = db.Column(db.Text, nullable=False)
    side = db.Column(db.Enum(OrderSide), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False)
    status_reason = db.Column(db.Text)
    limit_price = db.Column(db.Float)
    stop_price = db.Column(db.Float)
    type = db.Column(db.Enum(OrderType), nullable=False)
    quantity = db.Column(db.Integer)
    notional = db.Column(db.Float)

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_positive'),
        CheckConstraint('notional > 0', name='check_notional_positive'),
        CheckConstraint('quantity IS NOT NULL OR notional IS NOT NULL', name="check_for_quantity_or_notional")
    )

    @property
    def masked_id(self):
        return mask_value(self.id)

    @property
    def masked_account_id(self):
        return mask_value(self.account_id)

    @property
    def serialize(self):
        return {
            'id': self.masked_id,
            'account_id': self.masked_account_id,
            'asset_id': self.asset_id,
            'side': self.side.value,
            'create_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status.value,
            'status_reason': self.status_reason,
            'limit_price': self.limit_price,
            'stop_price': self.stop_price,
            'type': self.type.value,
            'quantity': self.quantity,
            'notional': self.notional
        }