"""entry point"""

import sys
from urllib.parse import parse_qs, urlparse

from src.album import Album
from src.track import Tracks


def get_playlist_id(first_arg):
    """get playlist ID from first argument"""
    qs = urlparse(first_arg).query
    if not qs:
        return first_arg

    lists = parse_qs(qs).get("list")
    if not lists:
        raise ValueError("didn't find list key in qs")

    return lists[0]


if __name__ == "__main__":
    PLAYLIST_ID = get_playlist_id(sys.argv[1])
    TRACK_LIST = Album(PLAYLIST_ID).get_tracklist()
    Tracks(TRACK_LIST).download_tracks()
