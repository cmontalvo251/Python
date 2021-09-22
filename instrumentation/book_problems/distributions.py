import control as ctl
import numpy as np
import matplotlib.pyplot as plt
import math as M


x = np.arange(0,10,1)

print(x)

lam = 3.0
P = []
Psum = []
for xi in x:
    Pi = np.exp(-lam)*lam**xi/np.math.factorial(xi)
    P.append(Pi)
    if len(Psum) == 0:
        Psum.append(Pi)
    else:
        Psum.append(Psum[-1]+Pi)
             
plt.plot(x,P,'b*')
plt.grid()

print(np.sum(P))

plt.figure()
plt.plot(x,Psum,'b*')

#####Gaussian Distribution

mean = 110.0
stddev = 30.0

x = np.linspace(mean-3*stddev,mean+3*stddev,1000)
f = (1.0/(stddev*np.sqrt(2*np.pi)))*np.exp(-(x-mean)**2/(2*stddev**2))
f2 = (1.0/(stddev*0.5*np.sqrt(2*np.pi)))*np.exp(-(x-mean)**2/(2*(stddev*0.5)**2))

plt.figure()
plt.plot(x,f)
plt.plot(x,f2,'r-')




plt.show()