import requests
from app.music_api.spotify_credentials import SpotifyAuth

class SpotifyAPI():

    BASE_URL = 'https://api.spotify.com/v1'

    def __init__(self, Auth=SpotifyAuth):
        self.auth = Auth()

    def get_artist(self, artist_id):
        headers = {
            'Authorization': f'Bearer {self.auth.get_spotify_token()}'
        }
        response = requests.get(f'{self.BASE_URL}/artists/{artist_id}', headers=headers)

        return response.json()