
from marshmallow import Schema, fields


class RegisterBody(Schema):
    """ Schema for register request """
    username = fields.Str(required=True)
    password = fields.Str(required=True)