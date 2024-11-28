from flask import Blueprint, request

from app.accounts import Account
from app.auth import authorize_request
from app.extensions import bcrypt, db

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username:
        return "missing username", 400

    if not password:
        return "missing password", 400

    if Account.query.filter_by(username=username).first():
        return "username already exists", 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = Account(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return "", 201
