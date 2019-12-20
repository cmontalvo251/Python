from PyQt4 import QtGui, QtCore
import sys
from mainwindow import Ui_FancyRLTools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MainWindow(QtGui.QMainWindow):
    '''Main window class responsible for managing user interface'''
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_FancyRLTools()
        self.ui.setupUi(self)

        #Connect Slots
        QtCore.QObject.connect(self.ui.convertButton,QtCore.SIGNAL('clicked()'),self.convert)
        QtCore.QObject.connect(self.ui.clearButton,QtCore.SIGNAL('clicked()'),self.clear)
        QtCore.QObject.connect(self.ui.plotButton,QtCore.SIGNAL('clicked()'),self.plot)

    def plot(self):
        try:
            radians = float(self.ui.inputEdit.text() ) 
        except:
            radians = 2*np.pi

        x = np.linspace(-radians,radians,1000)
        y = np.sin(x)

        # create an axis
        ax = self.ui.figure.add_subplot(221)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(x,y)

        ax2 = self.ui.figure.add_subplot(222)
        ax2.clear()
        ax2.plot(y,x)

        ax3 = self.ui.figure.add_subplot(223)
        ax3.clear()
        ax3.plot(y,x,'g-')

        ax4 = self.ui.figure.add_subplot(224)
        ax4.clear()
        ax4.plot(x,y,'r-')

        # refresh canvas
        self.ui.canvas.draw()

    def convert(self):
        print('We will convert stuff here')
        radians = float(self.ui.inputEdit.text())
        print('Radians = ',radians)
        degrees = radians*180./np.pi
        print('Degrees = ',degrees)
        self.ui.outputEdit.setText(str(degrees))

    def clear(self):
        print('We will clear stuff here')
        self.ui.inputEdit.setText("")
        self.ui.outputEdit.setText("")

    def closeEvent(self,event):
        print('put something here if you want something to run when the program quits')

if __name__ == "__main__":

    #start up GUI
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    main.raise_()

    #quit program on exit
    sys.exit(app.exec_())

    #this is cool
