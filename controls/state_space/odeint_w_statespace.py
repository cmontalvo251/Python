import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sint

##Create A and B Matrices
c = 2.
k = 10.
m = 0.5
A = np.asarray([[0,1],[-k/m,-c/m]])
B = np.asarray([0,1/m])
k1 = 100.0
k2 = 5.0
K = np.asarray([k1,k2])
xc = np.asarray([10,0])

##create the derivatives routine
def Derivatives(x,t):
    u = np.matmul(K,xc-x) ### u (1x1) = K (1x2) * x-xc (2x1)
    #xdot = A*x + B*u
    xdot = np.matmul(A,x) + B*u
    return xdot

##Create time vector and initial conditions
tout = np.linspace(0,10,1000)
xinitial = np.asarray([0,-10])
#Run the integrator
xout = sint.odeint(Derivatives,xinitial,tout)

##Plot everything
plt.plot(tout,xout[:,0],label='x1')
plt.plot(tout,xout[:,1],label='x2')
plt.xlabel('Time (sec)')
plt.ylabel('State ')
plt.legend()
plt.grid()
plt.show()