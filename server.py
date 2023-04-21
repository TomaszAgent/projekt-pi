import socket
from config import CONNECTION_STRING, error_handler, read_data, FORMAT
from _thread import start_new_thread
from integral import integral
import os
from datetime import datetime

LOGS_DIR = "logs/"

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def request_handler(client, request, log_file):
    # If the request is an INTEGRAL request, extract the necessary parameters
    if request.split("\r\n")[0] == "INTEGRAL":
        a = int(request.split("\r\n")[1].split()[1])
        b = int(request.split("\r\n")[2].split()[1])
        f = request.split("\r\n")[3].split()[1]
        
        # Compute the integral and send the result back to the client
        result = integral(a, b, f)
        print(result)
        if result != 'ERROR OCCURRED':
            client.sendall(f"RESULT: {result}\r\n\r\n".encode(FORMAT))
        else:
            client.sendall(response.encode(FORMAT))
        log_file.write(f"INTEGRAL REQUEST: a={a}, b={b}, f={f}, RESULT: {result}\n")
        return False
        
    # If the request is a BYE request, send a response and return True to break the loop
    elif request.split("\r\n")[0] == "BYE":
        client.sendall("BYE\r\n\r\n".encode(FORMAT))
        log_file.write("BYE REQUEST\n")
        return True
        
    # If the request is not recognized, send an error message and return True to break the loop
    else:
        error_handler(client)
        log_file.write("INVALID REQUEST\n")
        return True

def connection_handler(client, addr):
    # Receive the initial HELLO message from the client
    data = read_data(client).decode(FORMAT)
    if data.split("\r\n")[0] == "HELLO":
        name = data.split("\r\n")[1]
        response = f"HELLO HABIBI {name}\r\n\r\n"
        client.sendall(response.encode(FORMAT))
        log_file_name = f"{name}{addr[0]}{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_file_path = os.path.join(LOGS_DIR, log_file_name)
        with open(log_file_path, "w") as log_file:
            log_file.write(f"CONNECTION ESTABLISHED: username={name}, IP={addr[0]}\n")
            # Handle subsequent requests from the client
            while True:
                request = read_data(client).decode(FORMAT)
                if request_handler(client, request, log_file):
                    break
            log_file.write("CONNECTION CLOSED\n")
    else:
        error_handler(client)

    # Close the connection with the client
    client.close()

# Set up the server socket and listen for incoming connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
    serv.bind(CONNECTION_STRING)
    serv.listen(5)
    while True:
        client, addr = serv.accept()
        print(f"Connected from {addr[0]}")
        start_new_thread(connection_handler, (client, addr))
