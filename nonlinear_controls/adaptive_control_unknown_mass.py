import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as ode

def Derivatives(state,t):
    ##States
    x = state[0]
    xdot = state[1]
    xm = state[2]
    xmdot = state[3]
    mhat = state[4]
    
    ###Parameters
    m = 5.0
    lam = 3.0
    zeta = 0.8
    wn = 2.0
    bm = 2.0
    gam = 3.0
    
    ###reference signal
    r = np.sin(4*t)
    
    ###Error Signals
    xtilde = x - xm
    xtildedot = xdot - xmdot
    
    ###Model Dynamics
    xmddot = bm*r - 2*zeta*wn*xmdot - wn**2*xm
    
    ###Control
    kd = 2*zeta*wn
    kp = wn**2
    v = xmddot - kd*xtildedot - kp*xtilde
    u = mhat*v
    
    ###Plant Dynamics and Kinematics
    #xdot already defined
    xddot = u/m
    
    ###Adaptive Control Dynamics
    s = xtildedot + lam*xtilde
    #mhatdot = -v*s*gam
    mhatdot = -gam*xtildedot*v 
    
    return np.asarray([xdot,xddot,xmdot,xmddot,mhatdot])
    
##Time vector
tout = np.linspace(0,200,10000)
##Initial Conditions
x0 = 0
xdot0 = 0
xm0 = x0
xmdot0 = xdot0
mhat0 = 1.0
state_initial = np.asarray([x0,xdot0,xm0,xmdot0,mhat0])
state_out = ode.odeint(Derivatives,state_initial,tout)

###Extract my states
xout = state_out[:,0]
xmout = state_out[:,2]
mhatout = state_out[:,4]

plt.figure()
plt.plot(tout,xout,label='X')
plt.plot(tout,xmout,label='Xm')
plt.legend()
plt.grid()

plt.figure()
plt.plot(tout,xout-xmout)
plt.grid()

plt.figure()
plt.plot(tout,mhatout)
plt.grid()

plt.show()