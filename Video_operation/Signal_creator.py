#!/usr/bin/python3
# -*-coding:utf-8 -*-

# Reference:**********************************************
# @Time    : 1/16/2020 8:01 PM
# @Author  : Gaopeng.Bai
# @File    : Signal_creator.py
# @User    : baigaopeng
# @Software: PyCharm
# @Description: To create qt signal.
# Reference:**********************************************
from PyQt5.QtCore import QObject, pyqtSignal


class Communicate(QObject):
    signal = pyqtSignal(str)