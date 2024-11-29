from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from app.music_api import SpotifyAPI

db = SQLAlchemy()
bcrypt = Bcrypt()
spotifyAPI = SpotifyAPI()