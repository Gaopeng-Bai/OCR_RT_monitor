#!/usr/bin/env python
# encoding: utf-8
"""
@author: Gaopeng
@license: (C) Copyright 2016-2020, Node Supply Chain Manager Corporation Limited.
@contact: gaopengbai0121@gmail.com
@software: Pycharm
@file: Client.py
@time: 2/20/2020 12:56 PM
@desc:
"""

import socket


class myclient:
    def __init__(self, callback):
        self.tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect server
        serverAddr = ('127.0.0.2', 8080)
        try:
            self.tcpClientSocket.connect(serverAddr)
        except WindowsError:
            print("no server connection")
            callback()

    def __del__(self):
        self.tcpClientSocket.close()

    def send_data(self, data):
        data = [str(x) for x in data]
        data = ".".join(data)
        self.tcpClientSocket.send(data.encode("utf-8"))

    def receiver(self):
        return self.tcpClientSocket.recv(1024)


if __name__ == "__main__":
    client = myclient()
    idata = [1124, 645, 456, 46]
    client.send_data(idata)

