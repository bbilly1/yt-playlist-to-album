"""all typed dics"""

from typing import TypedDict


class AlbumType(TypedDict):
    """describes an album"""

    artist: str
    name: str
    year: str
    total_tracks: int
    cover_art: str


class TrackType(TypedDict):
    """describes a track"""

    title: str
    track_nr: int
    video_id: str
    album: AlbumType
