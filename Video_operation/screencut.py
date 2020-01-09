#!/usr/bin/env python
# encoding: utf-8
"""
@author: Gaopeng
@license: (C) Copyright 2016-2020, Node Supply Chain Manager Corporation Limited.
@contact: gaopengbai0121@gmail.com
@software: Pycharm
@file: screencut.py
@time: 1/7/2020 12:18 PM
@desc: Manually draw a rect box that need to be recognised by using mouse events.
"""
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen, QGuiApplication
from Video_operation.Rcongnition import ocr_core

from six.moves import cPickle
import os


class myLabel(QLabel):
    """
    Initialize the box parameters.
    """
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = True

    def __init__(self, func, path="resource"):
        super().__init__()
        # callback function to interact between qt input dialog and paintevent.
        self.function = func
        self.box_refresh_signal = Communicate()
        # The box info save path.
        self.file_path = os.path.join(path, "vocab.pkl")
        if not os.path.exists(self.file_path):
            self.videobox = {}
        else:
            with open(self.file_path, 'rb') as f:
                self.videobox = cPickle.load(f)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  #
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
        elif event.buttons() == Qt.RightButton:  #
            self.flag = False
            if self.x0 != 0 and self.y0 != 0:
                self.pix_point(self.function())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:  #
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green, 2, Qt.DotLine))
        painter.drawRect(rect)

    def pix_point(self, name):
        if name != 0:
            self.videobox[name] = [self.x0, self.x1, self.y0, self.y1]
            self.save_box_to_local()
            self.box_refresh_signal.signal.emit("1")

            self.pick_screencut(self.videobox)

    def save_box_to_local(self):
        save_dict = dict(zip(self.videobox.keys(), self.videobox.values()))
        with open(self.file_path, 'wb') as f:
            cPickle.dump(save_dict, f)

    def box_clear(self):
        self.videobox.clear()

    def delete_box_image(self, path):
        if os.path.exists(path):
            os.remove(path)

    def pick_screencut(self, dic):
        for key in dic:
            pqscreen = QGuiApplication.primaryScreen()
            pixmap2 = pqscreen.grabWindow(self.winId(), dic[key][0], dic[key][2], abs(dic[key][1] - dic[key][0]),
                                          abs(dic[key][3] - dic[key][2]))
            # for test
            pixmap2.save(str(key) + '.png')
            self.recognition(str(key) + '.png')

    @staticmethod
    def recognition(path):
        print("Test: " + ocr_core(path))


class Communicate(QObject):
    signal = pyqtSignal(str)
