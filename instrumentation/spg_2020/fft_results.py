import numpy as np
import matplotlib.pyplot as plt

def waveform(t):
    return 1.3*np.sin(2*np.pi*10*t) + 0.8*np.sin(2*np.pi*15*t) + -1.2*np.sin(2*np.pi*4*t)

## sin(2*pi*f*t)
## 2*pi*f*t needs to be in radians
## w = 2*pi*f - rad/s
## so if f is 1/s t is seconds and 2*pi is radians
## f is in Hz

##Actual waveform
t = np.linspace(0,1,10000)
f = waveform(t)

###Sampling Period
###Nyquist Frequency
###
fs = 35.
Ts = 1.0/fs
ts = np.arange(0.,1.,Ts)

###Frequencies of the two waves below are 10 and 15
###Period = 0.1 and 0.06ish.
##plot 10 period = 1 second
fs = waveform(ts)

#plt.plot(ts,fs,'r*')
plt.plot(t,f)

#a0 = 0.
plt.figure()
for n in range(1,20):
    b = 0.
    w0 = 2*np.pi
    #n = 4
    for i in range(0,len(fs)):
        b = b + fs[i]*np.sin(n*w0*ts[i])*Ts
    b = 2*b
    #print('n=',n,' b=',b)
    plt.plot([n,n],[0,abs(b)],'b-*')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.show()