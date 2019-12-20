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
    
    x1dot = x2
    #xc = 0
    #xdotc = 0
    #kp = 50
    #kd = 30
    #u1 = -kp*(x1-xc) - kd*(x2 - xdotc)
    u1 = 0
    x2dot = -0.6*x2 - 3*x1 - x1**2 + u1
    #x2dot = -3*x1 - 0.6*x2
    #x2dot = 3*x1 - 0.6*x2

    xdot = np.asarray([x1dot,x2dot])

    return xdot #zdot is my output

##Main script
plt.close("all")

#integrate for 10 seconds
tout = np.linspace(0,10,10000)
x1initial = np.linspace(-5,2,30)
x2initial = np.linspace(-5,5,30)
V = np.zeros((len(x1initial),len(x2initial)))
r = 0
for x1 in x1initial:
    c = 0
    for x2 in x2initial:
        x1eq = 0
        x2eq = 0
        xinitial = np.asarray([x1-x1eq,x2-x2eq])
        xdot = Derivatives(xinitial,0)
        V[r][c] = xdot[0]**2 + xdot[1]**2
        c+= 1
    r += 1

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xv, yv = np.meshgrid(x1initial, x2initial, sparse=False, indexing='ij')
ax.contour(xv,yv,V,100)

plt.show()