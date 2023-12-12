import asyncio

from database import ServerDatabase

HOST = '127.0.0.1'
PORT = 8888

db = ServerDatabase(db_path='database.db')


async def handle_post_command(params: list):
    try:
        allocated_ram, allocated_cpus, disk_memory_size, disk_id = map(int, params)
        success = db.add_client(allocated_ram, allocated_cpus, disk_memory_size, disk_id)
        if success:
            return f"Client added successfully! Disk ID: {disk_id}"
        else:
            return f"Client with the same Disk ID {disk_id} already exists."
    except (ValueError, IndexError):
        return 'Invalid params for POST command'


async def process_command(command: str, params: list):
    if command == 'POST':
        return await handle_post_command(params)


# async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
#     try:
#         while True:
#             data_str = ""
#             while True:
#                 chunk = await reader.read(100)
#                 if not chunk:
#                     break
#                 data_str += chunk.decode()
#                 if '\n' in data_str:
#                     break
#
#             command, *params = data_str.strip().split(" ")
#             response = await process_command(command, params)
#
#             if response:
#                 writer.write(response.encode())
#                 await writer.drain()
#
#     finally:
#         print("Closing the connection")
#         writer.close()
#         await writer.wait_closed()

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = None

    while data != b'quit':
        data = await reader.read(256)
        msg = data.decode()
        addr, port = writer.get_extra_info('peername')
        print(f'Message from {addr}:{port}: {msg!r}')

        writer.write(data)
        await writer.drain()

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
