###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
 
def Derivatives(xstate,t):
    theta = xstate[0]
    thetadot = xstate[1]
    
    T = 0*(0-theta) + 0*(0-thetadot)

    thetadbldot = -thetadot**3 - 50*theta + T
    
    xstatedot = np.asarray([thetadot,thetadbldot])
    
    return xstatedot

tout = np.linspace(0,30,1000)
xstateinitial = np.asarray([0.01,0])

plt.figure()
for theta in np.arange(-2*np.pi,2*np.pi,1.0):
    for thetadot in np.arange(-2*np.pi,2*np.pi,1.0):
        xstateinitial = np.asarray([theta,thetadot])
        stateout = I.odeint(Derivatives,xstateinitial,tout)
        thetaout = stateout[:,0]
        thetadotout = stateout[:,1]
        l = np.where(np.abs(thetadotout) > 10)[0]
        #print(l)
        if len(l) > 1:
            l = l[0]
        elif len(l) == 0:
            l = len(thetaout)
        plt.plot(thetaout[0:l],thetadotout[0:l])
        plt.plot(thetaout[0],thetadotout[0],'b*')
        plt.plot(thetaout[l-1],thetadotout[l-1],'r*')
        #plt.pause(0.0001)
        plt.axis([-2*np.pi,2*np.pi,-2*np.pi,2*np.pi])

plt.show()

