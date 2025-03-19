import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I

###Closes all Figures
plt.close("all")

#######THIS IS A FUNCTION CALLED A DEFINITION IN PYTHON
#z and t are input. so z = [x,xdot], z is a 2x1 array with position
# and velocity in it and t is just time.
# matrices are NxM arrays and vectors are Nx1 arrays. Arrays are
# just a way for the computer to handle multiple numbers in one variable

###GLOBAL VARIABLES
##############Change these and watch what happens##########
c = 2.0 
m = 1.0
k = 4.0
a = 1.0
############################################################

def Derivatives(z,t):
    y = z[0]
    dydt = z[1]

    ################EQUATIONS O MOTION
    dy2dt2 = (25 - 1000*y - dydt)/5.0
    ###################################################
    zdot = np.asarray([dydt,dy2dt2]) #np is numpy (Numeric Python) and asarray says
    #make [xdot,xdbldot] an array
    return zdot
##############END OF FUNCTION SEPARATED BY TABS#######
    
tout = np.linspace(0,100,10000)  #linspace(start,end,number of data points)
zinitial = np.asarray([0,0])
zout = I.odeint(Derivatives,zinitial,tout) ##This is the ode toolbox from scipy (Scientific Python)
ahatout = zout[:,0]
plt.plot(tout,ahatout)

plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Measured Acceleration (m/s^2)')
plt.show()
