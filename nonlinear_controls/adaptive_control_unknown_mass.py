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
    a1hat = state[5]
    a0hat = state[6]
    
    ###Parameters
    m = 5.0
    zeta = 0.8
    wn = 2.0
    bm = 2.0
    gam = 30.0
    
    ###reference signal
    if t < 100:
        r = np.sin(4*t)
    else:
        r = np.cos(2*t)         
    
    ###Error Signals
    e = x - xm
    edot = xdot - xmdot
    
    ###Model Dynamics
    xmddot = bm*r - 2*zeta*wn*xmdot - wn**2*xm
    
    ###Control
    kd = 2*zeta*wn
    kp = wn**2
    v = xmddot - kd*edot - kp*e
    u = mhat*v + a1hat*xdot +a0hat*x
    
    ###Plant Dynamics and Kinematics
    #xdot already defined
    xddot = u/m
    
    ###Adaptive Control Dynamics
    mhatdot = -gam*edot*v
    a1hatdot = -gam*edot*xdot*0
    a0hatdot = -gam*edot*x*0
    
    return np.asarray([xdot,xddot,xmdot,xmddot,mhatdot,a1hatdot,a0hatdot])
    
##Time vector
tout = np.linspace(0,200,10000)
##Initial Conditions
x0 = 0
xdot0 = 0
xm0 = x0
xmdot0 = xdot0
mhat0 = 1.0
a0hat0 = 0.0
a1hat0 = 0.0
state_initial = np.asarray([x0,xdot0,xm0,xmdot0,mhat0,a0hat0,a1hat0])
state_out = ode.odeint(Derivatives,state_initial,tout)

###Extract my states
xout = state_out[:,0]
xmout = state_out[:,2]
mhatout = state_out[:,4]
a0hatout = state_out[:,5]
a1hatout = state_out[:,6]

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
plt.plot(tout,a0hatout)
plt.plot(tout,a1hatout)
plt.grid()

plt.show()