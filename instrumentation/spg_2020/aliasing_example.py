import numpy as np
import matplotlib.pyplot as plt

##Generate true waveform
tfinal = 0.2
t = np.linspace(0,tfinal,10000)
fm = 80.0 #sampled frequency
wm = 2*np.pi*fm
y = np.cos(wm*t)
plt.plot(t,y,label='Truth')
plt.grid()

#Now let's sample it
fs = 85.0 #sampling rate in Hz
period = 1.0/fs #time between data points
tsample = np.arange(0,tfinal,period)
ysample = np.cos(wm*tsample)
plt.plot(tsample,ysample,'r-*',label='Sampled Waveform')

plt.legend()
plt.show()