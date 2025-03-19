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
    ahat = z[0]
    ahatdot = z[1]
    
    ###FORCING FUNCTION
    forcing_function = (k/m)*a
    ##########################

    ################EQUATIONS O MOTION
    ahatdbldot = forcing_function - (c/m)*ahatdot - (k/m)*ahat
    ###################################################
    zdot = np.asarray([ahatdot,ahatdbldot]) #np is numpy (Numeric Python) and asarray says
    #make [xdot,xdbldot] an array
    return zdot
##############END OF FUNCTION SEPARATED BY TABS#######
    
tout = np.linspace(0,10,100)  #linspace(start,end,number of data points)
zinitial = np.asarray([0,0])

for c in range(0,10,1): ##Uncomment this to change damping ratio
#for k in range(0,10,1):  ##Uncomment this to change stiffness
#for a in range(0,10,1):  ###uncoment this to change forcing value
	zout = I.odeint(Derivatives,zinitial,tout) ##This is the ode toolbox from scipy (Scientific Python)
	ahatout = zout[:,0]
	plt.plot(tout,ahatout)

plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Measured Acceleration (m/s^2)')
plt.show()
