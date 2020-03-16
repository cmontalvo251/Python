import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S
import scipy.linalg as slin

##This makes a vector of K values from 0 to 10 with 1000 data points
K = np.linspace(0,10,100)

##This drops a figure down
plt.figure()

##This loops through my K values
for Ki in K:
    #print(Ki)
    
    ###This computes the roots of the polynomial based on the particular value of K in the loop
    s = np.roots([1,5,10,10,5,Ki])
    #print(s)
    
    ###This plots the real and imaginary components on the s-plane
    plt.plot(np.real(s),np.imag(s),'b*')
    plt.pause(0.0001)
    #this is me typing randomly so we see how the audio shakes out.
    
    
plt.show()