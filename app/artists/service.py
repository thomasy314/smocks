from datetime import datetime, timedelta, timezone

from app.music_api.artist_data import ArtistData
from app.music_api.music_api import MusicAPI


class ArtistService():

    def __init__(self, music_api=MusicAPI):
        self.music_api = music_api()
        # TODO: use db instead of storing state here
        self.artist_data_ttl = timedelta(hours=1)
        self.artist_data = {}
        self.artist_data_expiration = {}

    def get_artist_from_id(self, artist_id):

        current_time = datetime.now(timezone.utc)
        if (artist_id in self.artist_data 
            and artist_id in self.artist_data_expiration 
            and self.artist_data_expiration[artist_id] > current_time):
            return self.artist_data[artist_id]
        else:
            artist_info: ArtistData = self.music_api.get_artist(artist_id)
            self.artist_data[artist_id] = artist_info
            self.artist_data_expiration[artist_id] = current_time + self.artist_data_ttl
            return artist_info 

artistService = ArtistService()