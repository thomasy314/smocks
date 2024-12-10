from dataclasses import dataclass
from typing import Union, Optional

@dataclass
class SpotifyArtistData():
    id: str
    url: str
    popularity: int
    followers: int

@dataclass
class TidalArtistData():
    id: str
    url: str
    popularity: float

@dataclass
class MusicBrainzData():
    id: str
    
@dataclass
class ArtistData():
    id: str
    name: str
    spotify: Optional[SpotifyArtistData] = None
    tidal: Optional[TidalArtistData] = None
    musicBrainz: Optional[MusicBrainzData] = None
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'spotify': {
                'url': self.spotify.url,
                'followers': self.spotify.followers,
                'popularity': self.spotify.popularity
            },
            'tidal': {
                'id': self.tidal.id,
                'url': self.tidal.url,
                'popularity': self.tidal.popularity
            }
        }

    @property
    def smock_price(self):
        return self.spotify.popularity