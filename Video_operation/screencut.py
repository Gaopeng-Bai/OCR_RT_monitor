#!/usr/bin/env python
# encoding: utf-8
"""
@author: Gaopeng
@license: (C) Copyright 2016-2020, Node Supply Chain Manager Corporation Limited.
@contact: gaopengbai0121@gmail.com
@software: Pycharm
@file: screencut.py
@time: 1/7/2020 12:18 PM
@desc:
"""
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen, QGuiApplication
from Video_operation.Rcongnition import ocr_core


class myLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = True

    videobox = {}

    def __init__(self, func):
        super().__init__()
        self.function = func

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
            temp = {name: [self.x0, self.x1, self.y0, self.y1]}
            self.videobox.update(temp)
            self.pick_screencut(self.videobox)

    def box_clear(self):
        self.videobox.clear()

    def pick_screencut(self, dic):
        for key in dic:
            pqscreen = QGuiApplication.primaryScreen()
            pixmap2 = pqscreen.grabWindow(self.winId(), dic[key][0], dic[key][2], abs(dic[key][1] - dic[key][0]),
                                          abs(dic[key][3] - dic[key][2]))
            pixmap2.save(str(key) + '.png')
            self.recognition(str(key) + '.png')

    @staticmethod
    def recognition(path):
        print("Test: "+ocr_core(path))