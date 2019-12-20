###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S

##Create a function

def Derivatives(state,t):
    x = state[0]
    xdot = state[1]
    xddot = 10 - 25*x - 8*xdot
    dstatedt = np.asarray([xdot,xddot])
    return dstatedt

##Main script
plt.close("all")

#integrate for 10 seconds
tout = np.linspace(0,10,10000)
xinitial = np.asarray([0,0])
xout = I.odeint(Derivatives,xinitial,tout)

plt.plot(tout,xout[:,0],label='Odeint Toolbox')

##Analytic Solution
A = -2.0/5.0
B = 4.0*A/3.0
x_analytic = A*np.exp(-4*tout)*np.cos(3*tout) + B*np.exp(-4*tout)*np.sin(3*tout) + 2.0/5.0

line,=plt.plot(tout,x_analytic,label='Analytic Solution')
line.set_dashes([2,2])

plt.legend()

plt.grid()
plt.show()