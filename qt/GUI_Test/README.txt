##For this readme I'll walk you through how to set all this up.

I'm doing this all on Ubuntu 18.04 so if you're using Windows you're on your own.

First you need to use Qt Designer to open the *.ui and edit the GUI. Designing your
GUI is a tutorial in and of itself so for now just try and open it and make sure
you can see it.

The next thing you need to do is convert the *.ui to *.py module that you can use
to import using Python.

$ pyuic5 mainwindow.ui > mainwindow.py

That will use a built in pythonqt5 module to conver the UI to a PY module. Note
that you obviously need the pyqt5 module to get this to work. If you open mainwindow.py
in a text editor you should see this at the top

from PyQt5 import QtCore, QtGui, QtWidgets

go ahead and open python3 and just make sure you have those modules
installed. If you don't get any errors it means you have those
modules.

The only problem with the current mainwindow.py is that the Figure
object to plot does not exist. So we need to add it manually. These
need to go right before the GUIMain.setCentralWidget() function call.

self.figure = Figure()
self.canvas = FigureCanvas(self.figure)
r = 1 ##This is the row of the plot
c = 1 ##This is the column of the plot
self.gridLayout.addWidget(self.canvas,r,c,1,1)

You also need to add the following modules to the top of the python
module

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

Now you can open the main.py script and see how it works.

######################################3

if __name__ == "__main__":

    #start up GUI
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    main.raise_()

    #quit program on exit
    sys.exit(app.exec_())


#################################

That part of the main.py script is at the bottom and tells the routine
to open the gui and run __init__ routine where we connect all the
buttons to functions. For example the convertBUtton runs the convert
function

go ahead and run

$ python3 main.py

and see if the GUI pops up


