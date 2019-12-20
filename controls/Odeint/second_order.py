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
def Derivatives(z,t):
    x = z[0]
    xdot = z[1]
    xdbldot = 5*np.sin(3*t) - 6*xdot - 8*x
    zdot = np.asarray([xdot,xdbldot]) #np is numpy (Numeric Python) and asarray says
    #make [xdot,xdbldot] an array
    return zdot
##############END OF FUNCTION SEPARATED BY TABS#######
    
tout = np.linspace(0,10,100)  #linspace(start,end,number of data points)
zinitial = np.asarray([0,0])
zout = I.odeint(Derivatives,zinitial,tout) ##This is the ode toolbox from scipy (Scientific Python)

xout = zout[:,0]

plt.plot(tout,xout,label='Numerical')

za = 15.0/26.0*np.exp(-2*tout) - 3.0/10.0*np.exp(-4*tout) - 1.0/65.0*(18.0*np.cos(3*tout) + np.sin(3*tout))

line,=plt.plot(tout,za,color='red',label='Analytical')
line.set_dashes([2,2])
plt.legend(loc='upper left')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Position (m)')
plt.show()
