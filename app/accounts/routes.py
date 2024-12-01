
from flask import Blueprint

from app.accounts.service import get_account
from app.auth import authorize_request
from app.positions.service import get_account_market_value

bp = Blueprint('accounts', __name__)

@bp.get('/me')
@authorize_request(add_account_id=True)
def get_me(account_id):
    account = get_account(account_id=account_id)

    if account.id != account_id:
        return 'Forbidden', 403

    market_value = get_account_market_value(account_id=account_id)

    additional_info = {
        "market_value": market_value
    }

    return account.serialize | additional_info, 200