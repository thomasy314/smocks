from sqlalchemy import CheckConstraint

from app.extensions import db
from config import AccountConfig


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=AccountConfig.DEFAULT_BALANCE)

    __table_args__ = (
        CheckConstraint('balance > 0', name='check_balance_positive'),
    )