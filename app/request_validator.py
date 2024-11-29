from functools import wraps

from flask import request
from marshmallow import Schema


def validate_request(schema: Schema):
    """ Given a schema, creates decorator to validate incoming flask requests """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            validation = schema.validate(request.json)

            if len(validation):
                return validation, 400

            return f(*args, **kwargs)
        return wrapper
    return decorator