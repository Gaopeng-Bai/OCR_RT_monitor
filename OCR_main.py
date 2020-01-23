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
import os
import sys

import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from six.moves import cPickle

from GUI.box_manager import Ui_UI_box_manager
from GUI.image_GUI import Ui_Form

# from Remote_connection.Server import RUn_server
from Remote_connection.server_qthreaad import RUn_server

from Video_operation.pdf_fill import fill_data_in_pdf
from Video_operation.pdf_to_image import pdf_to_image
from Video_operation.setpdf_position import pdf_label
from Video_operation.video_box import Video_controller_window as VideoWindow


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


def persent_pdf():
    import webbrowser
    webbrowser.open('destination.pdf')


class OCR_main(QWidget, VideoWindow):
    get_path: str

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
        self.pdftoimage = pdf_to_image()

        self.GUi_init_setting()
        self.pictureLabel.box_refresh_signal.signal[str].connect(self.refresh_boxes_to_output)

        self.test = bool

    def GUi_init_setting(self):
        self.menuSetting.triggered[QAction].connect(self.Box_manager_window)
        self.menuSetting.setToolTip('To change the boxes information')

        # click to open file dialog
        self.ChoosePDFbutton.clicked.connect(self.pick_up_output_file)

        self.pdf_position_set.clicked.connect(self.pdf_position_set_)
        self.pdf_position_set.setToolTip('Click to set this position')
        self.pdf_position_reset.clicked.connect(self.delete_all_position)
        self.pdf_position_reset.setToolTip('Click to delete all position')

        self.run_program.clicked.connect(self.run_program_)
        self.run_program.setToolTip("Click to run program according to the timer")

        self.test.clicked.connect(self.run_program_test)

        # init position entry.
        self.PositionX.setReadOnly(True)
        self.PositionY.setReadOnly(True)
        self.refresh_boxes_to_output()

        # init combobox
        self.init_position()
        self.boxes.currentIndexChanged.connect(self.init_position)

        self.init_spinbox()

    def run_program_(self):
        """
        set a timer to run this program automatically in specific time period.
        :return:
        """
        self.test = False
        value = self.timer_output.value()
        self.timer = QTimer(self)  # init a timer
        self.timer.timeout.connect(self.operate)  #
        self.timer.start(value * 1000 * 60)  #

    def run_program_test(self):
        """
        run this program manually and remotely, receiver a signal form client then present the results pdf file.
        :return:
        """
        # init signal form server
        self.test = True
        RUn_server(self.operate)

    def operate(self):
        mw.pictureLabel.pick_screencut()
        position = {'position_x': [], 'position_y': []}
        data = []

        for key in mw.pictureLabel.output_dic:
            if key in self.combine:
                position['position_x'].append(self.combine[key][0])
                position['position_y'].append(self.combine[key][1])
                data.append(mw.pictureLabel.output_dic[key])
        if self.PDF_file_name != "":
            fill_data_in_pdf(position, data_to_fill=data, original_pdf=self.fileName_choose)
        else:
            QMessageBox.about(None, "No file chosen", "Please pick a pdf file first")

        if self.test:
            self.present_pdf_()
            # Create new thread to wait for connections
            # self.test_present_pdf = threading.Thread(target=self.present_pdf_)
            # self.test_present_pdf.start()
            # self.test_present_pdf.join()

    def present_pdf_(self):
        import subprocess
        chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        p = subprocess.Popen(
            [chrome_path, "destination.pdf"])  # This uses 'Subprocess' to open the file
        returncode = p.wait()  # This waits for the process to close
        print(returncode)

    def init_spinbox(self):
        self.timer_output.setMaximum(1000)

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
            self.PositionX.setText(str(self.combine[self.boxes.currentText()][0]))
            self.PositionY.setText(str(self.combine[self.boxes.currentText()][1]))
        else:
            self.PositionX.setText(' ')
            self.PositionY.setText(' ')

    def pdf_position_set_(self):
        if self.PDF_file_name.text() != '':
            self.position_set_window()
        else:
            QMessageBox.about(None, "No file chosen", "Please pick a pdf file first")

    def position_save(self, x, y):
        self.PositionX.setText(str(x))
        self.PositionY.setText(str(y))

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
        self.fileName_choose, _ = QFileDialog.getOpenFileName(self,
                                                              "Choose PDF file",
                                                              self.cwd,  # start path
                                                              "Text Files (*.pdf)")
        if self.fileName_choose == "":
            QMessageBox.about(None, "No file chosen", "Please try again")
        else:
            self.get_path = self.pdftoimage.run_convert(self.fileName_choose, 0)
            ex.change_path(self.get_path)
            self.PDF_file_name.setText(self.fileName_choose)

    @staticmethod
    def Box_manager_window():
        mainwindow.setVisible(False)
        ch.refresh_box()
        ch.show()

    @staticmethod
    def position_set_window():
        mainwindow.setVisible(False)
        ex.show()


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
        self.Change_box_name.setToolTip('Change the name of item, shortcut key "F2"')
        self.Change_box_name.clicked.connect(self.change_box_name_)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            if self.item_chosen is not '':
                self.delete_box_()
            else:
                QMessageBox.about(None, "No item chosen", "Please click a item first")
        if event.key() == Qt.Key_F2:
            if self.item_chosen is not '':
                self.change_box_name_()
            else:
                QMessageBox.about(None, "No item chosen", "Please click a item first")

    def change_box_name_(self):
        if self.item_chosen is not '':
            # check if item_chosen is key in dict.
            name = self.get_input()
            if self.item_chosen in mw.pictureLabel.videobox:
                mw.pictureLabel.videobox[name] = mw.pictureLabel.videobox.pop(self.item_chosen)
                mw.pictureLabel.delete_box_image(str(self.item_chosen) + '.png')
            else:
                a = get_keys(mw.pictureLabel.videobox, self.item_chosen)
                mw.pictureLabel.videobox[name] = mw.pictureLabel.videobox.pop(a)
                mw.pictureLabel.delete_box_image(str(a) + '.png')
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

                mw.pictureLabel.delete_box_image(str(self.item_chosen) + '.png')
            else:
                a = get_keys(mw.pictureLabel.videobox, self.item_chosen)
                mw.pictureLabel.videobox.pop(a)
                if a in mw.combine:
                    mw.combine.pop(a)
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


class PDF_image(QWidget, Ui_Form):
    def __init__(self, path='resource/example.png'):
        super(QWidget, self).__init__()
        self.setupUi(self)

        self.init_GUI(path)

    def change_path(self, new_path):
        self.image_set(new_path)

    def init_GUI(self, path):
        self.lb = pdf_label(callback_empty_painter=self.callback)
        self.lb.setGeometry(QRect(0, 0, 1000, 1400))
        self.lb.setToolTip('Left button to draw a rect area that need to fill, Right button confirm current position')

        self.image_set(path)
        self.verticalLayout_2.addWidget(self.lb)

        self.lb.setCursor(Qt.CrossCursor)

        self.lb.button_signal.signal[str].connect(self.slot_right_button)

    def image_set(self, path):
        img = cv2.imread(path)
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)

        self.lb.setPixmap(pixmap)

    @staticmethod
    def callback():
        QMessageBox.about(None, "No area drown", "Please press mouse left button to draw a area")

    def slot_right_button(self):
        x, y = self.lb.return_value()
        mw.position_save(x, y)
        self.close()

    def closeEvent(self, event):
        """
        overwrite closeEvent method，execute code when this window closed.
        :param event: close() the event triggered.
        :return: None
        """
        mainwindow.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    mw = OCR_main(mainWindow=mainwindow)
    # mw.set_video("resource/video.mp4", VideoBox.VIDEO_TYPE_OFFLINE, False)
    mw.set_video(0, OCR_main.VIDEO_TYPE_REAL_TIME, True)
    mainwindow.show()
    ch = Box_manager_widget()

    ex = PDF_image()
    sys.exit(app.exec_())
