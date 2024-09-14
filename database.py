import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS document_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        vector_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_request (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        request_count INTEGER DEFAULT 0
    )
''')

conn.commit()
conn.close()
