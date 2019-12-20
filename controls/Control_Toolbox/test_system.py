import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S
plt.close("all")
###Zeros poles and gains
tout = np.linspace(0,10,10000)
N,D = S.zpk2tf([0],[-1+1j,-1-1j],2)
sys = ctl.tf(N,D)
print sys

tout,yout = ctl.impulse_response(sys,tout)

plt.plot(tout,yout)

y_analytic = 2*np.exp(-tout)*np.cos(tout)-2*np.exp(-tout)*np.sin(tout)

line,=plt.plot(tout,y_analytic,color='red')
line.set_dashes([2,2])

plt.show()




