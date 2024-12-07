from traceback import format_exc

from flask import make_response

from werkzeug.exceptions import NotFound


def register_error_handlers(app):

    @app.errorhandler(415)
    def generic_error_handler(error):

        response = make_response("Unsupported media type, requires: application/json", 415)
        response.headers["Accept-Post"] = "application/json"

        return response

    @app.errorhandler(NotFound)
    def not_found_handler(error):
        return error.description, 404

    @app.errorhandler(Exception)
    def generic_error_handler(error):
        print("Internal Error: ", format_exc())

        return "Internal Error", 500