# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GUIMain(object):
    def setupUi(self, GUIMain):
        GUIMain.setObjectName("GUIMain")
        GUIMain.resize(261, 234)
        self.centralwidget = QtWidgets.QWidget(GUIMain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.inputEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.inputEdit.setObjectName("inputEdit")
        self.gridLayout.addWidget(self.inputEdit, 1, 1, 1, 1)
        self.outputEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.outputEdit.setObjectName("outputEdit")
        self.gridLayout.addWidget(self.outputEdit, 0, 1, 1, 1)
        self.convertButton = QtWidgets.QPushButton(self.centralwidget)
        self.convertButton.setObjectName("convertButton")
        self.gridLayout.addWidget(self.convertButton, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setObjectName("clearButton")
        self.gridLayout.addWidget(self.clearButton, 4, 0, 1, 1)
        self.plotButton = QtWidgets.QPushButton(self.centralwidget)
        self.plotButton.setObjectName("plotButton")
        self.gridLayout.addWidget(self.plotButton, 5, 0, 1, 1)
        GUIMain.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GUIMain)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 261, 25))
        self.menubar.setObjectName("menubar")
        self.GUI_TEST = QtWidgets.QMenu(self.menubar)
        self.GUI_TEST.setObjectName("GUI_TEST")
        GUIMain.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(GUIMain)
        self.statusbar.setObjectName("statusbar")
        GUIMain.setStatusBar(self.statusbar)
        self.menubar.addAction(self.GUI_TEST.menuAction())

        self.retranslateUi(GUIMain)
        QtCore.QMetaObject.connectSlotsByName(GUIMain)

    def retranslateUi(self, GUIMain):
        _translate = QtCore.QCoreApplication.translate
        GUIMain.setWindowTitle(_translate("GUIMain", "Test GUI "))
        self.convertButton.setText(_translate("GUIMain", "Convert"))
        self.label.setText(_translate("GUIMain", "Radians"))
        self.label_2.setText(_translate("GUIMain", "Degrees"))
        self.clearButton.setText(_translate("GUIMain", "Clear"))
        self.plotButton.setText(_translate("GUIMain", "Plot"))
        self.GUI_TEST.setTitle(_translate("GUIMain", "GUI_TEST"))

