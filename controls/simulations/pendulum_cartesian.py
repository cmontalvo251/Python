import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
from pdf import *

def Derivatives(xstate,t):
    #print(t)
    #positions
    x = xstate[0]
    y = xstate[1]
    #velocities
    xdot = xstate[2]
    ydot = xstate[3]

    #parameters
    E = 5.8e9
    d = 0.00024
    A = np.pi*(d/2)**2
    k = E*A/L
    w_n = np.sqrt(k/m)
    
    #distance vectors
    d = np.sqrt(x**2 + y**2)
    dhat = (d-L)/d

    #spring forces
    XS = k*dhat*x
    YS = k*dhat*y
    
    #dampening forces
    g = 9.81
    xddot = g - XS/m
    yddot = -YS/m

    xstatedot = np.asarray([xdot,ydot,xddot,yddot])
    
    return xstatedot

ctr = 0
eigs = []
#constants
L = 16.e3/2.
#mvec = np.linspace(12.0+0./3.,40.0,10)
#mvec = [12.0 + 0./3.]
m = 12.0 + 0./3.
wnominal = 8.*2*np.pi/(24.*3600.)
#mvec = np.linspace(wnominal,10*wnominal,10)
mvec = [wnominal]
pp = PDF(0,plt)
#for m in mvec:
for w0 in mvec:
    #integrate to reach steady state
    #tmax = 86400*2 #needs two days to reach steady state
    #tmax = 1000.0
    tmax = 1000
    tspan = np.linspace(0,tmax,10000)
    xstateinitial = np.asarray([L,0,0,0])
    zout = I.odeint(Derivatives,xstateinitial,tspan)

    #pull final states
    x = zout[:,0]
    y = zout[:,1]
    xdot = zout[:,2]
    ydot = zout[:,3]
    x_last = x[-1] 
    y_last = y[-1]
    xdot_last = xdot[-1] 
    ydot_last = ydot[-1]

    plt.figure()
    plt.plot(tspan,x)
    pp.savefig()

    plt.figure()
    plt.plot(tspan,y)
    plt.xlabel('Time')
    plt.ylabel('Flapping Amplitude (m)')
    plt.grid()
    pp.savefig()

    #compute partials for A matrix based on steady state equilibrium point
    xstatefinal = np.asarray([x_last,y_last,xdot_last,ydot_last])
    dx = 1.0e-6
    N = len(xstateinitial)
    Amatrix = np.zeros([N,N])
    for i in range(0,N):
        xstatefinal[i] += dx
        derivs_FORWARD = Derivatives(xstatefinal,tmax)
        xstatefinal[i] -= 2*dx
        derivs_BACKWARD = Derivatives(xstatefinal,tmax)
        xstatefinal[i] += dx
        partial = (derivs_FORWARD-derivs_BACKWARD)/(2*dx)
        Amatrix[:,i] = partial

    [s,v] = np.linalg.eig(Amatrix)
    print('s=',s)
    print('v=',v)

    #plt.close("all")
    plt.figure()
    plt.plot(s[0].real,s[0].imag,"x",color='red',markersize=10)
    plt.plot(s[1].real,s[1].imag,"x",color='red',markersize=10)
    plt.plot(s[2].real,s[2].imag,"x",color='blue',markersize=10)
    plt.plot(s[3].real,s[3].imag,"x",color='blue',markersize=10)
    #plt.plot([-1,1],[0,0],linestyle="--",color='black')
    #plt.plot([-0,0],[-1,1],linestyle="--",color='black')
    #plt.xlim([-0.25,0.05])
    #plt.ylim([-0.005,0.005])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.legend()
    plt.grid()
    pp.savefig()

    eigs.append(s)

pp.close()

plt.close("all")

plt.figure()
ctr = 0
for eig in eigs:
    wns = []
    for e in eig:
        wd = np.imag(e)
        sig = np.real(e)
        wn = np.sqrt(wd**2 + sig**2)
        wns.append(wn)
        plt.plot(mvec[ctr],wn,'bx')
    ctr+=1
    print('wns = ',wns)
#plt.xlabel('Mass (kg)')
plt.xlabel('Spin Rate (rad/s)')
plt.ylabel('Natural Frequency (rad/s)')
plt.grid()
plt.show()