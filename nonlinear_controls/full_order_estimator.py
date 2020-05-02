import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

def Derivatives(xtilde,t):
    H = 2.0
    K = 20.0
    F = -1.5*0
    x = 5.0
    ymeasured = H*x + 0.1*np.sin(100*t)
    e = ymeasured - H*xtilde
    xtildedot = F*xtilde + K*e
    return xtildedot

plt.close("all")

tout = np.linspace(0,10,1000)
xinitial = 0
xout = S.odeint(Derivatives,xinitial,tout)

plt.plot(tout,xout[:,0],label='Numerical Integration')

plt.legend()
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('X')

plt.show()