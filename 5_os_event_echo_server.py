import selectors
import socket


def runserver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()
    server_socket.setblocking(False)

    selector = selectors.DefaultSelector()
    selector.register(server_socket, selectors.EVENT_READ)

    try:
        while True:
            events = selector.select(timeout=1)

            if len(events) == 0:
                continue

            for event, _ in events:
                event_socket = event.fileobj

                if event_socket == server_socket:
                    conn, client_address = server_socket.accept()
                    print(f"Connection established with {client_address}")
                    selector.register(conn, selectors.EVENT_READ)
                else:
                    conn = event_socket
                    data = conn.recv(1024)
                    msg = b'echo: '
                    msg += data
                    conn.send(msg)

                    if data == b'bye\r\n':
                        conn.close()
                        print(f"connection with {client_address} closed")
                        break

    except KeyboardInterrupt:
        server_socket.close()


if __name__ == "__main__":
    runserver()
