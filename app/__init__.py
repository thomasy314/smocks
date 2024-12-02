from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.error_handler import register_error_handlers
from app.extensions import bcrypt, db
from app.smock_response import SmockResponse
from config import Config


def create_app(config_class=Config):
    load_dotenv()

    app = Flask(__name__)
    CORS(app)
    app.response_class = SmockResponse
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.accounts.routes import bp as accounts_bp
    app.register_blueprint(accounts_bp, url_prefix='/accounts')

    from app.artists import bp as artists_bp
    app.register_blueprint(artists_bp, url_prefix='/artists')

    from app.orders import bp as orders_bp
    app.register_blueprint(orders_bp, url_prefix='/orders')

    from app.positions import bp as positions_bp
    app.register_blueprint(positions_bp, url_prefix='/positions')

    register_error_handlers(app)

    return app
