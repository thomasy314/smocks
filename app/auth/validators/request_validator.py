
from marshmallow import Schema, fields


class LoginBody(Schema):
    """ Schema for login request """
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class RegisterBody(Schema):
    """ Schema for register request """
    username = fields.Str(required=True)
    password = fields.Str(required=True)

