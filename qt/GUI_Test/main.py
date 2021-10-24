from PyQt5 import QtGui, QtCore,QtWidgets
import sys
from mainwindowFigure import Ui_GUIMain
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MainWindow(QtWidgets.QMainWindow):
    '''Main window class responsible for managing user interface'''
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_GUIMain()
        self.ui.setupUi(self)

        #Connect Buttons to functions
        self.ui.convertButton.clicked.connect(self.convert)
        self.ui.clearButton.clicked.connect(self.clear)
        self.ui.plotButton.clicked.connect(self.plot)

    def plot(self):
        try:
            radians = float(self.ui.outputEdit.text()) 
        except:
            radians = 2*np.pi

        print(radians)

        x = np.linspace(-radians,radians,1000)
        y = np.sin(x)

        # create an axis
        ax = self.ui.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(x,y)

        ax.grid()

        # refresh canvas
        self.ui.canvas.draw()

    def convert(self):
        self.ui.statusbar.showMessage('We will convert stuff here')
        if len(self.ui.outputEdit.text()) > 0:
            radians = float(self.ui.outputEdit.text())
            print('Radians = ',radians)
            degrees = radians*180./np.pi
            print('Degrees = ',degrees)
            self.ui.inputEdit.setText(str(degrees))
        elif len(self.ui.inputEdit.text()) > 0:
            degrees = float(self.ui.inputEdit.text())
            print('Degrees = ',degrees)
            radians = degrees/180.*np.pi
            print('Radians = ',radians)
            self.ui.outputEdit.setText(str(radians))
        else:
            self.ui.statusbar.showMessage("NO INPUT DETECTED")

    def clear(self):
        print('We will clear stuff here')
        self.ui.inputEdit.setText("")
        self.ui.outputEdit.setText("")
        self.ui.statusbar.showMessage("")

    def closeEvent(self,event):
        print('put something here if you want something to run when the program quits')

if __name__ == "__main__":

    #start up GUI
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    main.raise_()

    #quit program on exit
    sys.exit(app.exec_())
