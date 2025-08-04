import sys
from PySide import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)       
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')    
        self.show()
        
        
app = QtGui.QApplication.instance()
standalone = app is None
if standalone:
    app = QtGui.QApplication(sys.argv)



ex = Example()



if standalone:
    sys.exit(app.exec_())
else:
    print "We're back with the Qt window still active"
