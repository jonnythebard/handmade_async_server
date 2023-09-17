import socket


def runserver():
    # Create a listening socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 12345))
    # After this code, listening 12345 port is bound to the socket
    server_socket.listen()

    try:
        # Accept a connection from a client
        # When a connection is created ephemeral port is bound to the connection socket
        connection, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        # Use client_socket to communicate with the client
        data = connection.recv(1024)
        print(data)

        # Close the client socket when done
        connection.close()
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == "__main__":
    runserver()
