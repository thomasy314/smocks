from dataclasses import asdict, dataclass
from typing import List, Optional


@dataclass
class SpotifyArtistData():
    id: str
    name: str
    url: str
    popularity: int
    followers: int
    monthly_listeners: int

@dataclass
class TidalArtistData():
    id: str
    name: str
    url: str
    popularity: float

@dataclass
class MusicBrainzArtistData():
    id: str
    name: str
    spotifyIds: List[str]
    tidalIds: List[str]
    
@dataclass
class ArtistData():
    id: str
    name: str
    spotify: Optional[SpotifyArtistData] = None
    tidal: Optional[TidalArtistData] = None
    musicBrainz: Optional[MusicBrainzArtistData] = None
    
    @property
    def serialize(self):
        return asdict(self)

    @property
    def smock_price(self):
        return self.spotify.popularity