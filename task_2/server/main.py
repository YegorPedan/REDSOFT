import asyncio

from database import ServerDatabase

db = ServerDatabase(db_path='database.db')


async def handle_post_command(params: list):
    try:
        allocated_ram, allocated_cpus, disk_memory_size, disk_id = map(int, params)
        success = db.add_client(allocated_ram, allocated_cpus, disk_memory_size, disk_id)
    except (ValueError, IndexError):
        return 'Invalid params for POST command'


async def process_command(command: str, params: list):
    if command == 'POST':
        return await handle_post_command(params)


async def handle_client(reader, writer):
    try:
        while True:
            data_str = ""
            while True:
                chunk = await reader.read(100)
                if not chunk:
                    break
                data_str += chunk.decode()
                if '\n' in data_str:
                    break

            command, *params = data_str.strip().split(" ")
            response = await process_command(command, params)

            writer.write(response.encode())
            await writer.drain()

    finally:
        print("Closing the connection")
        writer.close()


async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888,
    )
    addr = server.sockets[0].getsockname()
    print(f'Server on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
