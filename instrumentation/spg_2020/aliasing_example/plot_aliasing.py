import numpy as np
import matplotlib.pyplot as plt

#files = ['100Hz.txt','10Hz.txt','1Hz.txt']
files = ['100Hz.LessMass.txt','10Hz.LessMass.txt','1Hz.LessMass.txt']
for f in files:
    s = f.split('.')
    hz = s[0]
    data = np.loadtxt(f)
    time = data[:,0]
    time-=time[0]
    acceleration = data[:,1]
    plt.plot(time,acceleration,'-*',label=hz)
plt.xlim([0,10])
plt.xlabel('Time (sec)')
plt.ylabel('Acceleration (m/s^2)')
plt.grid()
plt.legend()
plt.show()