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

    Downloaded BOOLEAN

    );

    """)
    connection.commit()
    connection.close()
