# YouTube Playlist to Album

Download music playlist as an audio album, using yt-dlp.

## State and Intent
Just sharing a little CLI helper script I wrote for myself, maybe it will be useful to you too. Don't expect any support or feature development.

## Core functionality
This will create a Folder structure like so in your cwd:

`{artist}/{album}/{nr} - {title}.mp3`

Write metadata to the mp3 file:
- Title
- Artist
- Album
- Year
- Track nr
- Track total
- Cover Art

## Install
Install required libraries, e.g to run in an virtual environment:
```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Run
Pass the Playlist ID (just the Playlist ID) as a first argument to `main.py`, e.g.:

```
main.py <playlist-id>
```

This uses the free [musicbrainz.org](https://musicbrainz.org) API to validate and gather metadata information.

When in doubt, you'll get prompted to manually enter the `Artist` name, the playlist title will become the Album, track title will be the video title, cover art will be the video thumbnail of the first video in the playlist.
