import asyncio
from asyncio import AbstractEventLoop

from database import ServerDatabase

HOST = '0.0.0.0'
PORT = 8888


class ChatServer:

    def __init__(self, async_loop: AbstractEventLoop, host: str, port: int):
        self.loop = async_loop
        self.db = ServerDatabase(db_path='database.db')
        self.active_clients = []
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
        print(f'Username: {username}, Password: {password}')

        if bool(user_id := self.db.is_client_exists(username, password)):
            writer.write(b'Successfully authenticated')
        else:
            writer.write(b'Authentication failed. Please try again.')
        await asyncio.sleep(1)
        return user_id

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

    async def get_all_active_clients(self, writer: asyncio.StreamWriter):
        pass

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        is_authenticated = False

        while not is_authenticated:
            is_authenticated = await self.authenticate_client(reader, writer)
        await self.add_client_to_database(reader, writer)

        while True:
            query = (await reader.read(256)).decode()

            if query == 'get_all_active_clients':
                await self.get_all_active_clients(writer)

    async def run_server_forever(self):
        async with self.server:
            await self.server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    server = ChatServer(loop, HOST, PORT)
    loop.run_until_complete(server.run_server_forever())
