import os
import re
import mimetypes
from pytube import YouTube, Playlist
import sqlite3
from urllib.parse import urlparse, parse_qs
from mutagen.mp4 import MP4, MP4Tags


class Database:
    def __init__(self):
        # Establishing connection with the database and creating a cursor
        self.conn = sqlite3.connect('videos.db')
        self.c = self.conn.cursor()
        # Creating a table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY, 
            name TEXT,
            found INTEGER DEFAULT 0)''')
        self.conn.commit()

    def insert_video_id(self, v_id, video_name):
        # Inserting video id and name into the database
        self.c.execute("INSERT INTO videos VALUES (?, ?, 0)", (v_id, video_name))
        self.conn.commit()

    def update_found_status(self, video_id, found_value):
        # Updating the found status of a video in the database
        self.c.execute("UPDATE videos SET found=? WHERE id=?", (found_value, video_id))
        self.conn.commit()

    def video_id_exists(self, video_id):
        # Checking if a video id exists in the database
        self.c.execute("SELECT * FROM videos WHERE id=?", (video_id,))
        result = self.c.fetchone()
        return result is not None

    def video_name_exists(self, video_name):
        # Checking if a video name exists in the database
        self.c.execute("SELECT * FROM videos WHERE name=?", (video_name,))
        result = self.c.fetchone()
        return result is not None

    def delete_rows_with_found_value_zero(self):
        # Deleting rows from the database where found value is 0
        self.c.execute("DELETE FROM videos WHERE found=0")
        self.conn.commit()

    def __del__(self):
        # Committing changes and closing the connection when the object is deleted
        self.conn.commit()
        self.conn.close()


def get_video_id(url):
    # Function to extract video id from YouTube URL
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'www.youtube.com':
        if parsed_url.path == '/watch':
            query = parse_qs(parsed_url.query)
            if 'v' in query:
                return query['v'][0]
        elif parsed_url.path.startswith('/embed/') or parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    return None


def insert_video_id_in_metadata(file_path, video_id):
    # Function to insert video id in metadata of mp4 file
    mp4file = MP4(file_path)
    tags = MP4Tags()
    tags['id'] = [video_id]
    mp4file.tags = tags
    mp4file.save()


def starts_with_arabic(text):
    # Function to check if text starts with Arabic characters
    pattern = r'^[\u0600-\u06FF]'
    return re.match(pattern, text) is not None


def download_video(video_url, file_path, db):
    # Function to download a video from YouTube
    yt = YouTube(video_url)
    vid = get_video_id(video_url)
    if db.video_id_exists(vid):
        return

    streams = yt.streams.filter(progressive=True).order_by('resolution').desc()
    best_stream = streams.first()
    full_title = yt.title.replace("/", "_")
    print(f'Downloading {full_title}...')
    file_path = best_stream.download(output_path=file_path, filename=full_title + '.mp4')
    insert_video_id_in_metadata(file_path, vid)
    db.insert_video_id(vid, yt.title)
    print(f'Video {full_title} downloaded.')


def is_video(file_path):
    # Function to check if file is a video
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('video/')


def get_video_id_tags(video):
    # Function to extract video id from video file metadata
    try:
        mp4file = MP4(video)
        t = mp4file.tags['id\x00\x00'][0]
        return t
    except Exception as e:
        return None


def refresh(set, all, db):
    # Function to refresh found status of videos in the database
    for path, _ in all.items():
        for video in os.listdir(path):
            video_full_path = os.path.join(path, video)
            if is_video(video):
                if get_video_id_tags(video_full_path) is not None:
                    db.update_found_status(get_video_id_tags(video_full_path), set)


def download_playlist(url, path, db):
    # Function to download a playlist from YouTube
    playlist = Playlist(url)
    for video_url in playlist.video_urls:
        download_video(video_url, path, db)


def main(to_be_downloaded):
    # Main function to handle downloading of playlists
    db = Database()
    refresh(1, to_be_downloaded, db)
    db.delete_rows_with_found_value_zero()
    refresh(0, to_be_downloaded, db)
    for folder_path, playlist_urls in to_be_downloaded.items():
        for playlist_url in playlist_urls:
            download_playlist(playlist_url, folder_path, db)
    refresh(0, to_be_downloaded, db)


if __name__ == '__main__':
    # Define the playlists to be downloaded and call the main function
    to_be_downloaded = {
        'folderPath1': [
            'playlist1 link',
            'playlist2 link',

        ], 'folderPath2': [
            'playlist1 link',
            'playlist2 link',
        ]
    }
    main(to_be_downloaded)
