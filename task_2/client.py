import asyncio
from asyncio import StreamReader, StreamWriter
import uuid

HOST = '0.0.0.0'
PORT = 8888


async def authenticate(reader: StreamReader, writer: StreamWriter):
    result = ''
    while result != 'Successfully authenticated':
        # get the instructions from server
        data = await reader.read(256)
        print(data.decode())

        writer.write(input().encode())
        await writer.drain()
        data = await reader.read(256)
        print(data.decode())
        writer.write(input().encode())
        await writer.drain()
        result = (await reader.read(256)).decode()

        if result == 'Successfully authenticated':
            print('You are authenticated!')
        else:
            print('Username or password incorrect. Please try again.')


async def add_user(writer):
    unique_id = uuid.uuid4()
    data = f'add_client 1 2 3 {unique_id}'
    writer.write(data.encode())
    await writer.drain()


async def send_and_receive_messages():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    await authenticate(reader, writer)
    while True:
        try:
            message = input('Enter a message (or \'quit \' to exit) ')
            if message.lower() == 'quit':
                break
            elif message.lower() == 'add_user':
                await add_user(writer)

            print(f'Send: {message!r}')
            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(100)
            print(f'Received: {data.decode()!r}')
        except asyncio.CancelledError:
            print(f'CancelledError, stop the connection')
            break
    print('Closing the connection')
    writer.close()
    await writer.wait_closed()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(send_and_receive_messages())
