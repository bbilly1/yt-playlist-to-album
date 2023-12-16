"""entry point"""

import sys

from src.album import Album
from src.track import Tracks


if __name__ == "__main__":
    PLAYLIST_ARG = sys.argv[1]
    TRACK_LIST = Album(PLAYLIST_ARG).get_tracklist()
    Tracks(TRACK_LIST).download_tracks()
