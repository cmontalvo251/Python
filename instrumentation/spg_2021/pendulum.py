import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('pendulum.txt')

angle = -data
stop = len(data)*0.1
time = np.arange(0,stop,0.1)

tsettle = 12.0
sigma = 4.0/tsettle
period = 0.8
freq = 1/period
wd = 2*np.pi*freq
theta0 = 8.3
theta = theta0*np.exp(-sigma*time)*np.cos(wd*time)

plt.plot(time-3.16,angle+3.0,'b*')
plt.plot(time,theta,'r-')
#plt.xlim([0,3])
#plt.ylim([-10,20])
plt.show()