# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'box_manager.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UI_box_manager(object):
    def setupUi(self, UI_box_manager):
        UI_box_manager.setObjectName("UI_box_manager")
        UI_box_manager.resize(448, 421)
        UI_box_manager.setStyleSheet("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(UI_box_manager)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(UI_box_manager)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Box_list = QtWidgets.QTableWidget(self.frame)
        self.Box_list.setObjectName("Box_list")
        self.Box_list.setColumnCount(0)
        self.Box_list.setRowCount(0)
        self.verticalLayout.addWidget(self.Box_list)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Change_box_name = QtWidgets.QPushButton(self.frame)
        self.Change_box_name.setObjectName("Change_box_name")
        self.horizontalLayout.addWidget(self.Change_box_name)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.delete_box = QtWidgets.QPushButton(self.frame)
        self.delete_box.setObjectName("delete_box")
        self.horizontalLayout.addWidget(self.delete_box)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(UI_box_manager)
        QtCore.QMetaObject.connectSlotsByName(UI_box_manager)

    def retranslateUi(self, UI_box_manager):
        _translate = QtCore.QCoreApplication.translate
        UI_box_manager.setWindowTitle(_translate("UI_box_manager", "Box_Manager"))
        self.Change_box_name.setText(_translate("UI_box_manager", "Change Name"))
        self.delete_box.setText(_translate("UI_box_manager", "Delete"))
