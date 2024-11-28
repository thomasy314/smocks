from flask import Flask

from config import Config
from app.extensions import db

from app.artists import bp as artists_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(artists_bp, url_prefix='/artists')

    return app