import asyncio
import uuid

HOST = '127.0.0.1'
PORT = 8888


async def run_client() -> None:
    unique_id = uuid.uuid4()
    reader, writer = await asyncio.open_connection(HOST, PORT)
    message = await reader.read(256)
    print(message)
    data = f'add_client 19 12 15 {unique_id}'
    writer.write(data.encode())
    await writer.drain()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
