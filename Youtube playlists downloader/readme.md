# YouTube Playlist Downloader

## Overview
This Python script facilitates the download of YouTube playlists, storing relevant metadata in a SQLite database, and embedding video IDs into downloaded MP4 files' metadata. It's particularly useful for organizing and archiving online educational content.

## Features
- **Playlist Download**: Downloads videos from specified YouTube playlists.
- **Database Management**: Utilizes a SQLite database to manage downloaded videos and prevent duplicate downloads.
- **Metadata Embedding**: Embeds video IDs into downloaded MP4 files' metadata for easy identification and management.
- **Customizable**: Easily adaptable for different playlists and storage locations.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- pytube library (`pip install pytube`)
- mutagen library (`pip install mutagen`)

## Usage
1. Clone the repository or download the script file.
2. Ensure all prerequisites are met.
3. Modify the `to_be_downloaded` dictionary in the script to specify the playlists and destination folders.
4. Run the script using Python: `python youtube_playlist_downloader.py`

## `to_be_downloaded` Structure
The `to_be_downloaded` dictionary defines the playlists to be downloaded and their corresponding destination folders. Follow the format:
```python
to_be_downloaded = {
    'folderPath1': [
        'playlist1 link',
        'playlist2 link',
    ],
    'folderPath2': [
        'playlist3 link',
        'playlist4 link',
    ]
}
