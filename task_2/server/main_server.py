import asyncio
from asyncio import AbstractEventLoop
from hashlib import sha256
import configparser

from database import ServerDatabase

SALT = 'SOFT'


class ChatServer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChatServer, cls).__new__(cls)

        return cls._instance

    def __init__(self, async_loop: AbstractEventLoop, host: str, port: int):
        self.loop = async_loop
        self.db = ServerDatabase(db_path='database.db')
        self.active_clients = set()
        self.server = self.loop.run_until_complete(
            asyncio.start_server(
                self.handle_client, host, port
            )
        )

    async def insert_client_to_database(self, allocated_ram: str, allocated_cpus: str, disk_memory: str, disk_id: str):
        status = self.db.add_client(allocated_ram, allocated_cpus, disk_memory, disk_id)
        print(status)

    async def authenticate_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> int:
        writer.write(b'Enter username: ')
        await writer.drain()
        username = (await reader.read(256)).decode()
        writer.write(b'Enter password: ')
        await writer.drain()
        password = (await reader.read(256)).decode()
        password_hash = sha256((password + SALT).encode()).hexdigest()
        print(f'Username: {username}, Password: {password_hash}')

        if bool(user := self.db.is_client_exists(username, password_hash)):
            writer.write(b'Successfully authenticated')
        else:
            writer.write(b'Authentication failed. Please try again.')
        await asyncio.sleep(1)
        return user

    async def add_client_to_database(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(256)
        msg = data.decode()

        msg_data = msg.split()
        if msg_data[0] == 'add_client':
            await self.insert_client_to_database(msg_data[1], msg_data[2], msg_data[3], str(msg_data[4]))

        addr, port = writer.get_extra_info('peername')
        print(f'Message from {addr}:{port}: {msg!r}')

        writer.write(data)
        await writer.drain()

    async def get_all_active_clients(self):
        result = self.db.get_machines_for_users(self.active_clients)
        return result

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        user = False

        while not user:
            user = await self.authenticate_client(reader, writer)
        else:
            self.active_clients.add(user[0])
        await self.add_client_to_database(reader, writer)

        while True:
            query = (await reader.read(256)).decode()

            if query == 'get_all_active_clients':
                result = await self.get_all_active_clients()
                print(result)

    async def run_server_forever(self):
        async with self.server:
            await self.server.serve_forever()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    HOST = config['SERVER']['HOST']
    PORT = config['SERVER']['PORT']
    loop = asyncio.new_event_loop()
    server = ChatServer(loop, HOST, int(PORT))
    loop.run_until_complete(server.run_server_forever())