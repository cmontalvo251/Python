# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

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

class Ui_FancyRLTools(object):
    def setupUi(self, FancyRLTools):

        ##Create main window
        FancyRLTools.setObjectName(_fromUtf8("FancyRLTools"))
        FancyRLTools.resize(439, 298)

        ##Create Central Widget
        self.centralwidget = QtGui.QWidget(FancyRLTools)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        ##Create A Grid Layout
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 411, 241))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        ##Create everything inside it
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.convertButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.convertButton.setObjectName(_fromUtf8("convertButton"))
        self.gridLayout.addWidget(self.convertButton, 4, 2, 1, 1)
        self.plotButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.plotButton.setObjectName(_fromUtf8("plotButton"))
        self.gridLayout.addWidget(self.plotButton, 3, 2, 1, 1)
        self.outputEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.outputEdit.setObjectName(_fromUtf8("outputEdit"))
        self.gridLayout.addWidget(self.outputEdit, 3, 1, 1, 1)
        self.inputEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.inputEdit.setObjectName(_fromUtf8("inputEdit"))
        self.gridLayout.addWidget(self.inputEdit, 3, 0, 1, 1)
        self.clearButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.gridLayout.addWidget(self.clearButton, 0, 0, 1, 1)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout.addWidget(self.canvas,0,2,1,1)

        ##Set up menu and status bars
        FancyRLTools.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(FancyRLTools)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 439, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMeters_to_Feet = QtGui.QMenu(self.menubar)
        self.menuMeters_to_Feet.setObjectName(_fromUtf8("menuMeters_to_Feet"))
        FancyRLTools.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(FancyRLTools)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        FancyRLTools.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMeters_to_Feet.menuAction())

        self.retranslateUi(FancyRLTools)
        QtCore.QMetaObject.connectSlotsByName(FancyRLTools)

    def retranslateUi(self, FancyRLTools):
        FancyRLTools.setWindowTitle(_translate("FancyRLTools", "The Fanciest Root Locus", None))
        self.label.setText(_translate("FancyRLTools", "Radians", None))
        self.label_2.setText(_translate("FancyRLTools", "Degrees", None))
        self.convertButton.setText(_translate("FancyRLTools", "Convert", None))
        self.plotButton.setText(_translate("FancyRLTools", "Plot", None))
        self.clearButton.setText(_translate("FancyRLTools", "Clear", None))
        self.menuMeters_to_Feet.setTitle(_translate("FancyRLTools", "The Fanciest Root Locus", None))