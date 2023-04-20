import socket
from config import CONNECTION_STRING, error_handler, read_data, FORMAT
from _thread import start_new_thread
from integral import integral


def request_handler(client, request):

    if request.split("\r\n")[0] == "INTEGRAL":
        a = int(request.split("\r\n")[1].split()[1])
        b = int(request.split("\r\n")[2].split()[1])
        f = request.split("\r\n")[3].split()[1]
        result = integral(a, b, f)
        if result != 'ERROR OCCURRED\r\n\r\n':
            client.sendall(f"RESULT: {result}\r\n\r\n".encode(FORMAT))
        else:
            client.sendall(result.encode(FORMAT))
        return False
    elif request == "BYE\r\n\r\n":
        client.sendall("BYE\r\n\r\n".encode(FORMAT))
        return True
    else:
        error_handler(client)
        return True


def connection_handler(client):
    data = read_data(client).decode(FORMAT)
    if data.split("\r\n")[0] == "HELLO":
        name = data.split("\r\n")[1]
        response = f"HELLO HABIBI {name}\r\n\r\n"
        client.sendall(response.encode(FORMAT))
        while True:
            request = read_data(client).decode(FORMAT)
            if request_handler(client, request):
                break
    else:
        error_handler(client)

    client.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
    serv.bind(CONNECTION_STRING)
    serv.listen(5)
    while True:
        client, addr = serv.accept()
        print(f"Connected from {addr[0]}")
        start_new_thread(connection_handler, (client,))
