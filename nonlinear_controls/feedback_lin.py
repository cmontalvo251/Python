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
    k1 = 3
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
xinitial = np.asarray([-1,2])
xout = I.odeint(Derivatives,xinitial,tout)
x1out = xout[:,0]
x2out = xout[:,1]
plt.plot(x1out,x2out)
plt.plot(x1out[0],x2out[0],'b*')
plt.plot(x1out[-1],x2out[-1],'rs')
plt.xlabel('x1')
plt.ylabel('x2')
plt.grid()
plt.show()
