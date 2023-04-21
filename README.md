## To make program usable, paste this into console while being in projekt-pi directory:

```
pip install -r requirements.txt
```

<h4> After requirements.txt has been installed you can run program by using some IDE or by CMD, you need to remember that you have to start server first. </h4>

# Table of contents:

1. [Shortcut](#shortcut)
2. [Logs](#logs)
3. [Server](#server)
4. [Client](#client)
5. [Config](#config)
6. [Integral](#integral)

## Shortcut
This program is a client that connects to a server using a socket connection. The program prompts the user to enter their name and sends a "HELLO" message to the server. Then, the program enters a loop where the user is prompted to choose between calculating an integral or disconnecting from the server. If the user chooses to calculate an integral, the program prompts the user for the lower and upper bounds of the integration and the function to be integrated. The program sends the request to the server and receives the result or an error message in response. If the user chooses to disconnect, the program sends a "BYE" message to the server and exits the loop. If the server responds with a "BYE" message, the program closes the socket connection and terminates. The program uses helper functions to read data from the socket and handle errors.




## Logs

Files are named in this scheme, my file is named "Aleks127.0.0.120230421_004658.log" :

```.log
    "Aleks" is the username of the client who initiated the connection.
    "127.0.0.1" is the IP address of the client.
    "2023-04-21" is the date when the log was created, in the format YYYY-MM-DD.
    "004057" is the time when the log was created, in the format HHMMSS (hours, minutes, seconds).
    ".log" is the file extension, indicating that the file contains log data.
```

<h3>Now let's talk about the code and what's going on in it.

## Server

```python
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

```

# Client

```python
import socket
from config import CONNECTION_STRING, read_data, FORMAT

# create a socket object and connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.connect(CONNECTION_STRING)

    # ask for user's name and send a HELLO message to the server
    name = input("What's your name:")
    request = f'HELLO\r\n{name}\r\n\r\n'
    server.sendall(request.encode(FORMAT))

    # read server's response and check if it's a HELLO message
    response = read_data(server).decode(FORMAT)
    if response.split()[0] == "HELLO":
        print(response)

        # loop until the user decides to disconnect
        while True:
            # ask the user what function they want to use
            operation = int(input('What function do you want to use (1-integral, 0-disconnect):'))

            if operation == 1:  # user wants to calculate an integral
                a = input("Bottom Range:")
                b = input("Top Range:")
                f = input("Function:")
                request = f"INTEGRAL\r\nBOTTOM-RANGE: {a}\r\n TOP-RANGE: {b}\r\n FUNCTION: {f}\r\n\r\n"
                server.sendall(request.encode(FORMAT))

                # read server's response and print the result or an error message
                response = read_data(server).decode(FORMAT)
                if response.split()[0] == 'RESULT:':
                    print(f"server returned: {response.split()[1]}")
                else:
                    print("error occurred")

            elif operation == 0:  # user wants to disconnect
                server.sendall("BYE\r\n\r\n".encode(FORMAT))

                # read server's response and break the loop if it's a BYE message
                response = read_data(server).decode(FORMAT)
                if response == "BYE\r\n\r\n":
                    break
                else:
                    print("error ocurred")

            else:  # user entered an invalid operation
                print("unoperated function")

    else:  # server didn't respond with a HELLO message
        print('error occurred')

    # close the socket connection
    server.close()
```

## Config

```python

HOST = "localhost"  # host address of the server
PORT = 39236  # port number of the server
CONNECTION_STRING = (HOST, PORT)  # tuple containing host and port
FORMAT = "utf-8"  # encoding format used for communication with the server


def read_data(socket):
    """
    Helper function that reads data from the socket until it finds the
    end-of-message delimiter '\r\n\r\n'.
    """
    data = b''
    while b'\r\n\r\n' not in data:
        data += socket.recv(1)
    return data


def error_handler(socket):
    """
    Helper function that sends an error message to the client if an invalid
    request is made.
    """
    error = b'unoperated request\r\n\r\n'
    socket.sendall(error)
```

## Integral

```python

import numpy as np


def integral(a, b, f):
    """
    Computes the definite integral of a given function f over the interval [a, b]
    using the trapezoidal rule with 1000 subintervals.
    """
    dx = ((b-a) / 1000)
    X = np.arange(a, b, dx).tolist()
    try:
        Y = []
        for element in X:
            Y.append(eval(f, {}, {'x': element}))
        s = dx * np.sum(Y)
        return s
    except:
        return 'ERROR OCCURRED\r\n\r\n'
```
