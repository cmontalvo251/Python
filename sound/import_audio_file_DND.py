#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt


def FFTReimmann(w,x):
    global dt
    out = 0
    for i in range(0,len(x)):
        ti = dt*i
        out += x[i]*(dt)*np.cos(w*ti)
    return out

#####FOR FAKE DATA###########
# dt = 0.01
# N = 100
# nmax = N
##Make fake accel data
# factual = 15.0
# t = np.arange(0,dt*N,dt)
# f = 9.81*np.sin(2*np.pi*factual*t)
# L = dt*N
############################

####USING AUDIO DATA USE THIS
#data = np.loadtxt('Audio_transposed.txt')
data = np.loadtxt('Audio_truncated.txt')
t = data[:,0]
f = data[:,1]
dt = t[1]-t[0]
L = t[-1]
N = len(f)
nmax = 200
###########################

#plt.plot(t,f)
#plt.show()

wn_fund = 0
anMAX = 0.0
f_fund = 0
# an_vec = [0]*nmax
for i in range(1,nmax+1):
    print('FFT frequency = ' + str(i) + ' out of ' + str(nmax))
    #Frequency
    w = 2.0*i*np.pi/L
    print('Frequency (Hz) = ' + str((i-1)/L))
    #Reimann Sum
    ani = (2.0/L)*FFTReimmann(w,f)
    # an_vec[i] = abs(ani)
    print(ani)
    if abs(ani) > anMAX:
        anMAX = abs(ani)
        wn_fund = w
        f_fund = (i-1)/L

# plt.plot(an_vec)
# plt.show()
print('Fundamental Frequency (Hz) = ',f_fund)
print('anMAX = ',anMAX)
print('L = ',L)
