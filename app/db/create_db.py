from app.accounts import Account
from app.extensions import db
from app.orders import Order
from app.positions import Position


def create_dbs():
    db.drop_all()
    db.create_all()
