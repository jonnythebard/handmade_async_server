import socket


def runserver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()
    server_socket.setblocking(False)
    connections = []

    try:
        while True:
            try:
                connection, client_address = server_socket.accept()
                print(f"Connection established with {client_address}")
                connections.append(connection)
            except BlockingIOError:
                pass

            for conn in connections:
                try:
                    data = conn.recv(1024)
                except BlockingIOError:
                    continue

                print(f"send to {client_address}: {data}")
                msg = b'echo: '
                msg += data
                conn.send(msg)

                if data == b'bye\r\n':
                    conn.close()
                    print(f"connection with {client_address} closed")
                    connections.remove(conn)
                    break
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == "__main__":
    runserver()
