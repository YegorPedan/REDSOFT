import asyncio
from asyncio import AbstractEventLoop

from database import ServerDatabase

HOST = '0.0.0.0'
PORT = 8888


class ChatServer:

    def __init__(self, async_loop: AbstractEventLoop, host: str, port: int):
        self.loop = async_loop
        self.db = ServerDatabase(db_path='database.db')
        self.server = self.loop.run_until_complete(
            asyncio.start_server(
                self.handle_client, host, port
            )
        )

    async def add_client_to_database(self, allocated_ram: str, allocated_cpus: str, disk_memory: str, disk_id: str):
        status = self.db.add_client(allocated_ram, allocated_cpus, disk_memory, disk_id)
        print(status)

    async def authenticate_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:
        is_authenticated = False
        writer.write(b'Enter username: ')
        await writer.drain()
        username = (await reader.read(256)).decode()
        writer.write(b'Enter password: ')
        await writer.drain()
        password = (await reader.read(256)).decode()
        print(f'Username: {username}, Password: {password}')

        if bool(self.db.is_client_exists(username, password)):
            writer.write(b'Successfully authenticated')
            is_authenticated = True
        else:
            writer.write(b'Authentication failed. Please try again.')
        await asyncio.sleep(1)
        return is_authenticated

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        is_authenticated = False

        while not is_authenticated:
            is_authenticated = await self.authenticate_client(reader, writer)

        data = await reader.read(256)
        while True:
            msg = data.decode()

            msg_data = msg.split()
            if is_authenticated:
                if msg_data[0] == 'add_client':
                    await self.add_client_to_database(msg_data[1], msg_data[2], msg_data[3], str(msg_data[4]))

                addr, port = writer.get_extra_info('peername')
                print(f'Message from {addr}:{port}: {msg!r}')

                writer.write(data)
                await writer.drain()
            else:
                await asyncio.sleep(1)
                writer.write(b'Enter username: ')
                username = await reader.read(256)
                print(username)
            data = await reader.read(256)

    async def run_server_forever(self):
        async with self.server:
            await self.server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    server = ChatServer(loop, HOST, PORT)
    loop.run_until_complete(server.run_server_forever())
