import base64
from functools import wraps

from flask import abort, make_response, request

from app.accounts import Account
from app.extensions import bcrypt


def authorize_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get auth header
        authorization = request.headers.get('Authorization')

        if not authorization:
            abort(401, description="Unauthorized - Missing Authorization header")
            return None

        # Get auth header parts
        basic_auth = authorization.split(' ')

        if len(basic_auth) != 2 or basic_auth[0] != 'Basic':
            response = make_response(
                'Unauthorized - Incorrect auth scheme', 401)
            response.headers['WWW-Authenticate'] = 'Basic'
            abort(response)
            return

        # decode auth header
        basic_token = basic_auth[1]

        decoded_token = base64.b64decode(
            basic_token).decode("utf-8").split(":")

        if len(decoded_token) != 2:
            description = 'Unauthorized - Incorrectly formatted basic auth, expected: base64(username:password)'
            response = make_response(
                description, 401)
            response.headers['WWW-Authenticate'] = 'Basic'
            abort(response)
            return

        # Check credentials in db
        [username, password] = decoded_token

        account = Account.query.filter_by(username=username).first()

        if not account:
            abort(
                401, description=f'No account found for this username: {username}')
            return

        if not bcrypt.check_password_hash(account.password, password):
            abort(401, description='Incorrect password')
            return

        return f(*args, **kwargs)
    return decorated_function
