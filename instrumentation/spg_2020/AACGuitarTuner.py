import math 
import numpy as np
import matplotlib.pyplot as plt
import time

def AAC(data,samplerate,lowestFreq):
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

##############MAIN#########

#Sample rate of microphone (16000Hz)
samplerate = 16000.0
#lowest resolvable frequency (50Hz)
lowestFreq = 50.0
#Tmax = maximum number of expected periods
Tmax = 1.0/lowestFreq

#Timestep
dt = 1.0/samplerate

#Raw Data from CPX
# High E String Data
# B String Data (tau = 5)
# G String Data (tau = )
# D String Data (tau = )
# A String Data (tau = 20/1000)
# Low E String Data (tau = 20/1000)
all_data = np.loadtxt('raw_data.txt',delimiter=',')

##Pick a string
for x in range(0,6):
    data = all_data[x,:]

    #tau = time constant = somewhere between 6-10 ms for speech
    ##Low E, A, D
    if x > 3:
        tau = 20.0/1000.0
    else:
        ##G, B, E
        tau = 7.0/1000.0

    datamean = np.mean(data)
    datamin = np.min(data)
    datamax = np.max(data)
    data = data - datamean
    data = (2*data)/(datamax-datamin)
    plt.figure()
    plt.plot(data)
    plt.title('Raw Data')
    plt.grid()
    
    segment,Zkvals,Ykvals,kint,yint,zkmax,kmax,frequency = AAC(data,samplerate,lowestFreq)
    
    plt.plot(segment)

    plt.figure()
    plt.plot(Zkvals,'b-',label='Zk')
    plt.plot(Ykvals,'r-',label='Yk')
    plt.plot(kint,yint,'g*')
    plt.plot(kmax,zkmax,'r*')
    plt.grid()
    
    print('Frequency (Hz) = ',frequency)

plt.show()


