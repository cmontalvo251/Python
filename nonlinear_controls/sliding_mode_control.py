import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

lam = 0.7
x_d = 0
xdot_d = 0
xddot_d = 0

def Derivatives(xvec,t):
    x = xvec[0]
    xdot = xvec[1]
    
    eta = 3. #Whatever
    F = 2.5*xdot**2*np.cos(3*x) ###How bad can I be?
    k = F + eta
    xtildedot = xdot - xdot_d
    
    f = -2500*xdot**2*np.cos(3*x)
    fhat = -0.0*xdot**2*np.cos(3*x)
    
    xtilde = x - x_d
    s = xtildedot + lam*xtilde
    u = xddot_d - fhat - lam*xtildedot - k*np.sign(s)
    xddot = f + u
    
    xvecdot = np.asarray([xdot,xddot])
    return xvecdot

plt.close("all")

tout = np.linspace(0,20,1000)
x1vec = np.linspace(-0.5,0.5,9)
x2vec = np.linspace(-0.5,0.5,9)
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

x_d = 0.
xdot_d = 0.
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xv, yv = np.meshgrid(x2vec, x1vec, sparse=False, indexing='ij')
xtilde = xv - x_d
xtildedot = yv - xdot_d
s = xtildedot + lam*xtilde
#s = 0
# xdot + lam*x = 0
# xdot = -lam*x
s1D = -lam*x1vec + lam*x1vec
ax.plot_wireframe(xv,yv,s)
ax.plot(x1vec,-lam*x1vec,s1D,'r-')

plt.show()
