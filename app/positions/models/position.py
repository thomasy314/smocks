from sqlalchemy import CheckConstraint

from app.extensions import db


class Position(db.Model):
    __tablename__ = "positions"

    account_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    average_entry_price = db.Column(db.Float, nullable=False)

    __table_args__ = (
        CheckConstraint('quantity > 0', name="check_quantity_positive"),
    )