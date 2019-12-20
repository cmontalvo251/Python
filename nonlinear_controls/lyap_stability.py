###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as C
import scipy.signal as S

##Create a function

def Derivatives(x,t):
    x1 = x[0] #Oh btw array start with 0 in python not 1 like MATLAb 
    x2 = x[1]
    
    fx2 = -x2*np.cos(x1)
    k1 = 100
    k2 = 0
    gamma = -k1*x1 - k2*x2
    u = (1/np.cos(2*x1))*(gamma - fx2)
    x1dot = -2*x1 + 3*x2 + np.sin(x1)
    x2dot = -x2*np.cos(x1) + u*np.cos(2*x1)

    xdot = np.asarray([x1dot,x2dot])

    return xdot #zdot is my output

##Main script
plt.close("all")

#integrate for 10 seconds
tout = np.linspace(0,10,1000)
x1initial = np.linspace(-10,10,30)
x2initial = np.linspace(-10,10,30)
V = np.zeros((len(x1initial),len(x2initial)))
Vdot = 0*V
r = 0
for x1 in x1initial:
        c = 0
        for x2 in x2initial:
            x1eq = 0
            x2eq = 0
            xinitial = np.asarray([x1-x1eq,x2-x2eq])
            xdot = Derivatives(xinitial,0)
            x1dot = xdot[0]
            x2dot = xdot[1]
            V[r][c] = 0.5*xinitial[0]**2 + 0.5*xinitial[1]**2
            Vdot[r][c] = xinitial[0]*x1dot + xinitial[1]*x2dot
            c+=1
        r+=1

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xv, yv = np.meshgrid(x1initial, x2initial, sparse=False, indexing='ij')
ax.contour(xv,yv,V,100)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
ax2.contour(xv,yv,Vdot,100)

plt.show()