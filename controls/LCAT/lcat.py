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
#3.5) The state space stuff is completely broken. I have no idea
#what's going on
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
#3.) There is no lineEdit for ICs. Not sure where to put this but if
#you make tabs there will probably be room.
#4.) I don't think ramp and parabola inputs are working
#5.) Controller does not support the ability to take a state space K
#at the moment

class MainWindow(QtGui.QMainWindow):
    '''Main window class responsible for managing user interface'''
    def __init__(self,v=True,parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.verbose = v
        self.ui = Ui_GUI()
        self.ui.setupUi(self)

        ##There are CREATE, SIMULATE, IMPORT, FEEDBACK, PLACE, LOCUS
        ##and EXPORT buttons. Each button press will need to read only
        ##a subset of the fields, perform some necessary calculation
        ##and then run the populate routine

        #Connect Slots
        QtCore.QObject.connect(self.ui.createButton,QtCore.SIGNAL('clicked()'),self.CREATE)
        QtCore.QObject.connect(self.ui.simulateButton,QtCore.SIGNAL('clicked()'),self.SIMULATE)
        QtCore.QObject.connect(self.ui.importButton,QtCore.SIGNAL('clicked()'),self.IMPORT)
        QtCore.QObject.connect(self.ui.feedbackButton,QtCore.SIGNAL('clicked()'),self.FEEDBACK)
        QtCore.QObject.connect(self.ui.placeButton,QtCore.SIGNAL('clicked()'),self.PLACE)
        QtCore.QObject.connect(self.ui.locusButton,QtCore.SIGNAL('clicked()'),self.LOCUS)
        QtCore.QObject.connect(self.ui.exportButton,QtCore.SIGNAL('clicked()'),self.EXPORT)

        #Setup default system
        self.defaultSystem()

        #Then populate all the LineEdits and plots
        self.populate()

        ##Then read for debugging
        #if self.verbose:
        self.readALL()

    def CREATE(self):
        #The create button must first readCREATE
        typ,z,p,k,num,den,A,B,C,D = self.readCREATE()
        #Then depending on the system type it will create a new system
        if typ == 'tf':
            self.system = ctldyn.makeSystem(num,den,systype='TF',verbose=self.verbose)
        elif typ == 'zpk':
            self.system = ctldyn.makeSystem(z,p,k,systype='ZPK',verbose=self.verbose)
        elif typ == 'ss':
            self.system = ctldyn.makeSystem(A,B,C,D,systype='SS',verbose=self.verbose)
        #Once the system is created we need to recompute everything
        #since the entire system has changed
        self.SIMULATE(oc=[1,0])
        self.FEEDBACK() ##FEEDBACK calls the locus routine
        #Then we re-run the populate routine
        self.populate()
            
    def SIMULATE(self,oc=[1,1]):
        ##The simulate button must first readSIMULATE
        t0,tf,tn,typ = self.readSIMULATE()
        #Then we need to simulate the open and closed loop systems
        if oc[0] == 1:
            self.system.integrateOpenLoop(t0,tf,num=tn,ic=np.asarray([0,0]),input=typ)
        if oc[1] == 1:
            self.system.integrateClosedLoop(t0,tf,num=tn,ic=np.asarray([0,0]),input=typ)
        if oc[0] + oc[1] == 2:
            self.populate()

    def IMPORT(self):
        print('Import Button')

    def FEEDBACK(self):
        #The feedback button is the locus button but the
        #user does not need to know that
        #Then again perhaps we could get rid of this button
        #And put the initial conditions in here
        self.LOCUS()
        
    def PLACE(self):
        #The place button will read the desired closed loop poles and
        #zeros and compute the controller required to do so
        #first we need to read the poles and zeros
        z,p = self.readPLACE()
        self.system.place(p)
        #Then populate
        self.populate()

    def LOCUS(self):
        #First things first though we need to read all the control variables
        ssK,z,p,k,typ = self.readFEEDBACK()
        #Then we need to read all the locus variables
        k0,kf,kn = self.readLOCUS()
        #Then run the rltools
        self.system.rltools(k0,kf,kn,k,z,p)
        #Then run the populate routine
        self.populate()

    def EXPORT(self):
        print('Export Button')
                
    def defaultSystem(self):
        #Create the default system
        num = np.asarray([10])
        den = np.asarray([1,2,10])
        self.system = ctldyn.makeSystem(num,den,systype='TF',verbose=self.verbose)
        #print(self.system.sysTF)
        
        ##From here we need to integrate the open loop system
        self.system.integrateOpenLoop(0,5,ic=np.asarray([0,0]),input='step')

        #Then create a default controller
        #This will also create a root locus and simulate the
        #closed loop system
        self.system.rltools(0.1,3,100,2,[-5],[]) #K0,KF,KN,KSTAR,zeros,poles

    def readCREATE(self):
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
        return system_type,plant_zeros,plant_poles,plant_gain,plant_num,plant_den,A,B,C,D
        #G{s} block is readOnly

    def readSIMULATE(self):
        t0 = self.tofloat(str(self.ui.t0Edit.text()))
        tf = self.tofloat(str(self.ui.tfEdit.text()))
        tn = self.tofloat(str(self.ui.tnEdit.text()))
        input_type = str(self.ui.inputBox.currentText())
        return t0,tf,tn,input_type

    def readFEEDBACK(self):
        K = self.toarray(str(self.ui.ssKEdit.text()))
        controller_zeros = self.toarray(str(self.ui.zCEdit.text()))
        controller_poles = self.toarray(str(self.ui.pCEdit.text()))
        controller_gain = self.tofloat(str(self.ui.kCEdit.text()))
        #C{s} block is readOnly

        ##Feedback needs to know whether the system is state space or not
        system_type = str(self.ui.sysTypeBox.currentText())

        return K,controller_zeros,controller_poles,controller_gain,system_type

    def readPLACE(self):
        closed_loop_zeros = self.toarray(str(self.ui.zGCLEdit.text()))
        closed_loop_poles = self.toarray(str(self.ui.pGCLEdit.text()))
        #GCL{s} block is readOnly
        return closed_loop_zeros,closed_loop_poles

    def readLOCUS(self):
        k0 = self.tofloat(str(self.ui.k0Edit.text()))
        kf = self.tofloat(str(self.ui.kfEdit.text()))
        kn = self.tofloat(str(self.ui.knEdit.text()))
        return k0,kf,kn
        
    def readALL(self):
        ##There are CREATE, SIMULATE, IMPORT, FEEDBACK, PLACE, LOCUS
        ##and EXPORT buttons. Each button press will need to read only
        ##a subset of the fields so we need subread functions for
        ##every button press.

        #CREATE fields
        self.readCREATE()

        #SIMULATE Fields
        self.readSIMULATE()

        #IMPORT is a separate functionality

        #FEEDBACK
        self.readFEEDBACK()

        #PLACE
        self.readPLACE()

        #LOCUS
        self.readLOCUS()

        #EXPORT will just read everything which is essentially just
        #this routine

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
            if ri < r and ri != 0:
                output+='\n'
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
        ##Then plot right away
        if not self.system.verbose:
            self.plot()
            
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
