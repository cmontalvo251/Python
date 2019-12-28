# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

########EXTRA PLOTTING MODULES#################
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
#############################################

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

class Ui_GUI(object):
    def setupUi(self, GUI):

        #MAIN WINDOW SETUP
        GUI.setObjectName(_fromUtf8("GUI"))
        self.width = 300
        GUI.resize(self.width, 300)

        ##CENTRAL WIDGET SETUP
        self.centralwidget = QtGui.QWidget(GUI)

        ##SIZE POLICY SETUP
        #Fixed,Minimum,Maximum,Preferred,MinimumExpanding,Expanding,Ignored
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred) #Horizontal, Vertical
        #sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        ##GRID LAYOUT FOR MAIN WINDOW
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        ###CREATE FRAME
        self.frame = QtGui.QFrame(self.centralwidget)

        ##SIZE POLICY FOR FRAME
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        #sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))

        ###GRID LAYOUT FOR FRAME
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))

        ###ADD ALL LINEEDITS AND LABELS - THESE ARE NOT IN ORDER UNFORTUNATELY
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 10, 1, 1, 1)

        self.label_25 = QtGui.QLabel(self.frame)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.gridLayout_2.addWidget(self.label_25, 8, 3, 1, 1)

        self.label_16 = QtGui.QLabel(self.frame)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_2.addWidget(self.label_16, 7, 2, 1, 1)

        self.label_17 = QtGui.QLabel(self.frame)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_2.addWidget(self.label_17, 0, 2, 1, 1)

        self.lineEdit_6 = QtGui.QLineEdit(self.frame)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.gridLayout_2.addWidget(self.lineEdit_6, 16, 0, 1, 1)

        self.lineEdit_16 = QtGui.QLineEdit(self.frame)
        self.lineEdit_16.setObjectName(_fromUtf8("lineEdit_16"))
        self.gridLayout_2.addWidget(self.lineEdit_16, 2, 2, 1, 1)

        self.label_14 = QtGui.QLabel(self.frame)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_2.addWidget(self.label_14, 15, 1, 1, 1)

        self.label_20 = QtGui.QLabel(self.frame)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_2.addWidget(self.label_20, 4, 1, 1, 1)

        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 4, 3, 1, 1)

        self.label_24 = QtGui.QLabel(self.frame)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.gridLayout_2.addWidget(self.label_24, 13, 1, 1, 1)

        self.label_27 = QtGui.QLabel(self.frame)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.gridLayout_2.addWidget(self.label_27, 15, 3, 1, 1)

        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 9, 1, 1, 1)

        self.comboBox = QtGui.QComboBox(self.frame)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.comboBox, 1, 0, 1, 1)

        self.label_21 = QtGui.QLabel(self.frame)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout_2.addWidget(self.label_21, 5, 1, 1, 1)

        self.lineEdit_2 = QtGui.QLineEdit(self.frame)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_2.addWidget(self.lineEdit_2, 5, 2, 1, 1)

        self.lineEdit_18 = QtGui.QLineEdit(self.frame)
        self.lineEdit_18.setObjectName(_fromUtf8("lineEdit_18"))
        self.gridLayout_2.addWidget(self.lineEdit_18, 11, 2, 1, 1)

        self.lineEdit_5 = QtGui.QLineEdit(self.frame)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.gridLayout_2.addWidget(self.lineEdit_5, 15, 2, 1, 1)

        self.lineEdit_8 = QtGui.QLineEdit(self.frame)
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))
        self.gridLayout_2.addWidget(self.lineEdit_8, 1, 2, 1, 1)

        self.label_15 = QtGui.QLabel(self.frame)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_2.addWidget(self.label_15, 16, 1, 1, 1)

        self.lineEdit_11 = QtGui.QLineEdit(self.frame)
        self.lineEdit_11.setObjectName(_fromUtf8("lineEdit_11"))
        self.gridLayout_2.addWidget(self.lineEdit_11, 4, 2, 1, 1)

        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 8, 1, 1, 1)

        self.lineEdit_3 = QtGui.QLineEdit(self.frame)
        self.lineEdit_3.setText(_fromUtf8(""))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout_2.addWidget(self.lineEdit_3, 11, 0, 1, 1)

        self.comboBox_2 = QtGui.QComboBox(self.frame)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.comboBox_2, 18, 0, 1, 1)

        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 6, 1, 1, 1)

        self.textEdit_3 = QtGui.QTextEdit(self.frame)
        self.textEdit_3.setObjectName(_fromUtf8("textEdit_3"))
        self.gridLayout_2.addWidget(self.textEdit_3, 8, 0, 1, 1)

        self.label_18 = QtGui.QLabel(self.frame)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_2.addWidget(self.label_18, 1, 3, 1, 1)

        self.plotButton = QtGui.QPushButton(self.frame)
        self.plotButton.setObjectName(_fromUtf8("plotButton"))
        self.gridLayout_2.addWidget(self.plotButton, 22, 0, 1, 1)

        self.label_6 = QtGui.QLabel(self.frame)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 11, 1, 1, 1)

        self.inputEdit = QtGui.QLineEdit(self.frame)
        self.inputEdit.setObjectName(_fromUtf8("inputEdit"))
        self.gridLayout_2.addWidget(self.inputEdit, 9, 0, 1, 1)

        self.lineEdit_14 = QtGui.QLineEdit(self.frame)
        self.lineEdit_14.setObjectName(_fromUtf8("lineEdit_14"))
        self.gridLayout_2.addWidget(self.lineEdit_14, 7, 0, 1, 1)

        self.label_26 = QtGui.QLabel(self.frame)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.gridLayout_2.addWidget(self.label_26, 13, 3, 1, 1)

        self.lineEdit_13 = QtGui.QLineEdit(self.frame)
        self.lineEdit_13.setObjectName(_fromUtf8("lineEdit_13"))
        self.gridLayout_2.addWidget(self.lineEdit_13, 10, 0, 1, 1)

        self.lineEdit_10 = QtGui.QLineEdit(self.frame)
        self.lineEdit_10.setObjectName(_fromUtf8("lineEdit_10"))
        self.gridLayout_2.addWidget(self.lineEdit_10, 5, 0, 1, 1)

        self.textEdit = QtGui.QTextEdit(self.frame)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_2.addWidget(self.textEdit, 13, 0, 1, 1)

        self.lineEdit = QtGui.QLineEdit(self.frame)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_2.addWidget(self.lineEdit, 15, 0, 1, 1)

        self.label_11 = QtGui.QLabel(self.frame)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 16, 3, 1, 1)

        self.clearButton = QtGui.QPushButton(self.frame)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.gridLayout_2.addWidget(self.clearButton, 12, 0, 1, 1)

        self.textEdit_2 = QtGui.QTextEdit(self.frame)
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.gridLayout_2.addWidget(self.textEdit_2, 8, 2, 1, 1)

        self.label_13 = QtGui.QLabel(self.frame)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_2.addWidget(self.label_13, 14, 0, 1, 1)

        self.convertButton = QtGui.QPushButton(self.frame)
        self.convertButton.setObjectName(_fromUtf8("convertButton"))
        self.gridLayout_2.addWidget(self.convertButton, 6, 2, 1, 1)

        self.lineEdit_4 = QtGui.QLineEdit(self.frame)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout_2.addWidget(self.lineEdit_4, 16, 2, 1, 1)

        self.textEdit_4 = QtGui.QTextEdit(self.frame)
        self.textEdit_4.setObjectName(_fromUtf8("textEdit_4"))
        self.gridLayout_2.addWidget(self.textEdit_4, 13, 2, 1, 1)

        self.pushButton = QtGui.QPushButton(self.frame)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_2.addWidget(self.pushButton, 12, 2, 1, 1)

        self.label_28 = QtGui.QLabel(self.frame)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.gridLayout_2.addWidget(self.label_28, 14, 2, 1, 1)

        self.label_19 = QtGui.QLabel(self.frame)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_2.addWidget(self.label_19, 2, 1, 1, 1)

        self.lineEdit_15 = QtGui.QLineEdit(self.frame)
        self.lineEdit_15.setObjectName(_fromUtf8("lineEdit_15"))
        self.gridLayout_2.addWidget(self.lineEdit_15, 6, 0, 1, 1)

        self.label_10 = QtGui.QLabel(self.frame)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 7, 1, 1, 1)

        self.label_8 = QtGui.QLabel(self.frame)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 5, 3, 1, 1)

        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_19 = QtGui.QLineEdit(self.frame)
        self.lineEdit_19.setObjectName(_fromUtf8("lineEdit_19"))
        self.gridLayout_2.addWidget(self.lineEdit_19, 2, 0, 1, 1)

        self.lineEdit_17 = QtGui.QLineEdit(self.frame)
        self.lineEdit_17.setObjectName(_fromUtf8("lineEdit_17"))
        self.gridLayout_2.addWidget(self.lineEdit_17, 10, 2, 1, 1)

        self.lineEdit_12 = QtGui.QLineEdit(self.frame)
        self.lineEdit_12.setObjectName(_fromUtf8("lineEdit_12"))
        self.gridLayout_2.addWidget(self.lineEdit_12, 4, 0, 1, 1)

        self.label_7 = QtGui.QLabel(self.frame)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 2, 3, 1, 1)

        self.lineEdit_7 = QtGui.QLineEdit(self.frame)
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))
        self.gridLayout_2.addWidget(self.lineEdit_7, 17, 0, 1, 1)

        self.label_23 = QtGui.QLabel(self.frame)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gridLayout_2.addWidget(self.label_23, 11, 3, 1, 1)

        self.label_22 = QtGui.QLabel(self.frame)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.gridLayout_2.addWidget(self.label_22, 10, 3, 1, 1)

        self.label_29 = QtGui.QLabel(self.frame)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.gridLayout_2.addWidget(self.label_29, 9, 2, 1, 1)

        self.lineEdit_9 = QtGui.QLineEdit(self.frame)
        self.lineEdit_9.setObjectName(_fromUtf8("lineEdit_9"))
        self.gridLayout_2.addWidget(self.lineEdit_9, 17, 2, 1, 1)

        self.label_12 = QtGui.QLabel(self.frame)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 17, 3, 1, 1)

        self.pushButton_2 = QtGui.QPushButton(self.frame)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_2.addWidget(self.pushButton_2, 18, 2, 1, 1)

        ###FINALLY ADD THE FRAME WIDGET TO THE MAIN WINDOW GRID
        self.gridLayout.addWidget(self.frame, 25, 1, 1, 1)

        ##################################################
        ##This 5,1,1,1 basically tells where to put it
        #Add the figure stuff to the gridlayout as well
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout.addWidget(self.canvas,25,2,1,1)
        #################################################

        ##Add the central widget to the main window
        GUI.setCentralWidget(self.centralwidget)

        ##ADD A MENU
        self.menubar = QtGui.QMenuBar(GUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMeters_to_Feet = QtGui.QMenu(self.menubar)
        self.menuMeters_to_Feet.setObjectName(_fromUtf8("menuMeters_to_Feet"))
        GUI.setMenuBar(self.menubar)

        ##ADD A STATUS BAR
        self.statusbar = QtGui.QStatusBar(GUI)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        GUI.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMeters_to_Feet.menuAction())

        ##THEN SET SOME FINAL NAMING CONVENSTIONS
        self.retranslateUi(GUI)
        QtCore.QMetaObject.connectSlotsByName(GUI)

    def retranslateUi(self, GUI):

        ##THIS IS WHERE WE NAME EVERYTHING
        GUI.setWindowTitle(_translate("GUI", "Linear Systems Analysis", None))
        self.label_5.setText(_translate("GUI", "C", None))
        self.label_25.setText(_translate("GUI", "C", None))
        self.label_16.setText(_translate("GUI", "N", None))
        self.label_17.setText(_translate("GUI", "Control Design", None))
        self.label_14.setText(_translate("GUI", "T0", None))
        self.label_20.setText(_translate("GUI", "p", None))
        self.label_2.setText(_translate("GUI", "p", None))
        self.label_24.setText(_translate("GUI", "G", None))
        self.label_27.setText(_translate("GUI", "K0", None))
        self.label_4.setText(_translate("GUI", "B", None))
        self.comboBox.setItemText(0, _translate("GUI", "tf", None))
        self.comboBox.setItemText(1, _translate("GUI", "zpk", None))
        self.comboBox.setItemText(2, _translate("GUI", "ss", None))
        self.label_21.setText(_translate("GUI", "k", None))
        self.label_15.setText(_translate("GUI", "TF", None))
        self.label_3.setText(_translate("GUI", "A", None))
        self.comboBox_2.setItemText(0, _translate("GUI", "step", None))
        self.comboBox_2.setItemText(1, _translate("GUI", "impulse", None))
        self.comboBox_2.setItemText(2, _translate("GUI", "ramp", None))
        self.comboBox_2.setItemText(3, _translate("GUI", "parabola", None))
        self.label_9.setText(_translate("GUI", "num", None))
        self.label_18.setText(_translate("GUI", "ss K", None))
        self.plotButton.setText(_translate("GUI", "SIMULATE", None))
        self.label_6.setText(_translate("GUI", "D", None))
        self.label_26.setText(_translate("GUI", "GCL", None))
        self.label_11.setText(_translate("GUI", "KF", None))
        self.clearButton.setText(_translate("GUI", "CREATE", None))
        self.label_13.setText(_translate("GUI", "Simulation", None))
        self.convertButton.setText(_translate("GUI", "FEEDBACK", None))
        self.pushButton.setText(_translate("GUI", "PLACE", None))
        self.label_28.setText(_translate("GUI", "Root Locus", None))
        self.label_19.setText(_translate("GUI", "z", None))
        self.label_10.setText(_translate("GUI", "den", None))
        self.label_8.setText(_translate("GUI", "k", None))
        self.label.setText(_translate("GUI", "Plant Design", None))
        self.label_7.setText(_translate("GUI", "z", None))
        self.label_23.setText(_translate("GUI", "GCL p", None))
        self.label_22.setText(_translate("GUI", "GCL z", None))
        self.label_29.setText(_translate("GUI", "Closed Loop", None))
        self.label_12.setText(_translate("GUI", "KN", None))
        self.pushButton_2.setText(_translate("GUI", "LOCUS", None))
        self.menuMeters_to_Feet.setTitle(_translate("GUI", "Linear Systems Analysis", None))

