"""extract album metadata"""

from difflib import SequenceMatcher

import requests
import yt_dlp
from src.musicbrainz import Brainz
from src.static_types import AlbumType, TrackType


class Album:
    """interact with an album"""

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.response: dict = {}

    def get_tracklist(self) -> list[TrackType]:
        """build list of tracks in album"""
        self.get_yt_metadata()
        album: AlbumType = self.get_album()
        track_list: list[TrackType] = self.build_tracks(album)

        return track_list

    def get_yt_metadata(self) -> None:
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
        """identify album from playlist"""
        if self.response.get("channel"):
            artist = self.response["channel"]
        else:
            artist = self.response["entries"][0]["channel"]

        album_name = self.response["title"]
        album: AlbumType = Brainz().get_release_id(artist, album_name)
        album.update(
            {
                "cover_art": self.get_thumbnail(self.response)
            }
        )

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

        track_list: list[TrackType] = Brainz().get_track_list(album)
        entries = [(i["title"], i["id"]) for i in self.response["entries"]]

        for track in track_list:
            video_id = self.find_best_match_id(entries, track["title"])
            track.update({"video_id": video_id})

        return track_list

    @staticmethod
    def find_best_match_id(entries, search_title):
        """find id"""
        best_match_id = None
        best_match_ratio = 0

        for title, video_id in entries:
            current_ratio = SequenceMatcher(
                None, search_title.lower(), title.lower()
            ).ratio()
            if current_ratio > best_match_ratio:
                best_match_id = video_id
                best_match_ratio = current_ratio

        return best_match_id
