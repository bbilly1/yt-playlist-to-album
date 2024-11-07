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
        if not album:
            album = self._custom_album(artist)

        album.update(
            {
                "cover_art": self.get_thumbnail()
            }
        )

        return album

    def _custom_album(self, artist: str) -> AlbumType:
        """manual input for album"""
        album: AlbumType = {
            "album_id": None,
            "name": self.response["title"],
            "artist": artist,
            "year": None,
            "total_tracks": len(self.response["entries"]),
            "cover_art": None,
        }
        return album

    def get_thumbnail(self) -> str:
        """find best thumb"""
        playlist_thumbs = self.response["thumbnails"]
        playlist_thumbs.reverse()
        for thumb in playlist_thumbs:
            width, height = [int(i) for i in playlist_thumbs[-1]["resolution"].split("x")]
            if width == height and requests.head(thumb["url"], timeout=60).ok:
                return thumb["url"]

        return playlist_thumbs[-1]["url"]

    def build_tracks(self, album: AlbumType) -> list[TrackType]:
        """build album tracks"""
        if album["album_id"]:
            track_list: list[TrackType] = Brainz().get_track_list(album)
            entries = [(i["title"], i["id"]) for i in self.response["entries"]]
            for track in track_list:
                youtube_id = self.find_best_match_id(entries, track["title"])
                track.update({"youtube_id": youtube_id})

        else:
            track_list: list[TrackType] = self.manual_tracks(album)

        return track_list

    def manual_tracks(self, album) -> list[TrackType]:
        """build manual tracks"""
        tracks = []
        for idx, entry in enumerate(self.response["entries"], 1):
            track = TrackType(
                title=entry["title"],
                track_nr=idx,
                youtube_id=entry["id"],
                track_id=None,
                album=album,
            )
            tracks.append(track)

        return tracks

    @staticmethod
    def find_best_match_id(entries, search_title):
        """find id"""
        best_match_id = None
        best_match_ratio = 0

        for title, youtube_id in entries:
            current_ratio = SequenceMatcher(
                None, search_title.lower(), title.lower()
            ).ratio()
            if current_ratio > best_match_ratio:
                best_match_id = youtube_id
                best_match_ratio = current_ratio

        return best_match_id
