
from app.accounts.models.account import Account


def get_account(account_id):
    return Account.query.get(account_id)
