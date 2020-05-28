import numpy as np 
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import mpl_toolkits.mplot3d as a3

##In order to import this toolbox into a python script you need to 
##do the following. Copy the following lines of code below
# import sys
# sys.path.append('/home/carlos/Dropbox/BlackBox/pdf')
# from pdf import *

# or

# In order to get python to search for all of your lovely blackbox 
# python routines. Add this to your .bashrc file

# for d in /home/carlos/Dropbox/BlackBox/*/; do
# 	PYTHONPATH+=:$d
# done
# export PYTHONPATH

# In order to get this to work in Thonny you need to navigate to
# /home/user/.thonny/BundledPython36/lib/python3.6/site-packages and place
# a symbolic link here

# In Enthough you need to make symbolic links here
# /home/carlos/.local/share/canopy/edm/envs/User/lib/python2.7/site-packages

# For Thonny make symbolic links here
# ~/.thonny/BundledPython36/lib/python3.6/site-packages$ 

class PDF():
    def __init__(self,SHOWPLOTS,plt):
        self.SHOWPLOTS = SHOWPLOTS
        if self.SHOWPLOTS == 0:
            self.pdfhandle = self.SetupPDF()
        else:
            self.plt = plt

    def SetupPDF(self):
        if sys.platform == 'linux2':
            os.system('rm plots.pdf')
        pdfhandle = PdfPages('plots.pdf')
        return pdfhandle

    def close(self):
        if self.SHOWPLOTS == 1:
            self.plt.show()
        else:
            self.pdfhandle.close()
            print('Saving plots...')

            #AND THEN USE EVINCE TO OPEN PDF if on linux
            if 1: #sometimes I just want to turn this off
                if sys.platform == 'linux2' or sys.platform == 'linux':
                    print('Opening Plots')
                    os.system('evince plots.pdf &')
            else:
                print('Just gonna finish rather than opening evince')

    def savefig(self,*extra):
        if self.SHOWPLOTS == 0:
            if len(extra) > 0:
                lgd = extra[0]
                self.pdfhandle.savefig(bbox_extra_artists=(lgd,), bbox_inches='tight')
            else:
                self.pdfhandle.savefig()

# Copyright - Carlos Montalvo 2016
# You may freely distribute this file but please keep my name in here
# as the original owner
