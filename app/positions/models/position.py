from sqlalchemy import CheckConstraint

from app.auth import mask_value
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

    @property
    def masked_account_id(self):
        return mask_value(self.account_id)

    @property
    def serialize(self):
        return {
            'account_id': self.masked_account_id,
            'asset_id': self.asset_id,
            'quantity': self.quantity,
            'average_entry_price': self.average_entry_price
        }