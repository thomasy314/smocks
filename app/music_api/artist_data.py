from dataclasses import dataclass
from typing import Union, Optional

@dataclass
class SpotifyArtistData():

    id: str
    url: str
    popularity: Union[int, float]
    followers: int

@dataclass
class ArtistData():

    id: str
    name: str
    spotify: Optional[SpotifyArtistData] = None
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'spotify': {
                'url': self.spotify.url,
                'followers': self.spotify.followers,
                'popularity': self.spotify.popularity
            }
        }

    @property
    def smock_price(self):
        return self.spotify.popularity