from PyQt4 import QtGui, QtCore
import sys
from example import Window
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

if __name__ == "__main__":

    #start up GUI
    app = QtGui.QApplication(sys.argv)
    main = Window()
    main.show()
    main.raise_()

    #quit program on exit
    sys.exit(app.exec_())