"""entry point"""

import json
import pathlib
import sys
from urllib.parse import parse_qs, urlparse

import yt_dlp
from src.album import Album
from src.track import Tracks


def read_config() -> dict:
    """read config file"""
    pwd = pathlib.Path(__file__).parent.resolve()
    try:
        with open(pwd / "config.json", "r", encoding="utf-8") as config_file:
            config = json.loads(config_file.read())
    except FileNotFoundError:
        config = {}

    return config


def query_yt(url):
    """extract available playlists from url using yt-dlp"""
    yt_obs = {
        "skip_download": True,
        "ignoreerrors": True,
        "extract_flat": True,
    }
    response = yt_dlp.YoutubeDL(yt_obs).extract_info(url)
    playlists = [i["id"] for i in response["entries"]]

    return playlists


def get_playlist_ids(first_arg) -> list[str]:
    """get playlist IDs from first argument"""
    path = urlparse(first_arg).path
    if path.endswith("/playlists") or path.endswith("/releases"):
        playlists = query_yt(first_arg)
        return playlists

    qs = urlparse(first_arg).query
    if not qs:
        return [first_arg]

    lists = parse_qs(qs).get("list")
    if lists:
        return lists

    raise ValueError("failed to parse arg")


if __name__ == "__main__":
    CONFIG = read_config()
    PLAYLIST_IDS = get_playlist_ids(sys.argv[1])
    for PLAYLIST_ID in PLAYLIST_IDS:
        TRACK_LIST = Album(PLAYLIST_ID).get_tracklist()
        Tracks(TRACK_LIST, config=CONFIG).download_tracks()
