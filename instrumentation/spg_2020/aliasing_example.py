import numpy as np
import matplotlib.pyplot as plt

##Generate true waveform
tfinal = 0.1
t = np.linspace(0,tfinal,10000)
fm = 80.0 #sampled frequency
wm = 2*np.pi*fm
y = np.cos(wm*t)
plt.plot(t,y,label='Truth')
plt.grid()

#Now let's sample it
fs = 160.0 #sampling rate in Hz
period = 1/fs #time between data points
number_of_data_points = int(tfinal/period)+1
tsample = np.linspace(0,tfinal,number_of_data_points)
ysample = np.cos(wm*tsample)
plt.plot(tsample,ysample,'r-*',label='Sampled Waveform')

plt.legend()
plt.show()