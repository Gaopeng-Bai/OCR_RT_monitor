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

import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cv2 import *
from GUI.OCR_GUI import Ui_Monitor
from Video_operation.screencut import myLabel

import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class Video_controller_window(Ui_Monitor):
    VIDEO_TYPE_OFFLINE = 0
    VIDEO_TYPE_REAL_TIME = 1

    STATUS_INIT = 0
    STATUS_PLAYING = 1
    STATUS_PAUSE = 2

    video_url = ""

    def __init__(self, mainWindow, video_url="", video_type=VIDEO_TYPE_OFFLINE, auto_play=True):
        self.playCapture = VideoCapture(0, cv2.CAP_DSHOW)
        self.timer = VideoTimer()
        self.pictureLabel = myLabel(self.save_box_callback)
        self.setupUi(mainWindow)
        self.video_url = video_url
        self.video_type = video_type  # 0: offline  1: realTime
        self.auto_play = auto_play
        self.status = self.STATUS_INIT  # 0: init 1:playing 2: pause
        self.element_init()

    @staticmethod
    def save_box_callback():
        text, okPressed = QInputDialog.getText(None, "Save this box?", "Box name:")
        if okPressed:
            if text != '':
                return text
            else:
                QMessageBox.about(None, "Name empty", "Please save again with name")
                return 0
        else:
            return 0

    def element_init(self):
        # Components
        self.pictureLabel.setCursor(Qt.CrossCursor)
        init_image = QPixmap("resource/cat.jpeg").scaled(self.centralwidget.width(), self.centralwidget.height())
        self.pictureLabel.setPixmap(init_image)

        self.mainlayerout.addWidget(self.pictureLabel)

        self.Run_OCR.setEnabled(True)
        self.Run_OCR.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPlay))
        self.Run_OCR.clicked.connect(self.switch_video)

        # timer 设置
        self.timer.timeSignal.signal[str].connect(self.show_video_images)

        # video 初始设置
        if self.video_url != "":
            self.set_timer_fps()
            if self.auto_play:
                self.switch_video()
        # self.videoWriter = VideoWriter('*.mp4', VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, size)

    def reset(self):
        self.timer.stop()
        self.playCapture.release()
        cv2.destroyAllWindows()
        self.status = Video_controller_window.STATUS_INIT
        self.Run_OCR.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPlay))

    def set_timer_fps(self):
        self.playCapture.open(self.video_url)
        # sometime fps default
        fps = self.playCapture.get(CAP_PROP_FPS)
        self.timer.set_fps(24)
        self.playCapture.release()
        cv2.destroyAllWindows()

    def set_video(self, url, video_type=VIDEO_TYPE_OFFLINE, auto_play=False):
        self.reset()
        self.video_url = url
        self.video_type = video_type
        self.auto_play = auto_play
        self.set_timer_fps()
        if self.auto_play:
            self.switch_video()

    def play(self):
        if self.video_url == "" or self.video_url is None:
            return
        if not self.playCapture.isOpened():
            self.playCapture.open(self.video_url)
        self.timer.start()
        self.Run_OCR.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPause))
        self.status = Video_controller_window.STATUS_PLAYING

    def stop(self):
        if self.video_url == "" or self.video_url is None:
            return
        if self.playCapture.isOpened():
            self.timer.stop()
            if self.video_type is Video_controller_window.VIDEO_TYPE_REAL_TIME:
                self.playCapture.release()
                cv2.destroyAllWindows()
            self.Run_OCR.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPlay))
        self.status = Video_controller_window.STATUS_PAUSE

    def re_play(self):
        if self.video_url == "" or self.video_url is None:
            return
        self.playCapture.release()
        cv2.destroyAllWindows()
        self.playCapture.open(self.video_url)
        self.timer.start()
        self.Run_OCR.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPause))
        self.status = Video_controller_window.STATUS_PLAYING

    def show_video_images(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                height, width = frame.shape[:2]
                if frame.ndim == 3:
                    rgb = cvtColor(frame, COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cvtColor(frame, COLOR_GRAY2BGR)

                temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image)
                self.pictureLabel.setPixmap(temp_pixmap)
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success and self.video_type is Video_controller_window.VIDEO_TYPE_OFFLINE:
                    print("play finished")  # Judge local file is finished
                    self.reset()
                    self.Run_OCR.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()

    def switch_video(self):
        if self.video_url == "" or self.video_url is None:
            return
        if self.status is Video_controller_window.STATUS_INIT:
            self.playCapture.open(self.video_url)
            self.timer.start()
            self.Run_OCR.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPause))
        elif self.status is Video_controller_window.STATUS_PLAYING:
            self.timer.stop()
            if self.video_type is Video_controller_window.VIDEO_TYPE_REAL_TIME:
                self.playCapture.release()
                cv2.destroyAllWindows()
            self.Run_OCR.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPlay))
        elif self.status is Video_controller_window.STATUS_PAUSE:
            if self.video_type is Video_controller_window.VIDEO_TYPE_REAL_TIME:
                self.playCapture.open(self.video_url)
            self.timer.start()
            self.Run_OCR.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPause))

        self.status = (Video_controller_window.STATUS_PLAYING,
                       Video_controller_window.STATUS_PAUSE,
                       Video_controller_window.STATUS_PLAYING)[self.status]


class Communicate(QObject):
    signal = pyqtSignal(str)


class VideoTimer(QThread):

    def __init__(self, frequent=20):
        QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()
        self.mutex = QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit("1")
            time.sleep(1 / self.frequent)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.frequent = fps
