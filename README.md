## To make program usable, paste this into console while being in projekt-pi directory:

`
pip install -r requirements.txt
`
<h4> After requirements.txt has been installed you can run program by using some IDE or by CMD, you need to remember that you have to start server first. </h4>

# Table of contents:
1. [Server](#server)
2. [Client](#client)
3. [Config](#config)
4. [Integral](#integral)


<h3>Now let's talk about the code and what's going on in it.


## Server
```python
import socket
from config import CONNECTION_STRING, error_handler, read_data, FORMAT
from _thread import start_new_thread
from integral import integral

def request_handler(client, request):
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
        return False
        
    # If the request is a BYE request, send a response and return True to break the loop
    elif request.split("\r\n")[0] == "BYE":
        client.sendall("BYE\r\n\r\n".encode(FORMAT))
        return True
        
    # If the request is not recognized, send an error message and return True to break the loop
    else:
        error_handler(client)
        return True

def connection_handler(client):
    # Receive the initial HELLO message from the client
    data = read_data(client).decode(FORMAT)
    if data.split("\r\n")[0] == "HELLO":
        name = data.split("\r\n")[1]
        response = f"HELLO HABIBI {name}\r\n\r\n"
        client.sendall(response.encode(FORMAT))
    else:
        error_handler(client)

    # Handle subsequent requests from the client
    while True:
        request = read_data(client).decode(FORMAT)
        if request_handler(client, request):
            break

    # Close the connection with the client
    client.close()

# Set up the server socket and listen for incoming connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
    serv.bind(CONNECTION_STRING)
    serv.listen(5)
    while True:
        client, addr = serv.accept()
        print(f"Connected from {addr[0]}")
        start_new_thread(connection_handler, (client,))
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
