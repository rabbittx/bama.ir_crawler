import sqlite3

# Create a SQLite database (if it doesn't exist)
conn = sqlite3.connect('bama_ads.db')
cursor = conn.cursor()

# Create a table to store the data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        link TEXT,
        model TEXT,
        date TEXT,
        type TEXT,
        year TEXT,
        used TEXT,
        gear TEXT,
        badges TEXT,
        price TEXT,
        city TEXT,
        address TEXT
    )
''')

conn.commit()
conn.close()
