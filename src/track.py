"""download tracks"""

import requests
import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from src.static_types import TrackType


class Tracks:
    """represent album tracks"""

    def __init__(self, track_list: list[TrackType]):
        self.track_list = track_list
        self.cover_art: bytes = bytes()

    def get_cover_art(self) -> None:
        """get cover art binary"""
        url = self.track_list[0]["album"].get("cover_art")
        if url:
            self.cover_art = requests.get(url, timeout=60).content

    def download_tracks(self) -> None:
        """download album tracks"""
        self.get_cover_art()
        for track in self.track_list:
            audio_path: str = self.download_single(track)
            self.write_metadata(track, audio_path)

    def download_single(self, track: TrackType) -> str:
        """download single video"""
        artist = self._str_cleaner(track["album"]["artist"])
        album = self._str_cleaner(track["album"]["name"])
        track_nr = str(track.get("track_nr")).zfill(2)
        title = self._str_cleaner(track["title"])
        template = f"{artist}/{album}/{track_nr} - {title}"
        yt_obs = {
            "format": "bestaudio/best",
            "extractaudio": True,
            "audioformat": "mp3",
            "outtmpl": template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        yt_dlp.YoutubeDL(yt_obs).download(track.get("youtube_id"))

        return f"{template}.mp3"

    @staticmethod
    def _str_cleaner(input_string) -> str:
        """clean string for filesystem"""
        invalid_chars = ["/", "%", ":", "\\", "|", "<", ">", "?", "*"]
        cleaned_string = "".join(
            [char for char in input_string if char not in invalid_chars]
        )
        return cleaned_string

    def write_metadata(self, track: TrackType, audio_path: str) -> None:
        """write metadata to track"""
        track_nr = track.get("track_nr")
        total_tracks = track["album"].get("total_tracks")

        audio = EasyID3(audio_path)
        audio["title"] = track.get("title")
        audio["artist"] = track["album"].get("artist")
        audio["albumartist"] = track["album"].get("artist")
        audio["album"] = track["album"].get("name")
        audio["date"] = track["album"].get("year")
        audio["tracknumber"] = f"{track_nr}/{total_tracks}"
        audio["musicbrainz_trackid"] = track["track_id"]
        audio["musicbrainz_albumid"] = track["album"].get("album_id")
        audio["website"] = f"https://www.youtube.com/watch?v={track['youtube_id']}"
        audio.save()

        cover_handler = ID3(audio_path)
        cover_handler["APIC"] = APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=self.cover_art
        )

        cover_handler.save()
