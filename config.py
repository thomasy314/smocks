import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEFAULT_REQUEST_TIMEOUT = 10

class Config:
    SECRET_KEY=os.getenv('SMOCKS_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI') or f'sqlite:///{os.path.join(basedir, 'app.db')}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_LENGTH_SECONDS = 3600

class AccountConfig:
    DEFAULT_BALANCE = 100

class SpotifyConfig:
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

class TidalConfig:
    CLIENT_ID = os.getenv('TIDAL_CLIENT_ID')
    CLIENT_SECRET = os.getenv('TIDAL_CLIENT_SECRET')

class GoogleConfig:
    SEARCH_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
    SEARCH_BILLBOARD_ENGINE = os.getenv('GOOGLE_SEARCH_BILLBOARD_ENGINE')