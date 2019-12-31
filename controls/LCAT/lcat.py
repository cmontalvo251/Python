#!/usr/bin/python

from PyQt4 import QtGui, QtCore
import sys
from gui import Ui_GUI
import numpy as np
import matplotlib.pyplot as plt
import ast
import controlsystemdynamics as ctldyn

##########################TASKS###############################################

#The following tasks are necessary to make the software function properly
#2.) read() function will require subread() functions where only
#certain lineEdits are read depending on button presses
#3.) Connect button presses to functions. Each button press will call
#a subread() function and then perform the computation and then the
#populate routine
#4.) Create the export functionality to first generate all the plots
#individually so you can save them in high res.
#5.) Append to the export routine by exporting the textEdits to a text
#file
#6.) With a file generated get the import routine working
#7.) Rename the program to LInear Systems Analysis (LISA)

#None of the following ideas are necessary to say the least but it would be nice.
#1.) I'd like to have the Frame widget on the left be tabbed so I can
#shrink the window and see the plots more. Partition everything just
#the way you have it just this time have each section on a tab
#2.) Do the same tab stuffs for the plots so you only see one plot at
#a time.

class MainWindow(QtGui.QMainWindow):
    '''Main window class responsible for managing user interface'''
    def __init__(self,v=True,parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.verbose = v
        self.ui = Ui_GUI()
        self.ui.setupUi(self)

        #Connect Slots
        #QtCore.QObject.connect(self.ui.simulateButton,QtCore.SIGNAL('clicked()'),self.plot)

        #Setup default system
        self.defaultSystem()

        #Then populate all the LineEdits
        self.populate()

        ##Then read for debugging
        if self.verbose:
            self.read()
        
        ##Then plot right away
        if not self.system.verbose:
            self.plot()

    def defaultSystem(self):
        #Create the default system
        num = np.asarray([2])
        den = np.asarray([1,2,2])
        self.system = ctldyn.makeSystem(num,den,systype='TF',verbose=self.verbose)
        #print(self.system.sysTF)
        
        ##From here we need to integrate the open loop system
        self.system.integrateOpenLoop(0,10,ic=np.asarray([0,0]),input='step')

        #Then create a default controller
        #This will also create a root locus and simulate the
        #closed loop system
        self.system.rltools(1,10,10,5,[],[]) #K0,KF,KN,KSTAR,zeros,poles

    def read(self):
        system_type = str(self.ui.sysTypeBox.currentText())
        plant_zeros = self.toarray(str(self.ui.zGEdit.text()))
        plant_poles = self.toarray(str(self.ui.pGEdit.text()))
        plant_gain = self.tofloat(str(self.ui.kGEdit.text()))
        plant_num = self.toarray(str(self.ui.numGEdit.text()))
        plant_den = self.toarray(str(self.ui.denGEdit.text()))
        A = self.toarray(str(self.ui.ssAEdit.toPlainText()))
        B = self.toarray(str(self.ui.ssBEdit.text()))
        C = self.toarray(str(self.ui.ssCEdit.text()))
        D = self.toarray(str(self.ui.ssDEdit.text()))
        #G{s} block is readOnly
        t0 = self.tofloat(str(self.ui.t0Edit.text()))
        tf = self.tofloat(str(self.ui.tfEdit.text()))
        tn = self.tofloat(str(self.ui.tnEdit.text()))
        input_type = str(self.ui.inputBox.currentText())
        K = self.toarray(str(self.ui.ssKEdit.text()))
        controller_zeros = self.toarray(str(self.ui.zCEdit.text()))
        controller_poles = self.toarray(str(self.ui.pCEdit.text()))
        controller_gain = self.tofloat(str(self.ui.kCEdit.text()))
        #C{s} block is readOnly
        closed_loop_zeros = self.toarray(str(self.ui.zGCLEdit.text()))
        closed_loop_poles = self.toarray(str(self.ui.pGCLEdit.text()))
        #GCL{s} block is readOnly
        k0 = self.tofloat(str(self.ui.k0Edit.text()))
        kf = self.tofloat(str(self.ui.kfEdit.text()))
        kn = self.tofloat(str(self.ui.knEdit.text()))

    def tostring(self,input):
        if self.verbose:
            print('Numpy (input) = ',input)
        s = np.shape(input)
        if len(s) == 1:
            r = s[0]
            c = 0
        else:
            r = s[0]
            c = s[1]
        output = '['
        for ri in range(0,r):
            if ri > 0:
                output+=','
            if c > 0:
                output += '['
                for ci in range(0,c):
                    if ci > 0:
                        output += ','
                    output+= str(input[ri][ci])
                output += ']'
            else:
                output += str(input[ri])
        output+= ']'
        if self.verbose:
            print('String (output) = ',output)
        return output
        
    def tostring1(self,input):
        if self.verbose:
            print('Numpy (input) = ',input)
        output = str(input)
        if self.verbose:
            print('String (output) = ',output)
        return output

    def tofloat(self,input):
        if self.verbose:
            print('String (input) = ',input)
        output = np.float(input)
        if self.verbose:
            print('Numpy (output) = ',output)
        return output

    def toarray(self,input):
        if self.verbose:
            print('String (input) = ',input)
        input_ = input.replace(' ',',')
        output = np.asarray(ast.literal_eval(input_))
        if self.verbose:
            print('Numpy (output) = ',output)
        return output
        
    def populate(self):
        self.ui.zGEdit.setText(self.tostring(self.system.plant_zeros))
        self.ui.pGEdit.setText(self.tostring(self.system.plant_poles))
        self.ui.kGEdit.setText(self.tostring1(self.system.plant_gain))
        self.ui.numGEdit.setText(self.tostring(self.system.num))
        self.ui.denGEdit.setText(self.tostring(self.system.den))
        self.ui.ssAEdit.setText(self.tostring(self.system.A))
        self.ui.ssBEdit.setText(self.tostring(self.system.B))
        self.ui.ssCEdit.setText(self.tostring(self.system.C))
        self.ui.ssDEdit.setText(self.tostring(self.system.D))
        self.ui.GEdit.setText(self.tostring1(self.system.sysTF))
        self.ui.t0Edit.setText(self.tostring1(self.system.tstart))
        self.ui.tfEdit.setText(self.tostring1(self.system.tend))
        self.ui.tnEdit.setText(self.tostring1(self.system.tn))
        self.ui.ssKEdit.setText(self.tostring(self.system.K))
        self.ui.zCEdit.setText(self.tostring(self.system.controller_zeros))
        self.ui.pCEdit.setText(self.tostring(self.system.controller_poles))
        self.ui.kCEdit.setText(self.tostring1(self.system.KSTAR))
        self.ui.CEdit.setText(self.tostring1(self.system.sysC))
        self.ui.zGCLEdit.setText(self.tostring(self.system.closedloop_zeros))
        self.ui.pGCLEdit.setText(self.tostring(self.system.closedloop_poles))
        self.ui.GCLEdit.setText(self.tostring1(self.system.GCL))
        self.ui.k0Edit.setText(self.tostring1(self.system.K0))
        self.ui.kfEdit.setText(self.tostring1(self.system.KF))
        self.ui.knEdit.setText(self.tostring1(self.system.KN))

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
    main = MainWindow(False) ##Set false so we supress the output
    main.show()
    main.raise_()

    #quit program on exit
    sys.exit(app.exec_())

    #this is cool
