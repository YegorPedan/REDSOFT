import sqlite3
import os


class ServerDatabase:
    def __init__(self, db_path=':memory:'):
        self.cursor = None
        self.connection = None
        self.db_path = db_path
        self.connect()
        self.create_table_if_not_exists()

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def create_table_if_not_exists(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id INTEGER PRIMARY KEY,
                allocated_ram INTEGER,
                allocated_cpus INTEGER,
                disk_memory_size INTEGER,
                disk_id VARCHAR(256) UNIQUE
            );
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username VARCHAR(256),
        password VARCHAR(256),
        client_id INTEGER,
        FOREIGN KEY (client_id) REFERENCES clients(id)
        );
        """)
        self.connection.commit()

    def add_client(self, allocated_ram: str, allocated_cpus: str, disk_memory_size: str, disk_id: str) -> bool:
        status = True
        try:
            self.cursor.execute(
                """INSERT INTO clients (allocated_ram, allocated_cpus, disk_memory_size, disk_id)
                VALUES (?, ?, ?, ?);""", (allocated_ram, allocated_cpus, disk_memory_size, disk_id)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            status = False
        return status

    def get_all_clients(self):
        self.cursor.execute('SELECT * FROM clients;')
        return self.cursor.fetchall()

    def is_client_exists(self, username: str, password: str):
       self.cursor.execute('SELECT * FROM users WHERE username=? and password=?', (username, password))
       return self.cursor.fetchone()



