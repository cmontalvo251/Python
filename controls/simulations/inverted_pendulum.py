import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

plt.close("all")

g = 9.81
L = 1.0
m = 5.0
K = 10.0
b = 10.0
c = 0.0
theta0 = 50*np.pi/180.
thetac = 0*30*np.pi/180.

def controller(x):
    thetacdot = 0.0
    theta = x[0]
    thetadot = x[1]
    eint = x[2]
    e = thetac - theta
    edot = thetacdot - thetadot
    #T = K(s^2 + b*s + c)/s
    #T = K*s + K*b + K*c/s
    T = K*b*e + K*edot + K*c*eint
    return T,e

def DerivativesNL(x,t):
    theta = x[0]
    thetadot = x[1]
    eint = x[2]
    T,e = controller(x)
    thetaddot = g/L*np.sin(theta) + T/(m*L**2)
    eintdot = e
    xdot = np.asarray([thetadot,thetaddot,eintdot])
    return xdot
    
def Derivatives(x,t):
    theta = x[0]
    thetadot = x[1]
    eint = x[2]
    T,e = controller(x)
    xdot = np.matmul(A,x) + B*T  + B2*e
    return xdot
    
A = np.asarray([[0,1,0],[g/L,0,0],[0,0,0]])
B = np.asarray([0,1/(m*L**2),0])
B2 = np.asarray([0,0,1])
#eigs = np.linalg.eig(A)
#print(eigs)
xinitial = np.asarray([theta0,0,0])
tout = np.linspace(0,20,1000)
xout = S.odeint(Derivatives,xinitial,tout)
xoutNL = S.odeint(DerivativesNL,xinitial,tout)

plt.plot(tout,xout[:,0]*180/np.pi,label="Linear")
plt.plot(tout,xoutNL[:,0]*180./np.pi,'r-',label="Nonlinear")
plt.xlabel('Time (sec)')
plt.ylabel('Angle (deg)')
plt.legend()
plt.grid()

plt.show()