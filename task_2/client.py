import asyncio
import uuid

HOST = '0.0.0.0'
PORT = 8888


async def run_client() -> None:
    unique_id = uuid.uuid4()
    reader, writer = await asyncio.open_connection(HOST, PORT)

    message = await reader.read(256)
    print(message.decode())
    data = f'hallo, world!'
    writer.write(data.encode())
    await writer.drain()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
