#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

def FFTReimmannSIN(w,x):
    global dt
    out = 0
    for i in range(0,len(x)):
        ti = dt*i
        out += x[i]*(dt)*np.sin(w*ti)
    return out

def FFTReimmannCOS(w,x):
    global dt
    out = 0
    for i in range(0,len(x)):
        ti = dt*i
        out += x[i]*(dt)*np.cos(w*ti)
    return out

#####FOR FAKE DATA###########
dt = 0.01
N = 100
nmax = N
#Make fake accel data
factual = 30.0
t = np.arange(0,dt*N,dt)
f = 9.81*np.sin(2*np.pi*factual*t)
L = dt*N
############################

####USING AUDIO DATA USE THIS
#data = np.loadtxt('Audio_transposed.txt')
# data = np.loadtxt('Audio_truncated.txt')
# t = data[:,0]
# f = data[:,1]
# dt = t[1]-t[0]
# L = t[-1]
# N = len(f)
# nmax = 200
###########################

#plt.plot(t,f)
#plt.show()

awn_fund = 0
bwn_fund = 0
anMAX = 0.0
bnMAX = 0.0
bf_fund = 0
af_fund = 0
an_vec = [0]*nmax
for i in range(1,nmax):
    print('FFT frequency = ' + str(i) + ' out of ' + str(nmax))
    #Frequency
    w = 2.0*i*np.pi/L
    print('Frequency (Hz) = ' + str((i-1)/L))
    #Reimann Sum
    ani = (2.0/L)*FFTReimmannSIN(w,f)
    bni = (2.0/L)*FFTReimmannCOS(w,f)
    an_vec[i] = abs(ani)
    if abs(ani) > anMAX:
        anMAX = abs(ani)
        awn_fund = w
        af_fund = (i-1)/L
    if abs(bni) > bnMAX:
        bnMAX = abs(bni)
        bwn_fund = w
        bf_fund = (i-1)/L

if af_fund < bf_fund:
    f_fund = af_fund
else:
    f_fund = bf_fund
# plt.plot(an_vec)
# plt.show()
# print('Fundamental Frequency (Hz) = ',af_fund,bf_fund)
print('Fundamental Frequency (Hz) = ',f_fund)
