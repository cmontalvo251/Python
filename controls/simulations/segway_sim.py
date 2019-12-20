import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

plt.close("all")
g = 9.81
l = 1.0
m = 40.0
mm = 70.0
n = m + mm
K = 1000.0
b = 15.0
c = 50.0
theta0 = 30*np.pi/180.
thetac = 0*np.pi/180.

def controller(x):
    thetacdot = 0.0
    theta = x[0]
    thetadot = x[1]
    y = x[2]
    ydot = x[3]
    eint = x[4]
    e = thetac - theta
    edot = thetacdot - thetadot
    yc = 0
    ycdot = 0
    ey = yc - y
    eydot = ycdot - ydot
    #Constant Distrurbance #5
    W = 0.0
    F = K*b*e + K*edot  - 1.0*ey  - 15.4*eydot
    return F,e

def DerivativesNL(x,t):
    theta = x[0]
    thetadot = x[1]
    y = x[2]
    ydot = x[3]
    eint = x[4]
    F,e = controller(x)
    thetaddot = (F*np.cos(theta) - np.sin(theta)*np.cos(theta)*(m*l*thetadot**2)+(n*g*np.sin(theta)))/((n*l)-(m*l*np.cos(theta)**2))
    eintdot = e
    yddot = (l*thetaddot - g*np.sin(theta))/np.cos(theta)
    xdot = np.asarray([thetadot,thetaddot,ydot,yddot,eintdot])
    return xdot
    
xinitial = np.asarray([theta0,0,0,0,0])
tout = np.linspace(0,2000,1000)
xoutNL = S.odeint(DerivativesNL,xinitial,tout)

plt.plot(tout,xoutNL[:,0]*180./np.pi,'r-')
plt.xlabel('Time (sec)')
plt.ylabel('Angle (deg)')
plt.grid()

plt.figure()
plt.plot(tout,xoutNL[:,2],'r-')
plt.xlabel('Time (sec)')
plt.ylabel('Position (m)')
plt.grid()

plt.show()