from flask import Blueprint, request

from app.auth.exceptions import UserAlreadyExists
from app.auth.service import check_account_credentials, create_account
from app.auth.validators.request_validator import LoginBody, RegisterBody
from app.request_validator import validate_request
from app.smock_response import SmockResponse

bp = Blueprint("auth", __name__)


@bp.post("/login")
@validate_request(LoginBody())
def login():
    """ Handles checking basic login info """
    username = request.json.get("username")
    password = request.json.get("password")

    if not username:
        return "missing username", 400

    if not password:
        return "missing password", 400

    login_successful = check_account_credentials(username=username, password=password)

    if login_successful:
        return "", 200
    else:
        return "", 401

@bp.post("/register")
@validate_request(RegisterBody())
def register():
    """ Handles creating new users """
    username = request.json.get("username")
    password = request.json.get("password")

    if not username:
        return "missing username", 400

    if not password:
        return "missing password", 400

    try:
        new_user = create_account(username=username, password=password)
    except UserAlreadyExists:
        return "User already exists", 409

    response = SmockResponse(new_user.serialize, status=201)
    response.headers['Location'] = f'/accounts/{new_user.masked_id}'

    return response