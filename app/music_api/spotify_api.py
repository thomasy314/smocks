import requests
from werkzeug.exceptions import NotFound

from app.music_api.artist_data import ArtistData, SpotifyArtistData
from app.music_api.music_api import MusicAPI
from app.music_api.spotify_credentials import SpotifyAuth
from config import DEFAULT_REQUEST_TIMEOUT

class SpotifyAPI(MusicAPI):

    BASE_URL = 'https://api.spotify.com/v1'

    def __init__(self, Auth=SpotifyAuth):
        self.auth = Auth()

    def get_artist(self, artist_id: str) -> ArtistData:
        headers = {
            'Authorization': f'Bearer {self.auth.get_spotify_token()}'
        }
        response = requests.get(
            f'{self.BASE_URL}/artists/{artist_id}', headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT)

        if response.status_code == 404:
            raise NotFound(f'cannot find artist with id: {artist_id}')

        if 300 <= response.status_code:
            raise Exception(f'Error getting spotify artist: [{response.status_code}] {response.text}')

        response_data = response.json()

        spotifyArtistData = SpotifyArtistData(
            id=response_data['id'],
            url=response_data['external_urls']['spotify'], 
            followers=response_data['followers']['total'],
            popularity=response_data['popularity']
        )

        return ArtistData(
            id=response_data['id'], 
            name=response_data['name'],
            spotify=spotifyArtistData
            )    