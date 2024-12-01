from flask import Blueprint, request

from app.auth.service import create_account
from app.auth.validators.request_validator import RegisterBody
from app.request_validator import validate_request
from app.smock_response import SmockResponse

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

    if not new_user:
        return "Unable to create user", 400

    print('new user: ', new_user)
    response = SmockResponse(new_user.serialize, status=201)
    response.headers['Location'] = f'/accounts/{new_user.masked_id}'

    return response