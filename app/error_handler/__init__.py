from traceback import format_exc

from flask import make_response


def register_error_handlers(app):

    @app.errorhandler(415)
    def generic_error_handler(error):

        response = make_response("Unsupported media type, requires: application/json", 415)
        response.headers["Accept-Post"] = "application/json"

        return response

    @app.errorhandler(Exception)
    def generic_error_handler(error):
        print("Internal Error: ", format_exc())

        return "Internal Error", 500