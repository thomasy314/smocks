from dotenv import load_dotenv
from flask import Flask

from app.artists import bp as artists_bp
from app.auth.routes import bp as auth_bp
from app.extensions import bcrypt, db
from config import Config


def create_app(config_class=Config):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(artists_bp, url_prefix='/artists')
    app.register_blueprint(auth_bp)

    return app
