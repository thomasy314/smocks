import time

import requests

from config import DEFAULT_REQUEST_TIMEOUT, SpotifyConfig


class SpotifyAuth():
    auth_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, config=SpotifyConfig):
        self.access_token = None
        self.expire_time = 0
        self.config = config

    def get_spotify_token(self):
        if self.access_token == None or self.expire_time < time.time():
            self.refresh_spotify_token()
        return self.access_token

    def refresh_spotify_token(self):
        body = {
            "grant_type": "client_credentials",
            "client_id": self.config.CLIENT_ID,
            "client_secret": self.config.CLIENT_SECRET
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(
            self.auth_url, data=body, headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT)
        data = response.json()

        self.access_token = data['access_token']
        self.expire_time = time.time() + data['expires_in']
