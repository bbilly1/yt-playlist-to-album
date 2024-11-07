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
Pass one of the following as a first argument to the `main.py` script to either download a single album or all available in bulk:

- Playlist ID: `PLxxxxxxxxxxxx`
- Playlist URL: `https://www.youtube.com/playlist?list=PLxxxxxxxxxxxx`
- Channel Playlist Page: `https://www.youtube.com/@artist/playlists`
- Channel Release Page: `https://www.youtube.com/@artist/releases`

```
main.py <playlist-id> | <playlist-url> | <channel-playlist-page> | <channel-release-page>
```

This uses the free [musicbrainz.org](https://musicbrainz.org) API to validate and gather metadata information.

When in doubt, you'll get prompted to manually enter the `Artist` name, the playlist title will become the Album, track title will be the video title, cover art will be the video thumbnail of the first video in the playlist.

If there is no match on [musicbrainz.org](https://musicbrainz.org), the data from YT will be taken as is without trying to identify the tracks.

If you download from /playlists or /releases pages, the scripts assumes, the artist stays the same.

## Config file
Optionally you can create a `config.json` file in the project folder. The following keys are supported:

- `sleep` (int): Sleep seconds, will be randomized with +/- 50%. 
- `yt_obs_append` (dict): yt-dlp options to append for download.
