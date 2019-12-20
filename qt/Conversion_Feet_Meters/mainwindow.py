# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(317, 232)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.convertButton = QtGui.QPushButton(self.centralwidget)
        self.convertButton.setGeometry(QtCore.QRect(30, 130, 106, 30))
        self.convertButton.setObjectName(_fromUtf8("convertButton"))
        self.clearButton = QtGui.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(160, 130, 106, 30))
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.inputEdit = QtGui.QLineEdit(self.centralwidget)
        self.inputEdit.setGeometry(QtCore.QRect(30, 30, 113, 29))
        self.inputEdit.setObjectName(_fromUtf8("inputEdit"))
        self.outputEdit = QtGui.QLineEdit(self.centralwidget)
        self.outputEdit.setGeometry(QtCore.QRect(30, 80, 113, 29))
        self.outputEdit.setObjectName(_fromUtf8("outputEdit"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 30, 80, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 90, 80, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 317, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMeters_to_Feet = QtGui.QMenu(self.menubar)
        self.menuMeters_to_Feet.setObjectName(_fromUtf8("menuMeters_to_Feet"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMeters_to_Feet.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.convertButton.setText(_translate("MainWindow", "Convert", None))
        self.clearButton.setText(_translate("MainWindow", "Clear", None))
        self.label.setText(_translate("MainWindow", "Meters", None))
        self.label_2.setText(_translate("MainWindow", "Feet", None))
        self.menuMeters_to_Feet.setTitle(_translate("MainWindow", "Meters to Feet", None))

