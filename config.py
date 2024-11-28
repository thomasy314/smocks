import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or f'sqlite:///{os.path.join(basedir, 'app.db')}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class SpotifyConfig:
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')