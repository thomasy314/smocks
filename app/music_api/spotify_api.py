import datetime
import re
import time
from dataclasses import dataclass
from http import HTTPMethod, HTTPStatus
from typing import List

import requests
from bs4 import BeautifulSoup
from werkzeug.exceptions import InternalServerError, NotFound

from app.music_api.artist_data import SpotifyArtistData
from app.music_api.spotify_credentials import SpotifyAuth
from config import DEFAULT_REQUEST_TIMEOUT


@dataclass
class ScrapedSpotifyArtistData():
    monthly_listeners: int

class SpotifyAPI():

    WEBSITE_URL: str = 'https://open.spotify.com'
    API_URL: str = 'https://api.spotify.com/v1'
    retry_after: float = 0

    def __init__(self, Auth=SpotifyAuth):
        self.auth = Auth()

    def query_spotify_api(self, url: str, method: HTTPMethod = HTTPMethod.GET, headers={}, params=None, body=None):

        if time.time() <= self.retry_after:
            formatted_retry_after_time = datetime.datetime.fromtimestamp(self.retry_after, datetime.timezone.utc).isoformat(timespec='seconds')
            raise InternalServerError(f'Too many requests to spotify api. Wait {retry_after_seconds} seconds until {formatted_retry_after_time}')

        headers['Accept'] = "application/json"
        response = requests.request(method.value, f'{self.API_URL}{url}', headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT, params=params, data=body)

        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            retry_after_seconds = response.headers['Retry-After']
            self.retry_after = time.time() + retry_after_seconds
            formatted_retry_after_time = datetime.datetime.fromtimestamp(self.retry_after, datetime.timezone.utc).isoformat(timespec='seconds')
            raise InternalServerError(f'Too many requests to spotify api. Wait {retry_after_seconds} seconds until {formatted_retry_after_time}')

        return response

    def get_artist(self, artist_id: str) -> SpotifyArtistData:
        api_data = self.get_raw_artists([artist_id])[0]
        scraped_data = self.get_scraped_artist(artist_id)


        return SpotifyArtistData(
            id=api_data['id'],
            name=api_data['name'],
            url=api_data['external_urls']['spotify'], 
            followers=api_data['followers']['total'],
            popularity=api_data['popularity'],
            monthly_listeners=scraped_data.monthly_listeners
        )

    def get_artists(self, artist_ids: List[str]) -> SpotifyArtistData:
        api_data = self.get_raw_artists(artist_ids)

        def add_scrapped_data_and_format(data):
            scraped_data = self.get_scraped_artist(data['id'])
            return SpotifyArtistData(
                id=data['id'],
                name=data['name'],
                url=data['external_urls']['spotify'], 
                followers=data['followers']['total'],
                popularity=data['popularity'],
                monthly_listeners=scraped_data.monthly_listeners
            )

        return list(map(add_scrapped_data_and_format, api_data))

    def get_raw_artists(self, artist_ids: List[str]) -> List[object]:
        headers = {
            'Authorization': f'Bearer {self.auth.get_spotify_token()}'
        }
        params = {
            'ids': ','.join(artist_ids)
        }
        url = f'/artists'
        response = self.query_spotify_api(url=url, headers=headers, params=params)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise NotFound(f'cannot find an artist with id in: [{artist_ids}]')

        if 300 <= response.status_code:
            raise Exception(f'Error getting spotify artist: [{response.status_code}] {response.text}')

        return response.json()['artists']

    def get_scraped_artist(self, artist_id: str) -> ScrapedSpotifyArtistData:
        url = f'{self.WEBSITE_URL}/artist/{artist_id}'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, features='lxml')

        listener_text = soup.find(class_="ovtJYocZljdWcU1FLBL5").text

        scrapedData = ScrapedSpotifyArtistData(
            monthly_listeners=int(''.join(re.findall("[0-9]+", listener_text)))
        )

        return scrapedData

