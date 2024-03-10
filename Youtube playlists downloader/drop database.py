import sqlite3

def drop_videos_table():
    """
    Drop the 'videos' table from the SQLite database.
    """
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS videos")
    conn.commit()
    conn.close()
drop_videos_table()