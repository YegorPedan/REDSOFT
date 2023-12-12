import asyncio


async def handle_client(reader: str, writer: str) -> None:
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message!r} from {addr!r}")

    response = "Hello, this is an asynchronous response!\n"
    writer.write(response.encode())
    await writer.drain()

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
