###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as C
import scipy.signal as S

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')

#integrate for 10 seconds
tout = np.linspace(0,10,1000)
x1initial = np.linspace(-10,10,1)
x2initial = np.linspace(-10,10,1)
for x1 in x1initial:
	for x2 in x2initial:
		x1eq = 0
		x2eq = 0
		xinitial = np.asarray([x1-x1eq,x2-x2eq])
		xout = I.odeint(Derivatives,xinitial,tout)

		x1out = xout[:,0] + x1eq
		x2out = xout[:,1] + x2eq
		
		Vdot = []
                V = []
                VVdot = []
		for x in xout:
                    x1 = x[0]
                    x2 = x[1]
                    xdot = Derivatives(np.asarray([x1,x2]),0)
                    Vdot.append(x1*xdot[0]+x2*xdot[1])
                    V.append(0.5*x1**2 + 0.5*x2**2)
                    VVdot.append((x1*xdot[0]+x2*xdot[1])*(0.5*x1**2 + 0.5*x2**2))
                Vdot = np.asarray(Vdot)
                V = np.asarray(V)
                VVdot = np.asarray(VVdot)
                ax.plot(x1out,x2out,Vdot)
                ax2.plot(x1out,x2out,V)
                ax3.plot(x1out,x2out,VVdot)
		

#plt.plot(tout,x1out,label='x1')
#plt.plot(tout,x2out,label='x2')
#plt.grid()
#plt.legend()

#plt.figure()
		#plt.plot(x1out,x2out)


#plt.xlim([-10,10])
#plt.ylim([-10,10])
plt.grid()

plt.figure()
plt.plot(tout,V)
plt.plot(tout,Vdot,'r-')
plt.grid()

plt.show()
