import asyncio

from database import ServerDatabase

HOST = '0.0.0.0'
PORT = 8888

db = ServerDatabase(db_path='database.db')


async def add_client_to_database(allocated_ram: str, allocated_cpus: str, disk_memory: str, disk_id: int):
    status = await db.add_client(allocated_ram, allocated_cpus, disk_memory, disk_id)
    print(status)


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    is_authenticated = False
    data = None

    writer.write(b'Login or registrate before using command!')
    while data != b'quit':
        data = await reader.read(256)
        msg = data.decode()

        msg_data = msg.split()
        if is_authenticated:
            if msg_data[0] == 'add_client':
                await add_client_to_database(msg_data[1], msg_data[2], msg_data[3], msg_data[4])

            addr, port = writer.get_extra_info('peername')
            print(f'Message from {addr}:{port}: {msg!r}')

            writer.write(data)
            await writer.drain()
        else:
            pass

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_client, HOST, PORT,
    )
    addr = server.sockets[0].getsockname()
    print(f'Server on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
