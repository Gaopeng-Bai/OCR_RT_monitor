#!/usr/bin/env python
# encoding: utf-8
"""
@author: Gaopeng
@license: (C) Copyright 2016-2020, Node Supply Chain Manager Corporation Limited.
@contact: gaopengbai0121@gmail.com
@software: Pycharm
@file: OCR_main.py
@time: 1/7/2020 11:56 AM
@desc:
"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Video_operation.video_box import Video_controller_window as VideoWindow
from GUI.box_manager import Ui_UI_box_manager


class OCR_main(QMainWindow, VideoWindow):
    def __init__(self, mainWindow):
        super().__init__(mainWindow=mainWindow)
        self.menuSetting.triggered[QAction].connect(self.test)

    @staticmethod
    def test():
        ch.show()


class Box_manager_widget(QWidget, Ui_UI_box_manager):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)
        # self.box_list_init()

    def box_list_init(self):
        """
        init the contents of box list
        :return:
        """
        self.Box_list.setColumnCount(5)
        self.Box_list.verticalHeader().setVisible(False)
        self.Box_list.setStyleSheet("QHeaderView::section{Background-color:rgb(0,1,1)}")
        self.Box_list.setHorizontalHeaderLabels(['Box name', 'X0', 'x1', 'y0', 'y1'])
        self.Box_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Box_list.resizeColumnsToContents()
        self.Box_list.resizeRowsToContents()
        self.Box_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Box_list.setSelectionBehavior(QAbstractItemView.SelectRows)

    def show_boxes(self):
        print(mw.pictureLabel.videobox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    mw = OCR_main(mainWindow=mainwindow)
    # mw.set_video("resource/video.mp4", VideoBox.VIDEO_TYPE_OFFLINE, False)
    mw.set_video(0, OCR_main.VIDEO_TYPE_REAL_TIME, True)
    mainwindow.show()
    ch = Box_manager_widget()
    sys.exit(app.exec_())