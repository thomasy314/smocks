from enum import Enum
from http import HTTPMethod, HTTPStatus
from typing import List

import requests
from werkzeug.exceptions import InternalServerError, NotFound

from app.music_api.artist_data import MusicBrainzArtistData
from config import DEFAULT_REQUEST_TIMEOUT


class PlatformName(Enum):
    SPOTIFY="spotify"
    TIDAL="tidal"

class MusicBrainzAPI():

    BASE_URL = 'https://musicbrainz.org/ws/2'

    def query_music_brainz_api(self, url: str, method: HTTPMethod = HTTPMethod.GET, headers={}, body={}):
        headers['Accept'] = 'application/json'

        response = requests.request(method.value, f'{self.BASE_URL}{url}', headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT, data=body)

        return response


    def get_ids_from_artist_spotify_url(self, spotify_url: str) -> List[str]:
        url = f'/url?resource={spotify_url}&inc=artist-rels'
        response = self.query_music_brainz_api(url=url)

        response_data = response.json()

        return [ d['artist']['id'] for d in response_data['relations'] ]

    def get_artist_info_from_artist_name(self, artist_name, min_score=100) -> List[str]:
        url = f'/artist/?query=artist:{artist_name}'
        response = self.query_music_brainz_api(url=url)

        response_data = response.json()

        return [ d for d in response_data['artists'] if d['score'] >= min_score ]


    def get_artist(self, artist_id: str) -> MusicBrainzArtistData:
        url = f'/artist/{artist_id}?inc=url-rels'
        response = self.query_music_brainz_api(url=url)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise NotFound(f'cannot find artist with id: {artist_id}')

        if 300 <= response.status_code:
            description = f'Error getting music brainz artist: [{response.status_code}] {response.text}'
            raise InternalServerError(description)

        response_data = response.json()

        spotify_ids = self._get_platform_ids_from_artist_data(PlatformName.SPOTIFY, response_data)
        tidal_ids = self._get_platform_ids_from_artist_data(PlatformName.TIDAL, response_data)

        return MusicBrainzArtistData(
            id=response_data['id'],
            name=response_data['name'],
            spotifyIds=spotify_ids,
            tidalIds=tidal_ids
        )

    def _get_platform_ids_from_artist_data(self, platform: PlatformName, artist_data) -> List[str]:
        relationships = artist_data['relations']

        ids = []

        for relation in relationships:
            if 'url' in relation and 'resource' in relation['url']:
                url = relation['url']['resource']
                if platform.value in url and "streaming" in relation['type']:
                    spotify_id = url.split('/')[-1]
                    ids.append(spotify_id)

        return ids