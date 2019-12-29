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

        #Setup default system
        self.defaultSystem()

        #Then populate all the LineEdits
        self.populate()
        
        ##Then plot right away
        if not self.system.verbose:
            self.plot()

        #And integrate the closed loop system
        #self.system.integrateClosedLoop(0,10,ic=np.asarray([0,0]),input='step')

    def defaultSystem(self):
        #Create the default system
        num = np.asarray([1])
        den = np.asarray([1,0])
        self.system = ctldyn.makeSystem(num,den,systype='TF',verbose=False)

        ##From here we need to integrate the open loop system
        self.system.integrateOpenLoop(0,2,ic=np.asarray([0,0]),input='step')

        #Then create a default controller
        #This will also create a root locus and simulate the
        #closed loop system
        self.system.rltools(10,1,5,[],[]) #KMAX,KSTEP,KSTAR,zeros,poles


    def populate(self):
        self.ui.zGEdit.setText("hello")        

    def plot(self):
        #Discard old axis
        self.ui.ax1.clear()
        # plot open loop data
        self.system.plotOpenLoop(self.ui.ax1)

        # create second axis and clear it
        self.ui.ax2.clear()
        self.system.plotrootlocus(self.ui.ax2)

        # third axis
        self.ui.ax3.clear()
        self.system.plotClosedLoop(self.ui.ax3)        

        ##4th axis?? what to do here?
        self.ui.ax4.clear()
        self.system.plotBode(self.ui.ax4)
        
        # refresh canvas
        self.ui.canvas.draw()

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
