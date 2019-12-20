###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S
import scipy.linalg as slin

plt.close("all")

[N,D] = S.zpk2tf([5],[-2,-3],[1])

sys = ctl.tf(N,D)

print sys

[p,z] = ctl.matlab.pzmap(sys,True)
plt.plot(np.real(z),np.imag(z),'ro')

plt.show()