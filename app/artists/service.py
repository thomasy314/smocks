from app.music_api.music_api import MusicAPI

from app.music_api import musicAPI

class ArtistService():

    def __init__(self, music_api: MusicAPI):
        self.music_api = music_api

    def get_artist_from_id(self, artist_id):

        artist_info = self.music_api.get_artist(artist_id)

        return artist_info 

artistService = ArtistService(musicAPI)