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

##########################TASKS###############################################

#None of the following ideas are necessary to say the least but it would be nice.


#The following tasks are necessary to make the software function properly

#1.) 


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
        self.system.rltools(1,10,10,5,[],[]) #K0,KF,KN,KSTAR,zeros,poles


    def populate(self):
        self.ui.zGEdit.setText(str(self.system.plant_zeros))
        self.ui.pGEdit.setText(str(self.system.plant_poles))
        self.ui.kGEdit.setText(str(self.system.plant_gain))
        self.ui.numGEdit.setText(str(self.system.num))
        self.ui.denGEdit.setText(str(self.system.den))
        self.ui.ssAEdit.setText(str(self.system.A))
        self.ui.ssBEdit.setText(str(self.system.B))
        self.ui.ssCEdit.setText(str(self.system.C))
        self.ui.ssDEdit.setText(str(self.system.D))
        self.ui.GEdit.setText(str(self.system.sysTF))
        self.ui.t0Edit.setText(str(self.system.tstart))
        self.ui.tfEdit.setText(str(self.system.tend))
        self.ui.tnEdit.setText(str(self.system.tn))
        self.ui.ssKEdit.setText(str(self.system.K))
        self.ui.zCEdit.setText(str(self.system.controller_zeros))
        self.ui.pCEdit.setText(str(self.system.controller_poles))
        self.ui.kCEdit.setText(str(self.system.KSTAR))
        self.ui.CEdit.setText(str(self.system.sysC))
        self.ui.zGCLEdit.setText(str(self.system.closedloop_zeros))
        self.ui.pGCLEdit.setText(str(self.system.closedloop_poles))
        self.ui.GCLEdit.setText(str(self.system.GCL))
        self.ui.k0Edit.setText(str(self.system.K0))
        self.ui.kfEdit.setText(str(self.system.KF))
        self.ui.knEdit.setText(str(self.system.KN))

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
