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
from PyQt5 import QtCore

# Variables for holding information about connections

# Client class, new instance created for each connected client
# Each instance has the socket and address that is associated with items
# Along with an assigned ID and a name chosen by the client


class Client(threading.Thread):
    def __init__(self, socket, func):
        threading.Thread.__init__(self)
        self.socket = socket
        self.callback_receive = func

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server and send it back to every
    # client aside from the client that has sent it
    # .decode is used to convert the byte data into a printable string
    def run(self):
        while True:
            sock, address = self.socket.accept()
            while address:
                try:
                    data = sock.recv(32)
                except:
                    print("Client " + " has disconnected")
                    break
                if data != "" and data != b'':
                    if str(data.decode("utf-8")) == "on":
                        print("run program")
                        self.callback_receive()


def RUn_server(function=None):
    # Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 80))
    print(sock.getsockname())
    sock.listen(1)

    # Create new thread to wait for connections
    # newConnectionsThread = threading.Thread(target=newConnections, args=(sock, function))
    client_thread = Client(sock, func=function)
    client_thread.start()

