from flask import make_response
from werkzeug.exceptions import InternalServerError, NotFound

from config import smocksLogger


def register_error_handlers(app):

    @app.errorhandler(415)
    def generic_error_handler(error):

        response = make_response("Unsupported media type, requires: application/json", 415)
        response.headers["Accept-Post"] = "application/json"

        return response

    @app.errorhandler(NotFound)
    def not_found_handler(error):
        return error.description, 404

    @app.errorhandler(InternalServerError)
    def internal_server_error(error: InternalServerError):
        smocksLogger.error(error.description, exc_info=True)

        return "Internal Error", 500

    @app.errorhandler(Exception)
    def generic_error_handler(error):
        message = f"Improperly handled exception: {str(error)}"
        smocksLogger.error(message, exc_info=True)

        return "Internal Error", 500