import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S
import control as ctl

x = np.linspace(-np.pi,np.pi,1000)

y1 = x**3
y2 = (np.sin(x))**4

plt.plot(x,y1)
plt.plot(x,y2)
plt.grid()


V = x**4/4 + (1./32.)*(-12.*x + 8*np.sin(2*x) - np.sin(4*x))

Vdot = -(x**3 - np.sin(x)**4)**2

plt.figure()
plt.plot(x,V)
plt.grid()

def Derivatives(x,t):
    xdot = -x**3 + np.sin(x)**4
    return xdot

plt.plot(x,Vdot)
plt.grid()
tout = np.linspace(0,10,100)
plt.figure()
for x0 in x:
    xout = S.odeint(Derivatives,x0,tout)
    plt.plot(tout,xout)
plt.grid()

plt.show()
