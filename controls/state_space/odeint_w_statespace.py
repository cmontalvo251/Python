import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sint

##Create A and B Matrices
A =
B =

##create the derivatives routine
def Derivatives(x,t):
    
    return xdot


##Create time vector and initial conditions
tout = np.linspace(0,10,1000)
xinitial =
#Run the integrator
xout = sint.odeint(Derivatives,xinitial,tout)

##Plot everything
plt.plot(tout,xout[:,0],label='x1')
plt.plot(tout,xout[:,1],label='x2')
plt.xlabel('Time (sec)')
plt.ylabel('State ')
plt.legend()
plt.grid()
plt.show()