HOST = "localhost"
PORT = 39238
CONNECTION_STRING = (HOST, PORT)
FORMAT = "utf-8"


def read_data(socket):
    data = b''
    while b'\r\n\r\n' not in data:
        data += socket.recv(1)

    return data


def error_handler(socket):
    error = b'unoperated request\r\n\r\n'
    socket.sendall(error)
