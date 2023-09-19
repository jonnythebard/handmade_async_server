import asyncio
import socket


async def runserver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()
    server_socket.setblocking(False)

    loop = asyncio.get_event_loop()

    try:
        while True:
            connection, client_address = await loop.sock_accept(server_socket)
            print(f"Connection established with {client_address}")

            while data := await loop.sock_recv(connection, 1024):
                msg = b'echo: '
                msg += data
                await loop.sock_sendall(connection, msg)

                if data == b'bye\r\n':
                    connection.close()
                    print(f"connection with {client_address} closed")
                    break

    except KeyboardInterrupt:
        server_socket.close()

if __name__ == "__main__":
    asyncio.run(runserver())
