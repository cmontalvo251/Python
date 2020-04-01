import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as ode

PRINTED = 1

def Derivatives(state,t):
    global PRINTED 
    ##States
    y = state[0]
    ym = state[1]
    arhat = state[2]
    ayhat = state[3]
    
    ###Parameters
    am = 5.0
    bm = 5.0
    gam = 3.0
    
    ###reference signal
    r = np.sin(4*t)
    
    ###Error Signals
    e = y - ym
    
    ###Model Dynamics
    ymdot = -am*ym + bm*r
    
    ###Control
    kp = am
    v = ymdot - kp*e
    bhat = bm/arhat
    ahat = ayhat*bhat + am
    u = (1/bhat)*(ahat*y + v)
    
    ###Plant Dynamics and Kinematics
    a = 4.0
    b = 2.0
    ydot = -a*y + b*u
    if PRINTED:
        print('ar = ',bm/b)
        print('ay = ',(a-am)/b)
        PRINTED = 0
    
   #Adaptive Controller
    ayhatdot = -gam*e*y
    arhatdot = -gam*e*r
    
    return np.asarray([ydot,ymdot,arhatdot,ayhatdot])
    
##Time vector
tout = np.linspace(0,20,1000)
##Initial Conditions
y0 = 0
ym0 = y0
arhat0 = 1.0
ayhat0 = 1.0
state_initial = np.asarray([y0,ym0,arhat0,ayhat0])
state_out = ode.odeint(Derivatives,state_initial,tout)

###Extract my states
yout = state_out[:,0]
ymout = state_out[:,1]
arhatout = state_out[:,2]
ayhatout = state_out[:,3]

plt.figure()
plt.plot(tout,yout,label='Y')
plt.plot(tout,ymout,label='Ym')
plt.legend()
plt.grid()

plt.figure()
plt.plot(tout,yout-ymout)
plt.grid()

plt.figure()
plt.plot(tout,arhatout)
plt.plot(tout,ayhatout)
plt.grid()

plt.show()
