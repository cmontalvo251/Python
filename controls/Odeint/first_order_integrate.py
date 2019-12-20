import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

plt.close("all")

def Derivatives(x,t):
    xdot = -4*x + 3*t
    return xdot
    
tout = np.linspace(0,10,1000)
xinitial = 2
xout = S.odeint(Derivatives,xinitial,tout)
plt.plot(tout,xout)

## Analytic Solution
A = 35./16.
B = 3./4.
C = -3./16.
xanalytic = A*np.exp(-4*tout) + B*tout + C

plt.plot(tout,xanalytic,'r--')

plt.show()