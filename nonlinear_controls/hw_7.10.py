import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
from mpl_toolkits.mplot3d import Axes3D

def Derivatives(xstate,t):
    x = xstate[0]
    xdot = xstate[1]
    xddot = xstate[2]
    
    b = 1
    a1 = 1
    a2 = 1

    x_d = 0
    xdot_d = 0
    xddot_d = 0
    xdddot_d = 0

    lam = 1
    k = 10
    
    xtil = x - x_d
    xtildot = xdot - xdot_d
    xtilddot = xddot - xddot_d
    
    s = xtilddot+2*xtildot*lam+lam**2*xtil
    
    bound = 0.5
    if s < bound and s > -bound:
        s_sign = 1/bound*s
    else:
        s_sign = np.sign(s)
                    
    u = 1/b*(a1*xddot**2+a2*(xdot**5)*np.sin(4*x)+xdddot_d-2*xtilddot*lam-lam**2*xtildot-k*s_sign)
    
    xdddot = b*u-a1*xddot**2-a2*(xdot**5)*np.sin(4*x)
    
    xstatedot = np.asarray([xdot,xddot,xdddot])
    
    return xstatedot

plt.close("all")

tspan = np.linspace(0,10,100)
x1vec = np.linspace(-10,10,11)
x2vec = np.linspace(-10,10,11)
x3vec = np.linspace(-10,10,11)
fig4 = plt.figure(4)
ax4 = fig4.add_subplot(111, projection='3d')
for x1 in x1vec:
    for x2 in x2vec:
        for x3 in x3vec:
            xinitial = np.asarray([x1,x2,x3])
            #xstatedot = Derivatives(xstate,t)
            xout = I.odeint(Derivatives,xinitial,tspan)
            plt.figure(1)
            plt.plot(tspan,xout[:,0])
            plt.figure(2)
            plt.plot(tspan,xout[:,1])
            plt.figure(3)
            plt.plot(tspan,xout[:,2])
            ax4.plot(xout[:,0],xout[:,1],xout[:,2])

plt.figure(1)
plt.xlabel('Time (sec)')
plt.ylabel('X')
#plt.title(r"$\lambda$=%0.1f , k=%0.1f , b=%0.1f , $\alpha_1$=%0.1f , $\alpha_2$=%0.1f"%(lam,k,b,a1,a2))
plt.grid()
plt.figure(2)
plt.xlabel('Time (sec)')
plt.ylabel('Xdot')
#plt.title(r"$\lambda$=%0.1f , k=%0.1f , b=%0.1f , $\alpha_1$=%0.1f , $\alpha_2$=%0.1f"%(lam,k,b,a1,a2))
plt.grid()
plt.figure(3)
plt.xlabel('Time (sec)')
plt.ylabel('Xddot')
#plt.title(r"$\lambda$=%0.1f , k=%0.1f , b=%0.1f , $\alpha_1$=%0.1f , $\alpha_2$=%0.1f"%(lam,k,b,a1,a2))
plt.grid()

plt.show()
