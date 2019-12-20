from control import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as S

g = 9.81
L = 1.0
m = 40.0
M = 70.0
mbar = m+M

B = np.matrix([[0],[1/(M*L)],[0],[1/M]])
A = np.matrix([[0,1,0,0],[g*mbar/(M*L),0,0,0],[0,0,0,1],[g*mbar/M-g,0,0,0]])
Q = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
R = np.matrix("1.0")
p = 1.0

Bode = np.asarray([0,1/(M*L),0,1/M])
Aode = np.asarray(A)

def Derivatives(xvec,t):
    global Klqr,Aode,Bode
    u = -np.matmul(Klqr,xvec)
    xvecdot = np.matmul(Aode,xvec) + Bode*u
    #print(xvecdot)
    return xvecdot

#fig2 = plt.figure()
#plt2 = fig2.add_subplot(1,1,1)

Klqr,riccatti_sol,eigs = lqr(A,B,Q,R)
print('K=',Klqr)
tout = np.linspace(0,300,1000)
xinitial = np.asarray([30*np.pi/180.0,0,0,0])
xout = S.odeint(Derivatives,xinitial,tout)

plt.plot(tout,xout[:,0]*180/np.pi)
plt.xlabel('Time')
plt.ylabel('Angle (deg)')
plt.figure()
plt.plot(tout,xout[:,2])
plt.xlabel('Time')
plt.ylabel('Position (m)')


plt.show()
