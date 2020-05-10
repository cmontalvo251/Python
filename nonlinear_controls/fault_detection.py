import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I

def Derivatives(state,t):
    ##States
    x = state[0]
    xdot = state[1]
    xm = state[2]
    xmdot = state[3]
    ahat = state[4]
    
    ###Parameters
    f = -9.81 #N
    g = 0.9 #Represents half a fault
    m = 1.0 #kg
    r = 20. #m
    
    ###Error Signals
    e = x - xm
    
    ###Model Dynamics
    Ts = 10.0
    zed = 0.8
    #Ts = 4.6/(zed*wn)
    wn = 4.6/(zed*Ts)
    xmddot = -2*zed*wn*xmdot - (wn**2)*xm + (wn**2)*r
    
    ###Control
    v = (wn**2)*(r - x) - 2*zed*wn*xdot - (f/m)
    gamma = 0.002
    ahatdot = -gamma*e*v
    u = ahat*v
    
    ###Plant Dynamics and Kinematics
    xddot = (f/m) + (g/m)*u
    
    return np.asarray([xdot,xddot,xmdot,xmddot,ahatdot])
    

plt.close("all")

##Time vector
tout = np.linspace(0,200,10000)
##Initial Conditions
x0 = 20. ##I think this is right because drone starts at zero roll angle.
xdot0 = 0. ##^^^^^^^^^^^^^
xm0 = 20. ##Let's assume perfect measurement
xmdot0 = 0. ##^^^^^^^^^^^^^
ahat0 = 1.0 #This is our guess of our system
state_initial = np.asarray([x0,xdot0,xm0,xmdot0,ahat0])
state_out = I.odeint(Derivatives,state_initial,tout)

###Extract my states
xout = state_out[:,0]
xmout = state_out[:,2]
ahatout = state_out[:,4]

plt.figure()
plt.plot(tout,xout,label='X')
plt.plot(tout,xmout,label='Xm')
plt.xlabel('Time (s)')
plt.ylabel('Model trajectory')
plt.legend()
plt.grid()

plt.figure()
plt.plot(tout,xout-xmout)
plt.xlabel('Time (s)')
plt.ylabel('Error')
plt.grid()

plt.figure()
plt.plot(tout,ahatout)
plt.xlabel('Time (s)')
plt.ylabel('Ahat')
plt.grid()

plt.show()
