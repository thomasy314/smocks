from app.accounts.models.account import Account
from app.extensions import bcrypt, db


def create_account(username, password):
    if Account.query.filter_by(username=username).first():
        return None

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = Account(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return new_user