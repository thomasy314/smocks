from functools import reduce
from pprint import pprint

from app.music_api.artist_data import (
    ArtistData,
    MusicBrainzArtistData,
    SpotifyArtistData,
    TidalArtistData,
)
from app.music_api.musicbrainz_api import MusicBrainzAPI
from app.music_api.spotify_api import SpotifyAPI
from app.music_api.tidal_api import TidalAPI


class MusicAPI():

    def __init__(self, spotify_api=SpotifyAPI, tidal_api=TidalAPI, music_brainz_api=MusicBrainzAPI):
        self.spotifyApi = spotify_api()
        self.tidalApi = tidal_api()
        self.musicBrainzApi = music_brainz_api()

    def get_artist(self, music_brainz_id: str) -> ArtistData:
        music_brainz_data: MusicBrainzArtistData = self.musicBrainzApi.get_artist(music_brainz_id)
        spotify_ids = music_brainz_data.spotifyIds
        tidal_ids = music_brainz_data.tidalIds

        def find_artist_data(acc, data):
            if data.name == music_brainz_data.name:
                return data
            return None

        # TODO Async these call
        spotify_data = reduce(find_artist_data, self.spotifyApi.get_artists(spotify_ids), None) 
        tidal_data = reduce(find_artist_data, self.tidalApi.get_artists(tidal_ids), None)

        return ArtistData(
            id=music_brainz_data.id,
            name=music_brainz_data.name,
            spotify=spotify_data,
            tidal=tidal_data,
            musicBrainz=music_brainz_data
        )