import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

plt.close("all")

def DerivativesNonLinear(z,t):
    theta = z[0]
    thetadot = z[1]
    
    l = 1.
    g = 10.
    
    thetac = 0.
    thetadotc = 0.
    
    kp = 26.
    kd = 8.
    
    e = thetac - theta
    edot = thetadotc - thetadot
    u = kp*e + kd*edot
    
    thetaddot = g/l*np.sin(theta) + u*np.cos(theta)/l
    
    zdot = np.asarray([thetadot,thetaddot])
    
    return zdot

def DerivativesLinear(z,t):
    theta = z[0]
    thetadot = z[1]
    
    l = 1.
    g = 10.
    
    thetac = 0.
    thetadotc = 0.
    
    kp = 26.
    kd = 8.
    
    e = thetac - theta
    edot = thetadotc - thetadot
    u = kp*e + kd*edot
    
    
    thetaddot = g/l*theta + u/l
    
    zdot = np.asarray([thetadot,thetaddot])
    
    return zdot
    

tout = np.linspace(0,20,1000)
zinitial = np.asarray([89*np.pi/180.,0])
zout = S.odeint(DerivativesLinear,zinitial,tout)
plt.plot(tout,zout[:,0],label='Linear')


zoutNL = S.odeint(DerivativesNonLinear,zinitial,tout)
plt.plot(tout,zoutNL[:,0],label='Non Linear')

plt.legend()
plt.grid()

plt.show()