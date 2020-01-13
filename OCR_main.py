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
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Video_operation.video_box import Video_controller_window as VideoWindow
from GUI.box_manager import Ui_UI_box_manager

from six.moves import cPickle


def get_keys(d, value):
    """
    find the the key in dict by value.
    :param d: dict.
    :param value: value to be fund
    :return: the key of this value in d.
    """
    for k, v in d.items():
        for i in v:
            if str(i) == str(value):
                return k


class OCR_main(QWidget, VideoWindow):
    def __init__(self, mainWindow, path="resource"):
        super().__init__(mainWindow=mainWindow)
        # reload box_position data, if not exist create new.
        self.file_path = os.path.join(path, "pdf.pkl")
        if not os.path.exists(self.file_path):
            self.combine = {}
        else:
            with open(self.file_path, 'rb') as f:
                self.combine = cPickle.load(f)

        self.cwd = os.getcwd()
        self.GUi_init_setting()
        self.pictureLabel.box_refresh_signal.signal[str].connect(self.refresh_boxes_to_output)

    def GUi_init_setting(self):
        self.menuSetting.triggered[QAction].connect(self.change_window)
        self.menuSetting.setToolTip('To change the boxes information')

        # click to open file dialog
        self.ChoosePDFbutton.clicked.connect(self.pick_up_output_file)

        self.pdf_position_set.clicked.connect(self.pdf_position_set_)
        self.pdf_position_set.setToolTip('Click to set this position')
        self.pdf_position_reset.clicked.connect(self.delete_all_position)
        self.pdf_position_reset.setToolTip('Click to delete all position')

        self.refresh_boxes_to_output()

        # init combobox
        self.init_position()
        self.boxes.currentIndexChanged.connect(self.init_position)

    def delete_all_position(self):
        self.combine.clear()
        self.init_position()
        self.save_box_to_local()

    def init_position(self):
        """
        set the position related current combobox text.
        :return:
        """
        if self.boxes.currentText() in self.combine:
            self.PositionX.setText(self.combine[self.boxes.currentText()][0])
            self.PositionY.setText(self.combine[self.boxes.currentText()][1])
        else:
            self.PositionX.setText(' ')
            self.PositionY.setText(' ')

    def pdf_position_set_(self):
        x = self.PositionX.text()
        y = self.PositionY.text()
        if x != '' and y != '':
            self.combine[self.boxes.currentText()] = [x, y]
            self.save_box_to_local()
        else:
            QMessageBox.about(None, "No data", "Please fill position x and y completely")

    def save_box_to_local(self):
        save_dict = dict(zip(self.combine.keys(), self.combine.values()))
        with open(self.file_path, 'wb') as f:
            cPickle.dump(save_dict, f)

    def refresh_boxes_to_output(self):
        self.boxes.clear()
        for i in self.pictureLabel.videobox:
            self.boxes.addItem(str(i))

    def pick_up_output_file(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "Choose PDF file",
                                                                self.cwd,  # start path
                                                                "Text Files (*.pdf)")
        if fileName_choose == "":
            QMessageBox.about(None, "No file chosen", "Please try again")
        else:
            self.PDF_file_name.setText(fileName_choose)

    def change_window(self):
        mainwindow.setVisible(False)
        ch.refresh_box()
        ch.show()


class Box_manager_widget(QWidget, Ui_UI_box_manager):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)
        self.item_chosen = ''
        self.button_init()
        self.box_list_init()
        self.refresh_box()

    def closeEvent(self, event):
        """
        overwrite closeEvent method，execute code when this window closed.
        :param event: close() the event triggered.
        :return: None
        """
        mainwindow.setVisible(True)
        mw.refresh_boxes_to_output()

    def button_init(self):
        self.delete_box.setToolTip('Delete the item you chosen, Shortcut key "Delete"')
        self.delete_box.clicked.connect(self.delete_box_)
        self.delete_box.setShortcut('Delete')  # shortcut key
        self.Change_box_name.setToolTip('Change the name of item, shortcut key "F2"')
        self.Change_box_name.clicked.connect(self.change_box_name_)
        self.Change_box_name.setShortcut('F2')  # shortcut key

    def change_box_name_(self):
        if self.item_chosen is not '':
            # check if item_chosen is key in dict.
            name = self.get_input()
            if self.item_chosen in mw.pictureLabel.videobox:
                mw.pictureLabel.videobox[name] = mw.pictureLabel.videobox.pop(self.item_chosen)
            else:
                a = get_keys(mw.pictureLabel.videobox, self.item_chosen)
                mw.pictureLabel.videobox[name] = mw.pictureLabel.videobox.pop(a)
            mw.pictureLabel.save_box_to_local()
            self.refresh_box()
        else:
            QMessageBox.about(None, "No item chosen", "Please click a item first")

    def get_input(self):
        text, okPressed = QInputDialog.getText(None, "Change box name", "Rename:")
        if okPressed:
            if text != '':
                return text
            else:
                QMessageBox.about(None, "Name empty", "Please try again")
                return 0
        else:
            return 0

    def delete_box_(self):
        if self.item_chosen is not '':
            # check if item_chosen is key in dict.
            if self.item_chosen in mw.pictureLabel.videobox:
                mw.pictureLabel.videobox.pop(self.item_chosen)
                if self.item_chosen in mw.combine:
                    mw.combine.pop(self.item_chosen)
                    mw.save_box_to_local()

                mw.pictureLabel.delete_box_image(str(self.item_chosen)+'.png')
            else:
                a = get_keys(mw.pictureLabel.videobox, self.item_chosen)
                mw.pictureLabel.videobox.pop(a)
                if a in mw.combine:
                    mw.combine.videobox.pop(a)
                    mw.save_box_to_local()

                mw.pictureLabel.delete_box_image(str(a) + '.png')
            mw.pictureLabel.save_box_to_local()
            self.refresh_box()
        else:
            QMessageBox.about(None, "No item chosen", "Please click a item first")

    def box_list_init(self):
        """
        init the contents of box list
        :return:
        """
        self.Box_list.verticalHeader().setVisible(False)
        self.Box_list.setHorizontalHeaderLabels(['Box name', 'X0', 'X1', 'Y0', 'Y1'])
        self.Box_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Box_list.resizeColumnsToContents()
        self.Box_list.resizeRowsToContents()
        self.Box_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Box_list.setSelectionBehavior(QAbstractItemView.SelectRows)

    def refresh_box(self):
        """
        Refresh box view
        :return:
        """
        if mw.pictureLabel.videobox is not None:
            self.show_boxes()

    def show_boxes(self):
        """
        show the box list
        :return:
        """
        self.Box_list.clearContents()
        self.Box_list.setRowCount(len(mw.pictureLabel.videobox))
        for i, item in enumerate(mw.pictureLabel.videobox):
            self.Box_list.setItem(i, 0, QTableWidgetItem(item))
            self.Box_list.setItem(i, 1, QTableWidgetItem(str(mw.pictureLabel.videobox[item][0])))
            self.Box_list.setItem(i, 2, QTableWidgetItem(str(mw.pictureLabel.videobox[item][1])))
            self.Box_list.setItem(i, 3, QTableWidgetItem(str(mw.pictureLabel.videobox[item][2])))
            self.Box_list.setItem(i, 4, QTableWidgetItem(str(mw.pictureLabel.videobox[item][3])))
        self.Box_list.itemClicked.connect(self.item_chosen_slot)

    def item_chosen_slot(self, item):
        self.item_chosen = item.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    mw = OCR_main(mainWindow=mainwindow)
    # mw.set_video("resource/video.mp4", VideoBox.VIDEO_TYPE_OFFLINE, False)
    mw.set_video(0, OCR_main.VIDEO_TYPE_REAL_TIME, True)
    mainwindow.show()
    ch = Box_manager_widget()
    sys.exit(app.exec_())
