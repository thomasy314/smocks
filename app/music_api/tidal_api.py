from enum import Enum

import requests
from werkzeug.exceptions import NotFound

from app.music_api.artist_data import ArtistData, TidalArtistData
from app.music_api.tidal_credentials import TidalAuth
from config import DEFAULT_REQUEST_TIMEOUT

class TidalExternalLinkTypes(Enum):
    TIDAL_SHARING="TIDAL_SHARING"

class TidalAPI():

    BASE_URL = 'https://openapi.tidal.com/v2'

    def __init__(self, Auth=TidalAuth):
        self.auth = Auth()

    def get_artist(self, artist_id: str) -> ArtistData:
        headers = {
            'Authorization': f'Bearer {self.auth.get_tidal_token()}'
        }
        response = requests.get(
            f'{self.BASE_URL}/artists/{artist_id}?countryCode=US', headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT)

        if response.status_code == 404:
            raise NotFound(f'cannot find artist with id: {artist_id}')

        if 300 <= response.status_code:
            raise Exception(f'Error getting Tidal artist: [{response.status_code}] {response.text}')

        response_data = response.json()['data']

        try:
            tidalUrl = next(url for url in response_data['attributes']['externalLinks'] if url['meta']['type'] == TidalExternalLinkTypes.TIDAL_SHARING.value)
        except StopIteration:
            raise NotFound(f'Unable to find Tidal artist url for: {response_data['id']}')
        except Exception as error:
            raise Exception(f'error getting url for {response_data['id']}: {str(error)}')

        tidalArtistData = TidalArtistData(
            id=response_data['id'],
            popularity=response_data['attributes']['popularity'],
            url=tidalUrl
        )

        return ArtistData(
            id=response_data['id'], 
            name=response_data['attributes']['name'],
            tidal=tidalArtistData
            )    
