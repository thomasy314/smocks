from flask import Blueprint, make_response, request

from app.accounts import Account
from app.auth.service import create_account
from app.auth.validators.request_validator import RegisterBody
from app.extensions import bcrypt, db
from app.request_validator import validate_request

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
@validate_request(RegisterBody())
def register():
    """ Handles creating new users """
    username = request.json.get("username")
    password = request.json.get("password")

    if not username:
        return "missing username", 400

    if not password:
        return "missing password", 400

    new_user = create_account(username=username, password=password)

    response = make_response(new_user.serialize, 201)
    response.headers['Location'] = f'/accounts/{new_user.masked_id}'

    return response