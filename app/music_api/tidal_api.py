from enum import Enum
from http import HTTPMethod, HTTPStatus
from typing import List

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

    def query_tidal_api(self, url: str, method: HTTPMethod = HTTPMethod.GET, headers={}, params=None, body=None):

        headers['Accept'] = "application/json"
        response = requests.request(method.value, f'{self.BASE_URL}{url}', headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT, params=params, data=body)

        return response

    def get_artist(self, artist_id: str) -> TidalArtistData:
        response_data = self.get_raw_artists([artist_id])[0]

        tidalUrl = self._get_url_from_tidal_data(response_data)

        return TidalArtistData(
            id=response_data['id'],
            popularity=response_data['attributes']['popularity'],
            url=tidalUrl
        )

    def get_artists(self, artist_ids: List[str]) -> List[TidalArtistData]:
        response_data = self.get_raw_artists(artist_ids)

        def format_data(data):
            tidalUrl = self._get_url_from_tidal_data(data)

            return TidalArtistData(
                id=data['id'],
                name=data['attributes']['name'],
                popularity=data['attributes']['popularity'],
                url=tidalUrl
            )

        return list(map(format_data, response_data))

    def get_raw_artists(self, artist_ids: List[str]) -> List[object]:
        headers = {
            'Authorization': f'Bearer {self.auth.get_tidal_token()}'
        }
        params = {
            'countryCode': 'US',
            'filter[id]': ','.join(artist_ids)
        }
        url = '/artists'
        response = self.query_tidal_api(url, params=params, headers=headers)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise NotFound(f'cannot find an artist with id in: [{artist_ids}]')

        if 300 <= response.status_code:
            raise Exception(f'Error getting Tidal artist: [{response.status_code}] {response.text}')

        return response.json()['data']

    def _get_url_from_tidal_data(self, data) -> str:
        try:
            return next(url for url in data['attributes']['externalLinks'] if url['meta']['type'] == TidalExternalLinkTypes.TIDAL_SHARING.value)
        except StopIteration:
            raise NotFound(f'Unable to find Tidal artist url for: {data['id']}')
        except Exception as error:
            raise Exception(f'error getting url for {data['id']}: {str(error)}')