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
import matplotlib.pyplot as plt
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
        self.width = 489
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

        ###ADD ALL LINEEDITS AND LABELS

        ##LABELS ARE FIRST
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 10, 1, 1, 1)

        self.label_14 = QtGui.QLabel(self.frame)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_2.addWidget(self.label_14, 15, 1, 1, 1)

        self.label_20 = QtGui.QLabel(self.frame)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_2.addWidget(self.label_20, 4, 1, 1, 1)

        self.label_24 = QtGui.QLabel(self.frame)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.gridLayout_2.addWidget(self.label_24, 13, 1, 1, 1)

        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 9, 1, 1, 1)

        self.label_21 = QtGui.QLabel(self.frame)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout_2.addWidget(self.label_21, 5, 1, 1, 1)

        self.label_15 = QtGui.QLabel(self.frame)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_2.addWidget(self.label_15, 16, 1, 1, 1)

        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 8, 1, 1, 1)

        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 6, 1, 1, 1)

        self.label_6 = QtGui.QLabel(self.frame)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 11, 1, 1, 1)

        self.label_13 = QtGui.QLabel(self.frame)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_2.addWidget(self.label_13, 14, 0, 1, 1)

        self.label_28 = QtGui.QLabel(self.frame)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.gridLayout_2.addWidget(self.label_28, 14, 2, 1, 1)

        self.label_19 = QtGui.QLabel(self.frame)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_2.addWidget(self.label_19, 2, 1, 1, 1)

        self.label_10 = QtGui.QLabel(self.frame)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 7, 1, 1, 1)

        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_16 = QtGui.QLabel(self.frame)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_2.addWidget(self.label_16, 17, 1, 1, 1)

        #Third Column Labels
        self.label_18 = QtGui.QLabel(self.frame)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_2.addWidget(self.label_18, 2, 3, 1, 1)

        self.label_7 = QtGui.QLabel(self.frame)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 4, 3, 1, 1)
        
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 5, 3, 1, 1)

        self.label_8 = QtGui.QLabel(self.frame)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 6, 3, 1, 1)

        self.label_25 = QtGui.QLabel(self.frame)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.gridLayout_2.addWidget(self.label_25, 8, 3, 1, 1)

        self.label_23 = QtGui.QLabel(self.frame)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gridLayout_2.addWidget(self.label_23, 10, 3, 1, 1)

        self.label_22 = QtGui.QLabel(self.frame)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.gridLayout_2.addWidget(self.label_22, 11, 3, 1, 1)

        self.label_26 = QtGui.QLabel(self.frame)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.gridLayout_2.addWidget(self.label_26, 13, 3, 1, 1)

        self.label_27 = QtGui.QLabel(self.frame)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.gridLayout_2.addWidget(self.label_27, 15, 3, 1, 1)

        self.label_11 = QtGui.QLabel(self.frame)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 16, 3, 1, 1)

        self.label_12 = QtGui.QLabel(self.frame)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 17, 3, 1, 1)

        
        ##Now add Line Edits and combo boxes in the order you'd like to tab things
        self.sysTypeBox = QtGui.QComboBox(self.frame)
        self.sysTypeBox.setObjectName(_fromUtf8("sysTypeBox"))
        self.sysTypeBox.addItem(_fromUtf8(""))
        self.sysTypeBox.addItem(_fromUtf8(""))
        self.sysTypeBox.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.sysTypeBox, 1, 0, 1, 1)

        self.zGEdit = QtGui.QLineEdit(self.frame)
        self.zGEdit.setObjectName(_fromUtf8("zGEdit"))
        self.gridLayout_2.addWidget(self.zGEdit, 2, 0, 1, 1)

        self.pGEdit = QtGui.QLineEdit(self.frame)
        self.pGEdit.setObjectName(_fromUtf8("pGEdit"))
        self.gridLayout_2.addWidget(self.pGEdit, 4, 0, 1, 1)

        self.kGEdit = QtGui.QLineEdit(self.frame)
        self.kGEdit.setObjectName(_fromUtf8("kGEdit"))
        self.gridLayout_2.addWidget(self.kGEdit, 5, 0, 1, 1)

        self.numGEdit = QtGui.QLineEdit(self.frame)
        self.numGEdit.setObjectName(_fromUtf8("numGEdit"))
        self.gridLayout_2.addWidget(self.numGEdit, 6, 0, 1, 1)

        self.denGEdit = QtGui.QLineEdit(self.frame)
        self.denGEdit.setObjectName(_fromUtf8("denGEdit"))
        self.gridLayout_2.addWidget(self.denGEdit, 7, 0, 1, 1)

        self.ssAEdit = QtGui.QTextEdit(self.frame)
        self.ssAEdit.setObjectName(_fromUtf8("ssAEdit"))
        self.gridLayout_2.addWidget(self.ssAEdit, 8, 0, 1, 1)

        self.ssBEdit = QtGui.QLineEdit(self.frame)
        self.ssBEdit.setObjectName(_fromUtf8("ssBEdit"))
        self.gridLayout_2.addWidget(self.ssBEdit, 9, 0, 1, 1)

        self.ssCEdit = QtGui.QLineEdit(self.frame)
        self.ssCEdit.setObjectName(_fromUtf8("ssCEdit"))
        self.gridLayout_2.addWidget(self.ssCEdit, 10, 0, 1, 1)

        self.ssDEdit = QtGui.QLineEdit(self.frame)
        self.ssDEdit.setText(_fromUtf8(""))
        self.ssDEdit.setObjectName(_fromUtf8("ssDEdit"))
        self.gridLayout_2.addWidget(self.ssDEdit, 11, 0, 1, 1)

        self.createButton = QtGui.QPushButton(self.frame)
        self.createButton.setObjectName(_fromUtf8("createButton"))
        self.gridLayout_2.addWidget(self.createButton, 12, 0, 1, 1)

        self.t0Edit = QtGui.QLineEdit(self.frame)
        self.t0Edit.setObjectName(_fromUtf8("t0Edit"))
        self.gridLayout_2.addWidget(self.t0Edit, 15, 0, 1, 1)
        
        self.tfEdit = QtGui.QLineEdit(self.frame)
        self.tfEdit.setObjectName(_fromUtf8("tfEdit"))
        self.gridLayout_2.addWidget(self.tfEdit, 16, 0, 1, 1)

        self.tnEdit = QtGui.QLineEdit(self.frame)
        self.tnEdit.setObjectName(_fromUtf8("tnEdit"))
        self.gridLayout_2.addWidget(self.tnEdit, 17, 0, 1, 1)

        self.inputBox = QtGui.QComboBox(self.frame)
        self.inputBox.setObjectName(_fromUtf8("inputBox"))
        self.inputBox.addItem(_fromUtf8(""))
        self.inputBox.addItem(_fromUtf8(""))
        self.inputBox.addItem(_fromUtf8(""))
        self.inputBox.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.inputBox, 18, 0, 1, 1)

        self.simulateButton = QtGui.QPushButton(self.frame)
        self.simulateButton.setObjectName(_fromUtf8("simulateButton"))
        self.gridLayout_2.addWidget(self.simulateButton, 19, 0, 1, 1)

        self.importButton = QtGui.QPushButton(self.frame)
        self.importButton.setObjectName(_fromUtf8("importButton"))
        self.gridLayout_2.addWidget(self.importButton, 0, 2, 1, 1)
        
        #Control Design with labels
        self.label_17 = QtGui.QLabel(self.frame)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_2.addWidget(self.label_17, 1, 2, 1, 1)

        self.ssKEdit = QtGui.QLineEdit(self.frame)
        self.ssKEdit.setObjectName(_fromUtf8("ssKEdit"))
        self.gridLayout_2.addWidget(self.ssKEdit, 2, 2, 1, 1)

        self.zCEdit = QtGui.QLineEdit(self.frame)
        self.zCEdit.setObjectName(_fromUtf8("zCEdit"))
        self.gridLayout_2.addWidget(self.zCEdit, 4, 2, 1, 1)

        self.pCEdit = QtGui.QLineEdit(self.frame)
        self.pCEdit.setObjectName(_fromUtf8("pCEdit"))
        self.gridLayout_2.addWidget(self.pCEdit, 5, 2, 1, 1)

        self.kCEdit = QtGui.QLineEdit(self.frame)
        self.kCEdit.setObjectName(_fromUtf8("kCEdit"))
        self.gridLayout_2.addWidget(self.kCEdit, 6, 2, 1, 1)

        self.feedbackButton = QtGui.QPushButton(self.frame)
        self.feedbackButton.setObjectName(_fromUtf8("feedbackButton"))
        self.gridLayout_2.addWidget(self.feedbackButton, 7, 2, 1, 1)

        self.CEdit = QtGui.QTextEdit(self.frame)
        self.CEdit.setObjectName(_fromUtf8("CEdit"))
        self.CEdit.setReadOnly(True)
        self.gridLayout_2.addWidget(self.CEdit, 8, 2, 1, 1)

        self.label_29 = QtGui.QLabel(self.frame)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.gridLayout_2.addWidget(self.label_29, 9, 2, 1, 1)

        self.zGCLEdit = QtGui.QLineEdit(self.frame)
        self.zGCLEdit.setObjectName(_fromUtf8("zGCLEdit"))
        self.gridLayout_2.addWidget(self.zGCLEdit, 10, 2, 1, 1)

        self.pGCLEdit = QtGui.QLineEdit(self.frame)
        self.pGCLEdit.setObjectName(_fromUtf8("pGCLEdit"))
        self.gridLayout_2.addWidget(self.pGCLEdit, 11, 2, 1, 1)

        self.placeButton = QtGui.QPushButton(self.frame)
        self.placeButton.setObjectName(_fromUtf8("placeButton"))
        self.gridLayout_2.addWidget(self.placeButton, 12, 2, 1, 1)

        self.k0Edit = QtGui.QLineEdit(self.frame)
        self.k0Edit.setObjectName(_fromUtf8("k0Edit"))
        self.gridLayout_2.addWidget(self.k0Edit, 15, 2, 1, 1)

        self.kfEdit = QtGui.QLineEdit(self.frame)
        self.kfEdit.setObjectName(_fromUtf8("kfEdit"))
        self.gridLayout_2.addWidget(self.kfEdit, 16, 2, 1, 1)

        self.knEdit = QtGui.QLineEdit(self.frame)
        self.knEdit.setObjectName(_fromUtf8("knEdit"))
        self.gridLayout_2.addWidget(self.knEdit, 17, 2, 1, 1)

        self.locusButton = QtGui.QPushButton(self.frame)
        self.locusButton.setObjectName(_fromUtf8("locusButton"))
        self.gridLayout_2.addWidget(self.locusButton, 18, 2, 1, 1)

        self.exportButton = QtGui.QPushButton(self.frame)
        self.exportButton.setObjectName(_fromUtf8("exportButton"))
        self.gridLayout_2.addWidget(self.exportButton, 19, 2, 1, 1)

        ##These are just diplays so it doesn't really matter what order they are
        self.GEdit = QtGui.QTextEdit(self.frame)
        self.GEdit.setObjectName(_fromUtf8("GEdit"))
        self.GEdit.setReadOnly(True)
        self.gridLayout_2.addWidget(self.GEdit, 13, 0, 1, 1)


        self.GCLEdit = QtGui.QTextEdit(self.frame)
        self.GCLEdit.setObjectName(_fromUtf8("GCLEdit"))
        self.GCLEdit.setReadOnly(True)
        self.gridLayout_2.addWidget(self.GCLEdit, 13, 2, 1, 1)

        ###FINALLY ADD THE FRAME WIDGET TO THE MAIN WINDOW GRID
        self.gridLayout.addWidget(self.frame, 22, 0, 1, 1)

        ##################################################
        ##This 5,1,1,1 basically tells where to put it
        #Add the figure stuff to the gridlayout as well
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(nrows=2, ncols=2)
        #self.figure = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas,GUI)
        plt.tight_layout()
        self.gridLayout.addWidget(self.canvas,22,1,1,1)
        self.gridLayout.addWidget(self.toolbar,21,1,1,1)
        #################################################

        ##Add the central widget to the main window
        GUI.setCentralWidget(self.centralwidget)

        ##ADD A MENU
        self.menubar = QtGui.QMenuBar(GUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        GUI.setMenuBar(self.menubar)

        ##ADD A STATUS BAR
        self.statusbar = QtGui.QStatusBar(GUI)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        GUI.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())

        ##THEN SET SOME FINAL NAMING CONVENSTIONS
        self.retranslateUi(GUI)
        QtCore.QMetaObject.connectSlotsByName(GUI)

    def retranslateUi(self, GUI):

        ##THIS IS WHERE WE NAME EVERYTHING and add things to the combo boxes
        GUI.setWindowTitle(_translate("GUI", "Linear Controls Analysis Tool (LCAT)", None))
        self.label_5.setText(_translate("GUI", "C", None))
        self.label_25.setText(_translate("GUI", "C{s}", None))
        self.label_17.setText(_translate("GUI", "Control Design", None))
        self.label_14.setText(_translate("GUI", "T0", None))
        self.label_20.setText(_translate("GUI", "p", None))
        self.label_2.setText(_translate("GUI", "p", None))
        self.label_24.setText(_translate("GUI", "G{s}", None))
        self.label_27.setText(_translate("GUI", "K0", None))
        self.label_4.setText(_translate("GUI", "B", None))
        self.sysTypeBox.setItemText(0, _translate("GUI", "tf", None))
        self.sysTypeBox.setItemText(1, _translate("GUI", "zpk", None))
        self.sysTypeBox.setItemText(2, _translate("GUI", "ss", None))
        self.label_21.setText(_translate("GUI", "k", None))
        self.label_15.setText(_translate("GUI", "TF", None))
        self.label_3.setText(_translate("GUI", "A", None))
        self.inputBox.setItemText(0, _translate("GUI", "step", None))
        self.inputBox.setItemText(1, _translate("GUI", "impulse", None))
        self.inputBox.setItemText(2, _translate("GUI", "ramp", None))
        self.inputBox.setItemText(3, _translate("GUI", "parabola", None))
        self.label_9.setText(_translate("GUI", "num", None))
        self.label_18.setText(_translate("GUI", "ss K", None))
        self.simulateButton.setText(_translate("GUI", "SIMULATE", None))
        self.importButton.setText(_translate("GUI", "IMPORT", None))
        self.label_6.setText(_translate("GUI", "D", None))
        self.label_26.setText(_translate("GUI", "GCL{s}", None))
        self.label_11.setText(_translate("GUI", "KF", None))
        self.createButton.setText(_translate("GUI", "CREATE", None))
        self.label_13.setText(_translate("GUI", "Simulation", None))
        self.feedbackButton.setText(_translate("GUI", "FEEDBACK", None))
        self.placeButton.setText(_translate("GUI", "PLACE", None))
        self.label_28.setText(_translate("GUI", "Root Locus", None))
        self.label_19.setText(_translate("GUI", "z", None))
        self.label_10.setText(_translate("GUI", "den", None))
        self.label_8.setText(_translate("GUI", "k", None))
        self.label.setText(_translate("GUI", "Plant Design", None))
        self.label_7.setText(_translate("GUI", "z", None))
        self.label_23.setText(_translate("GUI", "GCL z", None))
        self.label_22.setText(_translate("GUI", "GCL p", None))
        self.locusButton.setText(_translate("GUI", "LOCUS", None))
        self.exportButton.setText(_translate("GUI", "EXPORT", None))
        self.label_12.setText(_translate("GUI", "KN", None))
        self.label_16.setText(_translate("GUI", "TN", None))
        self.label_29.setText(_translate("GUI", "Closed Loop", None))
        self.menu.setTitle(_translate("GUI", "Linear Controls Analysis Tool (LCAT)", None))

