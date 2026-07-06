import sqlite3;

def initialize_database():
    connection = sqlite3.connect("MetaDataLog.db")
    #Cursor is like a messenger
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Log(

    SongId TEXT PRIMARY KEY,

    Title TEXT Not Null,

    Artist TEXT Not Null,

    Album TEXT Not Null,

    Year INTEGER,

    Duration INTEGER Not Null,
                   
    ISRC TEXT Not Null,

    Downloaded BOOLEAN

    );

    """)
    connection.commit()
    connection.close()

def log_track(song_id, title, artist, album, year, duration, isrc, downloaded):
    connection = sqlite3.connect("MetaDataLog.db")
    #Cursor is like a messenger
    cursor = connection.cursor()
    # Pushing the values from the python *ignoring how the song is formatted if its weirdly formatted* into the table
    # INSERT OR IGNORE INTO tells the computer to simply add or skip (if its a duplicate)
    cursor.execute("""
    INSERT OR IGNORE INTO Log (SongId, Title, Artist, Album, Year, Duration, ISRC, Downloaded)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)              
    """, (song_id, title, artist, album, year, duration, isrc, downloaded))
    was_added = (cursor.rowcount == 1)
    
    return was_added  # Return True if the track was added, False if it was ignored (duplicate)
    connection.commit()
    connection.close()
