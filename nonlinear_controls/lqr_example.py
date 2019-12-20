from control import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as S

B = np.matrix([[0],[1]])
A = np.matrix([[0,1],[0,0]])
Bode = np.asarray([0,1])
Aode = np.asarray([[0,1],[0,0]])
Q = np.matrix([[1.0,0],[0,0]])
R = np.matrix("1.0")
p = 1.0

def Derivatives(xvec,t):
    global K

    u = np.matmul(K,xvec)
    #u = -np.matmul(Klqr,xvec)

    xvecdot = np.matmul(Aode,xvec) + Bode*u

    return xvecdot

plt.close("all")
fig1 = plt.figure()
plt1 = fig1.add_subplot(1,1,1)
#fig2 = plt.figure()
#plt2 = fig2.add_subplot(1,1,1)

for q in np.linspace(0.1,100,3):
    #roots = np.roots([1,0,0,0,p])
    #sdesired = roots[0]
    print('------------------')
    print('Q = ',q)
    #print('These Roots',roots)
    #print('Desired Root',sdesired)
    #real_part = np.real(sdesired)
    #imag_part = np.imag(sdesired)
    #k2 = -real_part*2.0
    #k1 = (k2**2 - (-imag_part*2.0)**2)/4.0
    #print('My Root = ',-k2/2 + (0.5*np.sqrt(k2**2-4*k1))*1j)
    p2 = np.sqrt(p*q)
    p3 = np.sqrt(2*p2*p)
    p1 = p2*p3/p
    k1 = -p2/p
    k2 = -p3/p
    K = np.asarray([k1,k2])
    print('My K = ',-K)
    Klqr,riccatti_sol,eigs = lqr(A,B,Q*q,R)
    print('Python=',Klqr)
    tout = np.linspace(0,10,1000)
    xinitial = np.asarray([3,0])
    xout = S.odeint(Derivatives,xinitial,tout)

    plt1.plot(tout,xout[:,0])

plt.show()
