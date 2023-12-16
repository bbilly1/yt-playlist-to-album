"""extract album metadata"""

import requests
import yt_dlp
from src.static_types import AlbumType, TrackType


class Album:
    """interact with an album"""

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.response: dict = {}

    def get_tracklist(self) -> list[TrackType]:
        """build list of tracks in album"""
        self.get_metadata()
        album: AlbumType = self.get_album()
        track_list: list[TrackType] = self.build_tracks(album)

        return track_list

    def get_metadata(self) -> None:
        """get yt metadata"""
        yt_obs = {
            "skip_download": True,
            "ignoreerrors": True,
            "extract_flat": True,
            "check_formats": "selected",
        }
        url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.response = yt_dlp.YoutubeDL(yt_obs).extract_info(url)

    def get_album(self) -> AlbumType:
        """build album"""
        if self.response.get("channel"):
            artist = self.response["channel"]
        else:
            artist = input("artist: ")

        year = input("year: ")

        album: AlbumType = {
            "artist": artist,
            "name": self.response["title"],
            "year": year,
            "total_tracks": len(self.response["entries"]),
            "cover_art": self.get_thumbnail(self.response),
        }

        return album

    def get_thumbnail(self, response) -> str:
        """find best thumb"""

        playlist_thumbs = response["thumbnails"]
        playlist_thumbs.reverse()
        for thumb in playlist_thumbs:
            width, height = [int(i) for i in playlist_thumbs[-1]["resolution"].split("x")]
            if width == height and requests.head(thumb["url"], timeout=60).ok:
                return thumb["url"]

        raise ValueError("no thumb found")

    def build_tracks(self, album: AlbumType) -> list[TrackType]:
        """build album tracks"""

        track_list: list[TrackType] = []

        for idx, entry in enumerate(self.response["entries"]):
            track: TrackType = {
                "title": entry["title"],
                "track_nr": idx + 1,
                "video_id": entry["id"],
                "album": album,
            }
            track_list.append(track)

        return track_list
