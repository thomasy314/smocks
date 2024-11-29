from enum import Enum

from sqlalchemy import CheckConstraint, ForeignKey

from app.accounts import Account
from app.extensions import db


class OrderType(Enum):
    """ Types of orders you can make when buying or selling smocks """
    market=1
    limit=2
    stop=3
    stop_limit=4

class OrderStatus(Enum):
    """ States for the status of an order"""
    created=1
    completed=2
    cancelled=3
    failed=4

class OrderSide(Enum):
    """ Sides of an order """
    buy=1
    sell=2


class Order(db.Model):
    """ Schema for order database """
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, ForeignKey(Account.id), nullable=False)
    asset_id = db.Column(db.String, nullable=False)
    side = db.Column(db.Enum(OrderSide), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False)
    limit_price = db.Column(db.Float)
    stop_price = db.Column(db.Float)
    type = db.Column(db.Enum(OrderType), nullable=False)
    quantity = db.Column(db.Integer)
    notional = db.Column(db.Float)

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('notional > 0', name='check_notional_positive'),
        CheckConstraint('quantity IS NOT NULL OR notional IS NOT NULL', name="check_for_quantity_or_notional")
    )

