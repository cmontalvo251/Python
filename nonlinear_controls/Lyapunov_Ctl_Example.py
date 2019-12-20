###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as C
import scipy.signal as S

b = 2.
m = 4.
k0 = 1.
k1 = 0

##Create a function
def Derivatives(xvec,t):
    global b,m,k0,k1
    x1 = xvec[0] #Oh btw array start with 0 in python not 1 like MATLAb 
    x2 = xvec[1]

    lam = 5.
    gamma = -x1**2 - lam
    
    x1dot = x1**3 + x1*x2
    
    kp = -1000.
    
    u = kp*(x2-gamma)
    x2dot = u
    
    xvecdot = np.asarray([x1dot,x2dot])

    return xvecdot #zdot is my output

##Main script
plt.close("all")

#integrate for 10 seconds
tout = np.linspace(0,10,10000)
x1initial = np.linspace(-10,10,10)
x2initial = np.linspace(-10,10,10)
V = np.zeros((len(x1initial),len(x2initial)))
Vdot = np.zeros((len(x1initial),len(x2initial)))
r = 0
plt.figure()
for x1 in x1initial:
    c = 0
    for x2 in x2initial:
        xinitial = np.asarray([x1,x2])
        xdot = Derivatives(xinitial,0)
        xvecout = I.odeint(Derivatives,xinitial,tout)
        xout = xvecout[:,0]
        xdotout = xvecout[:,1]
        plt.plot(xout,xdotout)
        plt.plot(xout[0],xdotout[0],'g*')
        plt.plot(xout[-1],xdotout[-1],'rs')
        V[r][c] = 0.5*xinitial[0]**2 + 0.5*xinitial[1]**2
        Vdot[r][c] = xinitial[0]*xdot[0] + xinitial[1]*xdot[1]
        c+= 1
    r += 1
    
#plt.xlim([-10,10])
#lt.ylim([-10,10])

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xv, yv = np.meshgrid(x1initial, x2initial, sparse=False, indexing='ij')
ax.plot_surface(xv,yv,V)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xv, yv = np.meshgrid(x1initial, x2initial, sparse=False, indexing='ij')
ax.plot_surface(xv,yv,Vdot)

plt.show()