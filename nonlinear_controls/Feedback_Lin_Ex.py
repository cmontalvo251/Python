import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

def Derivatives(xvec,t):
    x1 = xvec[0]
    x2 = xvec[1]
    
    x1dot = np.sin(x2)
    
    ##Feedback Lin on x2
    k1 = 10.
    gamma = -k1*x2
    u = -(x1**4)*np.cos(x2) + gamma
    
    ##Feedback lin on x1
    k1 = 100.
    k2 = 50.
    gamma = -k1*x1 - k2*x1dot
    u = (1./np.cos(x2))*((-x1**4)*np.cos(x2)+gamma)
    
    ###Adaptive Gains on X1
    if x1 == 0:
        k1 = 100.
    else:
        k1 = 10*x1**4
    k2 = k1/2.
    gamma = -k1*x1 - k2*x1dot
    u = (1./np.cos(x2))*((-x1**4)*np.cos(x2)+gamma)
    
    x2dot = (x1**4)*np.cos(x2) + u
    
    xvecdot = np.asarray([x1dot,x2dot])
    return xvecdot

plt.close("all")

tout = np.linspace(0,10,1000)
x1vec = np.linspace(-50,50,4)
x2vec = np.linspace(-50,50,4)
for x1 in x1vec:
    for x2 in x2vec:
        xinitial = np.asarray([x1,x2])
        xout = S.odeint(Derivatives,xinitial,tout)
        plt.plot(xout[:,0],xout[:,1])
        plt.plot(xout[0,0],xout[0,1],'b*')
        plt.plot(xout[-1,0],xout[-1,1],'r*')
plt.xlabel('X1')
plt.ylabel('X2')
plt.grid()

plt.show()