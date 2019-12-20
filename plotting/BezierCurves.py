import math as M
import os
import numpy as np
import matplotlib.pyplot as plt

def makebezier(L,tspeed):
    t = np.linspace(0.0,tspeed,L)
    s = np.zeros((L,1))
    tout = np.zeros((L,1))
    idx = 0 
    for ti in t:
        out = bezier(ti,tspeed)
        s[idx] = out[0]
        tout[idx] = out[1]
        idx+=1

    #Interpolate 
    sout = interp1(tout,s,t)

    return [t,sout]


def bezier(t,tspeed):
    s = 1.0
    if t <= tspeed:
        p0f = 0.0
        tau = 0.8
        p1f = tau*tspeed
        p2f = (1-tau)*tspeed
        p3f = tspeed
        tau = t/tspeed
        tout = 3*tau*(1-tau)**2*(p1f) + 3*tau**2*(1-tau)*(p2f) + tau**3*p3f;

        p0y = 0.0
        p1y = 0.0
        p2y = 1.0
        p3y = 1.0
        s = (1-tau)**3*p0y + 3*tau*(1-tau)**2*(p1y) + 3*tau**2*(1-tau)*(p2y) + tau**3*p3y ;
        
    return [s,tout]

def find(xi,x):
    jdx = 0
    while x[jdx] < xi and jdx < len(x)-1:
        jdx += 1                

    if jdx == 0:
        jdx += 1

    return jdx

def interp1(x,y,xstar):
    L = np.size(xstar)
    yout = np.zeros((L,1))
    for idx in range(0,L):
        if L > 1:
            xi = xstar[idx]
        else:
            xi = xstar
        jdx = find(xi,x)
        if jdx == L-1:
            yout[idx] = y[-1]
        else:
            m = (y[jdx]-y[jdx-1])/(x[jdx]-x[jdx-1])
            yout[idx] = m*(xi-x[jdx-1]) + y[jdx-1]
        
    return yout

###########################

tspeed = 2
beziers = makebezier(100,tspeed)    
tbez = beziers[0]
sbez = beziers[1]

P = 50

t = np.linspace(0,10.0,P);
s = np.zeros((P,1))
idx = 0
for ti in t:
    s[idx] = interp1(tbez,sbez,ti)
    idx+=1

plt.plot(t,s)
plt.show()


    

# Copyright - Carlos Montalvo 2015
# You may freely distribute this file but please keep my name in here
# as the original owner

# Copyright - Carlos Montalvo 2015
# You may freely distribute this file but please keep my name in here
# as the original owner
