import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I

def Derivatives(state,t):
    ##States
    phi = state[0]
    phidot = state[1]
    phim = state[2]
    phimdot = state[3]
    Ihat = state[4]
    
    ###Parameters
    ##The following inertias are from FASTPilot/FASTRotor/X8/Autopilot.cpp
    ##Ixx = 15.0
    ##Iyy = 15.0
    ##Izz = 20.0
    I = 6.5 ##constant roll inertia
    
    ###Error Signals
    phitilde = phi - phim
    phitildedot = phidot - phimdot
    
    ###Model Dynamics
    ##With self-tuning, there are no model dynamics
    r = 10.*np.pi/180.*np.sin(2*t)
    Ts = 5.0
    zed = 0.1
    wn = 4.6/Ts
    phimddot = -2*zed*wn*phimdot - (wn**2)*phim + (wn**2)*r
    
    ###Control
    ##Pulling these gains from FASTPilot/FASTRotor/X8/Autopilot.cpp
    ##This code doesnt use ki or kyaw. Not sure if we will need it? Need to ask...
    kd = 2*zed*wn
    kp = wn**2
    v = phimddot - kd*phitildedot - kp*phitilde
    T = Ihat*v
    
    ###Plant Dynamics and Kinematics
    #phidot already defined
    # Inertia * ang accel = Torque
    phiddot = T/I
    
    mrac = 20.0
    Ihatdot = -mrac*phitildedot*v
    
    return np.asarray([phidot,phiddot,phimdot,phimddot,Ihatdot])
    

plt.close("all")

##Time vector
tout = np.linspace(0,2000,10000)
##Initial Conditions
phi0 = 0. ##I think this is right because drone starts at zero roll angle.
phidot0 = 0. ##^^^^^^^^^^^^^
phim0 = 0. ##Let's assume perfect measurement
phimdot0 = 0. ##^^^^^^^^^^^^^
Ihat0 = 10. #This is our guess of our inertia
state_initial = np.asarray([phi0,phidot0,phim0,phimdot0,Ihat0])
state_out = I.odeint(Derivatives,state_initial,tout)

###Extract my states
phiout = state_out[:,0]
phimout = state_out[:,2]
Ihatout = state_out[:,4]

plt.figure()
plt.plot(tout,phiout,label='Phi')
plt.plot(tout,phimout,label='Phim')
plt.xlabel('Time (s)')
plt.ylabel('Model trajectory')
plt.legend()
plt.grid()

plt.figure()
plt.plot(tout,phiout-phimout)
plt.xlabel('Time (s)')
plt.ylabel('Error')
plt.grid()

plt.figure()
plt.plot(tout,Ihatout)
plt.xlabel('Time (s)')
plt.ylabel('Inertia (kg-m^2)')
plt.grid()

plt.show()