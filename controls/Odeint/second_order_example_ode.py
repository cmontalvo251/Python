import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

def Derivatives(xvec,t):
    x = xvec[0]
    xdot = xvec[1]
    
    xddot = t**2 - 4*x
    
    xvecdot = np.asarray([xdot,xddot])
    return xvecdot

plt.close("all")

tout = np.linspace(0,10,1000)
xinitial = np.asarray([1,2])
xout = S.odeint(Derivatives,xinitial,tout)

plt.plot(tout,xout[:,0],label='Pythons Best')

###Analytic Solution
xanalytic = np.sin(2*tout) + 9./8.*np.cos(2*tout) + 0.25*tout**2 - 1./8.

plt.plot(tout,xanalytic,'r--',label='Davis Time to Shine')

plt.legend()

plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('X')

plt.show()