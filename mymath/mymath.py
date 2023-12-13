import numpy as np
import matplotlib.pyplot as plt
import plotting as P

##In order to import this toolbox into a python script you need to 
##do the following. Copy the following lines of code below
# import sys
# sys.path.append('/home/carlos/Dropbox/BlackBox/math')
# from math import *

# or
# In order to get python to search for all of your lovely blackbox 
# python routines. Add this to your .bashrc file

# for d in /home/carlos/Dropbox/BlackBox/*/; do
# 	PYTHONPATH+=:$d
# done
# export PYTHONPATH

# In order to get this to work in Thonny you need to navigate to
# /home/user/.thonny/BundledPython36/lib/python3.6/site-packages and place
# a symbolic link here

# In Enthough you need to make symbolic links here
# /home/carlos/.local/share/canopy/edm/envs/User/lib/python2.7/site-packages

def string2binary(text):
    dec = " ".join(str(ord(char)) for char in text).split(" ")
    print(dec)
    return " ".join(bin(int(b)) for b in dec)

def interpolateNans(inX):
    outX = []
    x_new = 0
    for x in inX:
        if not np.isnan(x):
            x_new = x
        outX.append(x_new)

    return np.asarray(outX)

def averages(time,input_stream,avg):
    ##Assume input string is in hrs :(
    ##But avg is in minutes :(
    time_avg = []
    data_avg = []
    t0 = time[0]
    numData = 0.0
    cur_avg = 0.0
    ctr = -1
    for t in time:
        #print t,cur_avg,numData
        ctr+=1
        if t > t0 + avg/60.0:
            ##Append avg
            data_avg.append(cur_avg/numData)
            time_avg.append(t0+avg/60.0)
            ##Reset t0,cur_avg and numData
            t0 = t
            cur_avg = 0.0
            numData = 0.0
        else:
            ##Increment numData and rolling average
            numData+=1.0
            cur_avg+= input_stream[ctr]

    #Get Last Data point
    time_avg.append(t0+avg/60.0)
    data_avg.append(cur_avg/numData)

    return [np.array(time_avg),np.array(data_avg)]

def sec(x):
    return 1/np.cos(x)

def psiwrap(xc,yc,x,y,psi):
    psic = np.arctan2(yc-y,xc-x)
    delpsi = -np.arctan2(np.sin(psi)*np.cos(psic)-np.cos(psi)*np.sin(psic),np.cos(psi)*np.cos(psic)+np.sin(psi)*np.sin(psic));
    return delpsi

def unwrap_simple(inX):
    outX = []
    for x in inX:
        if x > 180:
            x -= 360
        outX.append(x)
    return outX

def unwrap_complex(inX):
    outX = []
    for idx in range(1,len(inX)):
        if abs(inX[idx]-inX[idx-1]) > 180:
            inX[idx] = inX[idx] - 360
    return inX

def unwrap(inX,lower_threshold=0):
    #this will fix timer issues that accidentally reset or it will fix issues with heading wrapping around
    #+-360.
    outX = []
    offset = 0
    for x in inX:
        #make sure you've looped through once
        if len(outX) > 0:
            #Assume the function is monotonically increasing
            if x+offset < outX[-1]:
                offset = outX[-1] - x
        outX.append(x+offset)

    return outX
    
def Reimmann(x,t):
    out = 0
    for i in range(1,len(t)):
        out += x[i]*(t[i]-t[i-1])
    return out 

def fft(f,t,nmax,iplot,pp=None):
    N = len(t)
    tfft = np.linspace(t[0],t[-1],N)
    ffft = np.zeros([len(tfft)])
    if iplot:
        plt.figure()
        plt.plot(t,f,'b-',label='Original Waveform')
    if nmax < 1:
        nmax = 2
    iters = np.arange(1,nmax+1,1)
    an = np.zeros([len(iters)])
    bn = np.zeros([len(iters)])
    L = t[-1]
    d = (1.0/L)*Reimmann(f,t)
    for i in range(0,len(iters)):
        print('FFT frequency = ' + str(i) + ' out of ' + str(len(iters)))
        n = iters[i]
        #Frequency
        w = 2.0*n*np.pi/L
        print('Frequency (Hz) = ' + str(i/(L))
        data_a = np.cos(w*tfft)
        data_b = np.sin(w*tfft)
        #Reimann Sum
        ani = (2.0/L)*Reimmann(data_a*f,t)
        bni = (2.0/L)*Reimmann(data_b*f,t)
        #Save Coefficients
        an[i] = ani
        bn[i] = bni
        #Recreate Waveform
        ffft += ani*data_a + bni*data_b
        if iplot == 2:
            plt.plot(t,f,'b-',label='Original Waveform')
            plt.plot(tfft,ffft,'r--',label='Recreated Waveform')
            plt.pause(0.001)
            plt.cla()
    ffft += d
    frequencies = iters/L
    if iplot:
        plt.plot(tfft,ffft,'r--',label='Recreated Waveform')
        plt.grid()
        plt.legend()
        if pp is not None:
            pp.savefig()
        plt.figure()
        plt.scatter(frequencies,abs(an),color='b',marker='s',label='An')
        plt.scatter(frequencies,abs(bn),color='r',marker='*',label='Bn')
        plt.legend()
        plt.grid()
        plt.xlabel('Frequencies (Hz)')
        plt.ylabel('Magnitude')
        if pp is not None:
            pp.savefig()
    return d,an,bn,iters,frequencies

def Complimentary(sigma,inX):
    outX = np.zeros(len(inX))
    outX[0] = inX[0]
    for idx in range(0,len(inX)-1):
        outX[idx+1] = (1-sigma)*outX[idx] + sigma*inX[idx]
        
    return outX

def Moving_Average(num,inX):
    outX = np.zeros(len(inX))
    window = np.zeros(num)
    ctr = 0
    START_AVERAGING = 0
    for idx in range(0,len(inX)):
        window[ctr] = inX[idx]
        ctr+=1
        if ctr >= num:
            ctr = 0
            START_AVERAGING = 1
        if START_AVERAGING:
            s = np.sum(window)
            avg = s/num
            outX[idx] = avg
    return outX

def LowPass(inY,inX,a):
    dt = inX[1]-inX[0]
    #print("Timestep = ",dt)
    tau = 1.0/a
    #print("Tau = ",tau)
    alfa = 2*tau/dt
    #print("Alfa = ",alfa)
    outY = np.zeros(len(inY))
    outY[0] = inY[0]
    outX = np.zeros(len(inX))
    outX[0] = inX[0]
    for x in range(0,len(inX)-1):
        outY[x+1] = (inY[x+1]+inY[x]-outY[x]*(1-alfa))/(alfa+1)
        outX[x+1] = (inX[x+1]+inX[x]-outX[x]*(1-alfa))/(alfa+1)

    return [outY,outX]

def Derivative(inY,inX,threshold):
    deriv = np.copy(inY)*0
    last_non_zero = 0.0
    for j in range(0,len(inX)-2):
        deriv[j] = (-inY[j+2]+4*inY[j+1]-3*inY[j])/(2*(inX[j]-inX[j-1]))
        if abs(deriv[j]) > threshold:
            deriv[j] = last_non_zero
        else:
            if abs(deriv[j]) > 0.0:
                last_non_zero = deriv[j]

    xyout = [deriv,inX]
    
    return xyout

# Copyright - Carlos Montalvo 2016
# You may freely distribute this file but please keep my name in here
# as the original owner
