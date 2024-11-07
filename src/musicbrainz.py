"""get metadata from musicbrainz.org"""

import requests

from src.static_types import AlbumType, TrackType


class Brainz:
    """handler"""

    API_BASE = "https://musicbrainz.org/ws/2"
    API_TAIL = "fmt=json"

    def make_request(self, query: str) -> dict:
        """make request to API"""
        url = f"{self.API_BASE}/{query}&{self.API_TAIL}"
        response = requests.get(url, timeout=60)
        if not response.ok:
            print(response.text)
            raise ConnectionError

        return response.json()

    def get_release_id(self, artist: str, album_name: str) -> AlbumType | None:
        """get release id"""
        album = self._make_album_request(artist, album_name)
        if not album:
            artist = input("artist: ").strip()

        album = self._make_album_request(artist, album_name)

        return album

    def _make_album_request(self, artist: str, album_name: str) -> AlbumType | None:
        """get release id"""
        query = f"release?query=artist:{artist},release:{album_name}"
        response = self.make_request(query)

        for release in response["releases"]:
            if not "date" in release:
                continue
            if not album_name.lower() == release["title"].lower():
                continue

            artist_cred = [i["name"].lower() for i in release["artist-credit"]]
            if not artist.lower() in artist_cred:
                continue

            album: AlbumType = {
                "album_id": release["id"],
                "name": release["title"],
                "artist": artist,
                "year": release["date"].split("-")[0],
                "total_tracks": release["track-count"],
                "cover_art": None,
            }
            return album

        return None

    def get_track_list(self, album: AlbumType) -> list[TrackType]:
        """get list of tracks in release"""
        release_id = album["album_id"]
        query = f"release/{release_id}?inc=recordings&limit=1"
        response = self.make_request(query)
        tracks = response["media"][0]["tracks"]

        track_list: list[TrackType] = []

        for track_data in tracks:
            track: TrackType = {
                "title": track_data["title"],
                "track_nr": track_data["position"],
                "album": album,
                "youtube_id": None,
                "track_id": track_data["id"],
            }
            track_list.append(track)

        return track_list
