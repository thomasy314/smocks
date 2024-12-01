from traceback import format_exc


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def generic_error_handler(error):
        print("Internal Error: ", format_exc())

        return "Internal Error", 500