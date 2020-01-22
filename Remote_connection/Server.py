#!/usr/bin/env python
# encoding: utf-8
"""
@author: Gaopeng
@license: (C) Copyright 2016-2020, Node Supply Chain Manager Corporation Limited.
@contact: gaopengbai0121@gmail.com
@software: Pycharm
@file: Server.py
@time: 1/21/2020 6:36 PM
@desc:
"""
import socket
import threading

# Variables for holding information about connections
connections = []
total_connections = 0


# Client class, new instance created for each connected client
# Each instance has the socket and address that is associated with items
# Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal, func):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
        self.callback_receive = func

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server and send it back to every
    # client aside from the client that has sent it
    # .decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "" and data != b'':
                if str(data.decode("utf-8")) == "on":
                    self.callback_receive()


# Wait for new connections
def newConnections(socket, function):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True, func=function))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1


def RUn_server(function=None):
    # Get host and port
    # host = input("Host: ")
    # port = int(input("Port: "))

    # Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 80))
    print(sock.getsockname())
    sock.listen(5)

    # Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target=newConnections, args=(sock, function,))
    newConnectionsThread.start()
