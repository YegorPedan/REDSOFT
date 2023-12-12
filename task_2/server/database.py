import psycopg2
import os


class ServerDatabase:
    def __init__(self, db_name: str, user: str, password: str, host: str, port: str):
        self.connection = None
        self.cursor = None
        self.connection_params = {
            'dbname': os.getenv('DB_NAME') or db_name,
            'user': os.getenv('USER') or user,
            'password': os.getenv('PASSWORD') or password,
            'host': os.getenv('HOST') or host,
            'port': os.getenv('PORT') or port,
        }
        self.connect()

    def connect(self):
        self.connection = psycopg2.connect(**self.connection_params)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
