from PyQt4 import QtGui, QtCore
import sys
from mainwindow import Ui_MainWindow

class MainWindow(QtGui.QMainWindow):
    '''Main window class responsible for managing user interface'''
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Connect Slots
        QtCore.QObject.connect(self.ui.convertButton,QtCore.SIGNAL('clicked()'),self.convert)
        QtCore.QObject.connect(self.ui.clearButton,QtCore.SIGNAL('clicked()'),self.clear)

    def convert(self):
        print('We will convert stuff here')
        meters = float(self.ui.inputEdit.text())
        print('Meters = ',meters)
        feet = meters*3.28
        print('Feet = ',feet)
        self.ui.outputEdit.setText(str(feet))

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