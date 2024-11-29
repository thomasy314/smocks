import base64
from functools import wraps

from flask import abort, make_response, request

from app.accounts import Account
from app.auth.routes import bp
from app.auth.utils import mask_value
from app.extensions import bcrypt


def authorize_request(add_account_id=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Get auth header
            authorization = request.headers.get('Authorization')

            if not authorization:
                response = make_response("Unauthorized - Missing Authorization header", 401)
                response.headers['WWW-Authenticate'] = 'Basic'
                abort(response)
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
                response = make_response(f'Unauthorized - No account found for this username: {username}', 401)
                response.headers['WWW-Authenticate'] = 'Basic'
                abort(response)
                return

            if not bcrypt.check_password_hash(account.password, password):
                response = make_response('Unauthorized - Incorrect password', 401)
                response.headers['WWW-Authenticate'] = 'Basic'
                abort(response)
                return

            if add_account_id:
                kwargs.update({"account_id": account.id})

            return f(*args, **kwargs)
        return wrapper
    return decorator