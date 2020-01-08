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
        UI_box_manager.resize(348, 315)
        UI_box_manager.setStyleSheet("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(UI_box_manager)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Box_list = QtWidgets.QScrollArea(UI_box_manager)
        self.Box_list.setWidgetResizable(True)
        self.Box_list.setObjectName("Box_list")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 328, 264))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.Box_list.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.Box_list)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.box_delete = QtWidgets.QPushButton(UI_box_manager)
        self.box_delete.setObjectName("box_delete")
        self.horizontalLayout.addWidget(self.box_delete)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Change_name = QtWidgets.QPushButton(UI_box_manager)
        self.Change_name.setObjectName("Change_name")
        self.horizontalLayout.addWidget(self.Change_name)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(UI_box_manager)
        QtCore.QMetaObject.connectSlotsByName(UI_box_manager)

    def retranslateUi(self, UI_box_manager):
        _translate = QtCore.QCoreApplication.translate
        UI_box_manager.setWindowTitle(_translate("UI_box_manager", "Box_Manager"))
        self.box_delete.setText(_translate("UI_box_manager", "Delete"))
        self.Change_name.setText(_translate("UI_box_manager", "Change Name"))
