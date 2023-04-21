import socket
from config import CONNECTION_STRING, read_data, FORMAT


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.connect(CONNECTION_STRING)
    name = input("What's your name:")
    request = f'Hi\r\n{name}\r\n\r\n'
    server.sendall(request.encode(FORMAT))

    response = read_data(server).decode(FORMAT)

    if response.split()[0] == "HELLO":
        print(response)
        while True:
            operation = int(input('What function do you want to use (1-integral, 0-disconnect):'))
            if operation == 1:
                a = input("Bottom Range:")
                b = input("Top Range:")
                f = input("Function:")
                request = f"INTEGRAL\r\nBOTTOM-RANGE: {a}\r\n TOP-RANGE: {b}\r\n FUNCTION: {f}\r\n\r\n"
                server.sendall(request.encode(FORMAT))
                response = read_data(server).decode(FORMAT)
                if response.split()[0] == 'RESULT:':
                    print(f"server returned: {response.split()[1]}")
                else:
                    print("no i sie wyjebalo")
            elif operation == 0:
                server.sendall("BYE\r\n\r\n".encode(FORMAT))
                response = read_data(server).decode(FORMAT)
                if response == "BYE\r\n\r\n":
                    break
                else:
                    print("no i sie wyjebalo")
            else:
                print("ty jebany przygłupie, czytaj ze zrozumeiniem, 1 albo 0")
    else:
        print('no i sie wyjebalo')
    server.close()
