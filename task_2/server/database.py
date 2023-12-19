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

    def create_table_if_not_exists(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username VARCHAR(256),
        password VARCHAR(256)
        );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id INTEGER PRIMARY KEY,
                allocated_ram INTEGER,
                allocated_cpus INTEGER,
                disk_memory_size INTEGER,
                disk_id VARCHAR(256) UNIQUE,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
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

    def get_machines_for_users(self, user_ids: set):
        placeholders = ', '.join([str(user_id) for user_id in user_ids])

        # Use parameterized query to avoid SQL injection
        query = f"""SELECT clients.id, allocated_ram, allocated_cpus, disk_memory_size, disk_id FROM clients
        inner join users ON users.id == clients.user_id AND users.id in ({placeholders})"""

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result
