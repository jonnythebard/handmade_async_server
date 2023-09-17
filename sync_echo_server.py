import socket


def runserver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        while True:
            data = connection.recv(1024)
            print(data)
            msg = b'echo: '
            msg += data
            connection.send(msg)

            if data == b'bye\r\n':
                connection.close()
                break


if __name__ == "__main__":
    runserver()
