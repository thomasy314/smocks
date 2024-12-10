from typing import List
import requests
from werkzeug.exceptions import NotFound

from app.music_api.artist_data import ArtistData, MusicBrainzData
from config import DEFAULT_REQUEST_TIMEOUT

from pprint import pprint

class MusicBrainzAPI():

    BASE_URL = 'https://musicbrainz.org/ws/2'

    def get_ids_from_artist_spotify_url(self, spotify_url: str) -> List[str]:
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(
            f'{self.BASE_URL}/url?resource={spotify_url}&inc=artist-rels', headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT)

        response_data = response.json()

        return [ d['artist']['id'] for d in response_data['relations'] ]

    def get_artist_info_from_artist_name(self, artist_name, min_score=100) -> List[str]:
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(
            f'{self.BASE_URL}/artist/?query=artist:{artist_name}', headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT)

        response_data = response.json()

        return [ d for d in response_data['artists'] if d['score'] >= min_score ]


    def get_artist(self, artist_id: str) -> ArtistData:
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(
            f'{self.BASE_URL}/artist/{artist_id}?inc=url-rels', headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT)

        if response.status_code == 404:
            raise NotFound(f'cannot find artist with id: {artist_id}')

        if 300 <= response.status_code:
            description = f'Error getting spotify artist: [{response.status_code}] {response.text}'
            raise Exception(description)

        response_data = response.json()

        musicBrainzData = MusicBrainzData(
            id=response_data['id']
        )

        return ArtistData(
            id=response_data['id'], 
            name=response_data['name'],
            musicBrainz=musicBrainzData
            )    