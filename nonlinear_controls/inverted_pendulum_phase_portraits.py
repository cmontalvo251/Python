###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl

m = 1.0
g = 9.81
L = 2.0
c = 0.3
 
def Controller(xstate,t):
    thetac = 0.0
    thetadotc = 0.0
    theta = xstate[0]
    thetadot = xstate[1]
    error = thetac-theta
    errordot = thetadotc-thetadot
    kp = 100.0
    kd = 40.0
    T = kp*error + kd*errordot
    T = 0
    
    return T
 

def Derivatives(xstate,t):
    global m,g,L,c
    theta = xstate[0]
    thetadot = xstate[1]
    
    T = Controller(xstate,t)  
  
    
    thetadbldot = g/L*np.sin(theta) + T/(m*L**2) - c*thetadot
    
    xstatedot = np.asarray([thetadot,thetadbldot])
    
    return xstatedot

def DerivativesLINEARA(xstate,t):
    global m,g,L,c
    theta = xstate[0]
    thetadot = xstate[1]
    
    T = Controller(xstate,t)  
  
    theta0 = 0
    thetadbldot = g/L*np.cos(theta0)*theta + T/(m*L**2) - c*thetadot
    
    xstatedot = np.asarray([thetadot,thetadbldot])
    
    return xstatedot

def DerivativesLINEARB(xstate,t):
    global m,g,L,c
    theta = xstate[0]
    thetadot = xstate[1]
    
    T = Controller(xstate,t)  
  
    theta0 = np.pi
    thetadbldot = g/L*np.cos(theta0)*theta + T/(m*L**2) - c*thetadot
    
    xstatedot = np.asarray([thetadot,thetadbldot])
    
    return xstatedot

tout = np.linspace(0,30,1000)
xstateinitial = np.asarray([0.01,0])
stateout = I.odeint(Derivatives,xstateinitial,tout)

thetaout = stateout[:,0]
thetadotout = stateout[:,1]
plt.plot(tout,thetaout)

##There are 2 types of eq pts
#0,2pi,4pi
A0 = np.asarray([[0,1],[g/L*np.cos(0),-c]])
[s0,v0] = np.linalg.eig(A0)
print(s0)
print(v0)
#pi,3pi,5pi
Api = np.asarray([[0,1],[g/L*np.cos(np.pi),-c]])
[spi,vpi] = np.linalg.eig(Api)
print(spi)
print(vpi)

plt.figure()
for theta in np.arange(-2*np.pi,2*np.pi,1.0):
    for thetadot in np.arange(-2*np.pi,2*np.pi,1.0):
        xstateinitial = np.asarray([theta,thetadot])
        stateout = I.odeint(Derivatives,xstateinitial,tout)
        thetaout = stateout[:,0]
        thetadotout = stateout[:,1]
        plt.plot(thetaout,thetadotout)
        #plt.pause(0.0001)
        plt.axis([-2*np.pi,2*np.pi,-2*np.pi,2*np.pi])

plt.show()

