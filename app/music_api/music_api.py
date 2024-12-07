from typing import Protocol

from app.music_api.artist_data import ArtistData

class MusicAPI(Protocol):

    def get_artist(self, artist_id: str) -> ArtistData:
        ...