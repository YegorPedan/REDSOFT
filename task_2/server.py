import asyncio
import sqlite3


conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        ram INTEGER NOT NULL,
        cpu INTEGER NOT NULL,
        disk_capacity INTEGER NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS disks (
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        disk_id TEXT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
''')
conn.commit()
conn.close()