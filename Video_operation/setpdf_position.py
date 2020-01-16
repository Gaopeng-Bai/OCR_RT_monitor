#!/usr/bin/env python
# encoding: utf-8
"""
@author: Gaopeng
@license: (C) Copyright 2016-2020, Node Supply Chain Manager Corporation Limited.
@contact: gaopengbai0121@gmail.com
@software: Pycharm
@file: setpdf_position.py
@time: 1/14/2020 3:26 PM
@desc: QT widget to locate the position to be set on pdf file.
"""
# coding=utf-8

from PyQt5.QtCore import QRect, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QLabel


class pdf_label(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def __init__(self, callback_empty_painter):
        super().__init__()
        self.button_signal = Communicate()
        self.callback_empty_painter = callback_empty_painter

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  #
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
        elif event.buttons() == Qt.RightButton:  #
            self.flag = False
            if self.x0 != 0 and self.y0 != 0:
                self.button_signal.signal.emit("1")
            else:
                self.callback_empty_painter()

    def mouseReleaseEvent(self, event):
        self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        painter.drawRect(rect)

    def return_value(self):

        return int((self.x0+(self.x1-self.x0)/2-133+127)*96/162), \
               int((1470-(self.y0+(self.y1-self.y0)/2+462))*595/982+230)


class Communicate(QObject):
    signal = pyqtSignal(str)