import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
from pdf import *

def Derivatives(xstate,t):
    #print(t)
    #positions
    r = xstate[0]
    theta = xstate[1]
    #velocities
    rdot = xstate[2]
    thetadot = xstate[3]

    #parameters
    E = 5.8e9
    d = 0.00024
    A = np.pi*(d/2)**2
    k = E*A/L
    w_n = np.sqrt(k/m)
    
    #spring forces
    XB = k*(r-L)
    
    #Dynamics
    g = 9.81
    
    rddot = g*np.cos(theta) - XB/m + (thetadot**2)*r
    thetaddot = -2*thetadot*rdot/r - (g/r)*np.sin(theta)

    xstatedot = np.asarray([rdot,thetadot,rddot,thetaddot])
    
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
    tmax = 0.000000001
    tspan = np.linspace(0,tmax,10000)
    xstateinitial = np.asarray([L,0,0.0,0.0])
    zout = I.odeint(Derivatives,xstateinitial,tspan)

    #pull final states
    r = zout[:,0]
    theta = zout[:,1]
    rdot = zout[:,2]
    thetadot = zout[:,3]
    r_last = r[-1] 
    theta_last = theta[-1]
    rdot_last = rdot[-1] 
    thetadot_last = thetadot[-1]

    plt.figure()
    plt.plot(tspan,r)
    plt.xlabel('Time (sec)')
    plt.ylabel('Radius (m)')
    plt.grid()
    pp.savefig()

    plt.figure()
    plt.plot(tspan,theta)
    plt.xlabel('Time')
    plt.ylabel('Flapping Amplitude (rad)')
    plt.grid()
    pp.savefig()

    #compute partials for A matrix based on steady state equilibrium point
    xstatefinal = np.asarray([r_last,theta_last,rdot_last,thetadot_last])
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
    #plt.legend()
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
#plt.ylabel('Natural Frequency (rad/s)')
plt.grid()
plt.show()