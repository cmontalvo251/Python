import time
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import math

def AAC(data,samplerate,lowestFreq,tau):
    #Ms point is the sampling rate divided by the lowest resolvable frequency 
    Ms = int(samplerate/lowestFreq)
    #Ts = length of segment in seconds
    Ts = (Ms/samplerate)
    #Tmax = maximum expected period
    Tmax = (1.0/lowestFreq)*samplerate
    #sample of the dataset to compare with
    segment = data[0:Ms]

    ##Initializes some variables
    found_slope = 0
    intersect = 0
    k = 0
    klast = 0.
    ko = 0.
    ZKo = 0.
    Yk = 0.
    Yklast=0.
    Ykvals = np.zeros((len(data)))
    Zk = 0.0
    Zkvals = np.zeros((len(data)))
    Zklast = 0.
    slopeZk =0.
    slopeYk =0.
    kint = 0.
    yint = 0.
    zkmax = -1e20
    kmax = 0
    frequency = 0
    
    #for k in range(0,len(data)-Ms):
    while k < len(data)-Ms:
        ##Compute slope
        if k == 0:
            Yk = Zk
        else:
            slopeZk = (Zk-Zklast)/(k-klast) 
            slopeYk = (Yk-Yklast)/(k-klast)

        ##determine if ko is found
        if found_slope == 0 and slopeZk < slopeYk:
            ko = k
            ZKo = Zk
            found_slope = 1

        ##Save previous values
        klast = k
        Yklast = Yk
        Zklast = Zk

        ##Compute new Zk
        Zk = 0
        for m in range(1,Ms):
            Zk += segment[m]*data[(m+k)]
        Zkvals[k] = Zk
            
        ##Compute New Yk
        Yk = ZKo*math.exp(-1.0*(k-ko)/(samplerate*tau))
        Ykvals[k] = Yk

        ###Find the intersection poit
        if k > ko and Zkvals[k] >= Ykvals[k] and ko != 0 and intersect == 0:
            intersect = 1
            kint = k
            yint = Ykvals[k]
            print('Intersection Found')

        #Find the maxima
        if intersect == 1:
            if zkmax < Zkvals[k]:
                #Found a new maxima
                zkmax = Zkvals[k]
                kmax = k
            if Zkvals[k] < Ykvals[k]:
                N = kmax - ko
                frequency = samplerate/N
                k = len(data)*2

        #Increment k
        k+=1

    return segment,Zkvals,Ykvals,kint,yint,zkmax,kmax,frequency

##Record audio
fs = 16000.
duration = 640./fs
tau = 20./1000.0
lowestFreq = 50.

fig1 = plt.figure()
rect1 = fig1.patch
rect1.set_facecolor('white')
plt1 = fig1.add_subplot(1,1,1)

fig2 = plt.figure()
rect2 = fig2.patch
rect2.set_facecolor('white')
plt2 = fig2.add_subplot(1,1,1)
plt.ion()
plt.show()

while True:
    print('Pluck Note')
    time.sleep(0.5)
    print('Recording..')
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)[:,0]
    t = np.linspace(0,duration,len(audio))
    print('done..')
    
    ###Plot stream
    plt1.cla()
    plt1.plot(t,audio)
    plt1.set_ylim([-0.2,0.2])

    segment,Zkvals,Ykvals,kint,yint,zkmax,kmax,frequency = AAC(audio,fs,lowestFreq,tau)
    print('Frequency = ',frequency)

    plt2.cla()
    plt2.plot(Zkvals,'b-',label='Zk')
    plt2.plot(Ykvals,'r-',label='Yk')
    plt2.plot(kint,yint,'g*')
    plt2.plot(kmax,zkmax,'r*')
    plt2.grid()

    plt.pause(0.0001)
