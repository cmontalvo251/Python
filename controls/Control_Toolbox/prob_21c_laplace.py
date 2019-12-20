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

X1 = ctl.tf([2],[1,0,4,0,0,0])
print(X1)
X2 = ctl.tf([1,2],[1,0,4])
print(X2)

X = X1 + X2

tout = np.linspace(0,10,1000)
tout,yout = ctl.impulse_response(X,tout)

plt.plot(tout,yout,'b-',label='Inverse Laplace',LineWidth=6)
plt.xlabel('Time (sec)')
plt.ylabel('X')


#Analytic Solutions
xanalytic = np.sin(2*tout) + 9./8.*np.cos(2*tout) + 1./4.*tout**2 - 1./8.

plt.plot(tout,xanalytic,'r--',label='Davis Again',LineWidth=7)
plt.legend()

plt.grid()
plt.show()