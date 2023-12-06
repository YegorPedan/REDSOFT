import asyncio
import aiosqlite


class Server:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self.clients = {}

    async def start_server(self):
        server = await asyncio.start_server(None, self._host, self._port)
        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    server = Server('127.0.0.1', 8888)
    asyncio.run(server.start_server())
