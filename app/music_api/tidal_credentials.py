import base64
import time

import requests

from config import DEFAULT_REQUEST_TIMEOUT, TidalConfig


class TidalAuth():
    auth_url = 'https://auth.tidal.com/v1/oauth2/token'

    def __init__(self, config=TidalConfig):
        self.access_token = None
        self.expire_time = 0
        self.config = config

    def get_tidal_token(self):
        if self.access_token == None or self.expire_time < time.time():
            self.refresh_tidal_token()
        return self.access_token

    def refresh_tidal_token(self):
        import requests

        url = "https://auth.tidal.com/v1/oauth2/token"

        basicAuthToken = base64.b64encode(f'{self.config.CLIENT_ID}:{self.config.CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')

        payload = 'grant_type=client_credentials'
        headers = {
        'Authorization': f'Basic {basicAuthToken}',
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload, timeout=DEFAULT_REQUEST_TIMEOUT)
        data = response.json()

        self.access_token = data['access_token']
        self.expire_time = time.time() + data['expires_in']

