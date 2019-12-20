import control as C
import matplotlib.pyplot as plt
import numpy as np

tout = np.linspace(0,10,100)

X1 = C.tf([2,1],[1,2,2])

tout,xout = C.impulse_response(X1)

plt.plot(tout,xout)

##Analytic
xa = 2*np.exp(-tout)*np.cos(tout) - np.exp(-tout)*np.sin(tout)

plt.plot(tout,xa,'r--')

plt.show()