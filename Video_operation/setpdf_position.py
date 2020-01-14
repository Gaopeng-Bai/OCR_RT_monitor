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

from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
import cv2
import sys


class myLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def __init__(self, callback_position_confirm):
        super().__init__()
        self.callback_position_confirm = callback_position_confirm

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  #
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
        elif event.buttons() == Qt.RightButton:  #
            self.flag = False
            if self.x0 != 0 and self.y0 != 0:
                self.callback_position_confirm()

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


class PDF_image(QWidget):
    def __init__(self, path='example1.png'):
        super().__init__()
        self.path = path
        self.initUI()

    def initUI(self):
        self.resize(980, 2000)
        self.setWindowTitle('Position caption from image')

        self.lb = myLabel(self)
        self.lb.setGeometry(QRect(0, 0, 1000, 1400))

        img = cv2.imread(self.path)
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)

        self.lb.setPixmap(pixmap)
        self.lb.setCursor(Qt.CrossCursor)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDF_image()
    sys.exit(app.exec_())
