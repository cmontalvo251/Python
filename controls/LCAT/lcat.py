#!/usr/bin/python

from PyQt4 import QtGui, QtCore
import sys
from gui import Ui_GUI
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import controlsystemdynamics as ctldyn

class MainWindow(QtGui.QMainWindow):
    '''Main window class responsible for managing user interface'''
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_GUI()
        self.ui.setupUi(self)

        #Connect Slots
        #QtCore.QObject.connect(self.ui.simulateButton,QtCore.SIGNAL('clicked()'),self.plot)

        #Create the default system
        num = np.asarray([1])
        den = np.asarray([1,0])
        self.system = ctldyn.makeSystem(num,den,systype='TF',verbose=False)

        ##From here we need to integrate the open loop system
        self.system.integrateOpenLoop(0,10,ic=np.asarray([0,0]),input='step')

        #Then create a default controller
        #This will also create a root locus and simulate the
        #closed loop system
        self.system.rltools(100,1,10,[],[]) #KMAX,KSTEP,KSTAR,zeros,poles

        ##Then plot right away
        self.plot()

        #And integrate the closed loop system
        #self.system.integrateClosedLoop(0,10,ic=np.asarray([0,0]),input='step')

    def plot(self):
        x = np.linspace(-np.pi,np.pi,1000)
        y = np.sin(x*30)

        # create an axis
        #ax = self.ui.figure.add_subplot(221)
        # discards the old graph
        self.ui.ax1.clear()

        # plot open loop data
        self.system.plotOpenLoop(self.ui.ax1)

        # create second axis and clear it
        #ax2 = self.ui.figure.add_subplot(222)
        self.ui.ax2.clear()
        self.system.plotrootlocus(self.ui.ax2)

        # third axis
        #ax3 = self.ui.figure.add_subplot(223)
        self.ui.ax3.clear()
        self.system.plotClosedLoop(self.ui.ax3)        

        #ax4 = self.ui.figure.add_subplot(224)
        self.ui.ax4.clear()
        self.ui.ax4.plot(x,y,'r-')

        # refresh canvas
        self.ui.canvas.draw()

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

    #Plot immediately
    main.plot()

    #quit program on exit
    sys.exit(app.exec_())

    #this is cool
