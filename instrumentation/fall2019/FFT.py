import numpy as np
import matplotlib.pyplot as plt

##Actual waveform
t = np.linspace(0,1,10000)
f = 2*np.sin(2*np.pi*10*t) + np.sin(2*np.pi*15*t)


###Sampling Period
###Nyquist Frequency
###
fs = 100.
Ts = 1.0/fs

ts = np.arange(0.,1.,Ts)

###Frequencies of the two waves below are 10 and 15
###Period = 0.1 and 0.06ish.
##plot 10 period = 1 second
fs = 2*np.sin(2*np.pi*10*ts) + np.sin(2*np.pi*15*ts)

plt.plot(ts,fs,'r*')
plt.plot(t,f)

a0 = 0.
b10 = 0.
b15 = 0.0
f0 = 1.0
w0 = 2*np.pi*f0
for i in range(0,len(fs)):
    a0 = a0 + fs[i]*Ts
    b10 = b10 + fs[i]*np.sin(10.*w0*ts[i])*Ts
    b15 = b15 + fs[i]*np.sin(15.*w0*ts[i])*Ts
#a0 = a0 / len(fs)
b10 = 2*b10
b15 = 2*b15
print('a0=',a0)
print('b10=',b10)
print('b15=',b15)

plt.show()