#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 21:38:41 2023

@author: carlos
"""

##GAUSS-NEWTON 

### GUASSES - LSR - Least Squares Regression
## y1 = a0 + a1 * x1 = [1 x1]*[a0;a1]
## y2 = a0 + a1 * x2 = [1 x2]*[a0;a1]
## ...
## yn = a0 + a1 * xn = [1 xn]*[a0;a1]
## Y = [y1;y2;...yn] Nx1
## A = [a0;a1] 2x1
## H = [1 x1;1 x2;1 x3;...;1 xn] Nx2
## Y = H*A
## A = (H'*H)^-1 * H' * Y

### NEWTONS METHOD
## x(i+1) = x(i) - alfa*f(x)/f'(x)
## xvec(i+1) = xvec(i) - J^-1*f(x)
## xvec - 2x1
## f - 2x1
## J - 2x2 <- easily invertible

###MODULE
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

##FUNCTIONS
def f(a,x):
    a0 = a[0]
    a1 = a[1]
    y = a0*(1-np.exp(-a1*x))
    return y

def residuals(a,xdata,ydata):
    y = f(a,xdata)
    delta = y-ydata
    return np.transpose(delta)

def cost(a,xdata,ydata):
    return np.sum(residuals(a,xdata,ydata)**2)

def J(a,x):
    a0 = a[0]
    a1 = a[1]
    dfda0 = 1-np.exp(-a1*x)
    dfda1 = a0*x*np.exp(-a1*x)
    return np.transpose(np.vstack((dfda0,dfda1)))

##CREATE MY DATA SET
xdata = np.array([0.25,0.75,1.25,1.75,2.25])
ydata = np.array([0.28,0.57,0.68,0.74,0.79])

##INITIAL GUESS
ai = [1,1]
costi = cost(ai,xdata,ydata)
print('Initial Cost = ',costi)

alfa = 1.0
while alfa > 0.001:
    Ji = J(ai,xdata)
    JTJ = np.matmul(np.transpose(Ji),Ji)
    JTJinv = np.linalg.inv(JTJ)
    JTJ1JT = np.matmul(JTJinv,np.transpose(Ji))
    r = residuals(ai,xdata,ydata)
    #print('residuals = ',r)
    step = np.matmul(JTJ1JT,r)
    #print('step = ',step)
    anext = ai - alfa*step
    costnext = cost(anext,xdata,ydata)
    if costnext > costi:
        alfa = alfa/2.0
        print('Alfa = ',alfa)
    else:
        costi = costnext
        ai = anext
        print('Current Cost = ',costi)

###EVALUATE THE SOLUTION
print('Solution = ',ai)
print('Cost = ',cost(ai,xdata,ydata))
x = np.linspace(np.min(xdata),np.max(xdata),100)
y = f(ai,x)

###PLOT MY FUNCTION
plt.figure()
plt.plot(xdata,ydata,'b*',label='Data')
plt.plot(x,y,'r-',label='NLSR')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.grid()

plt.show()
