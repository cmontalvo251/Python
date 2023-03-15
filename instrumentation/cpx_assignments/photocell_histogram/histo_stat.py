import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('hist_stat.txt',delimiter=' ')
time = data[:,0]
time -= time[0]
ambient = data[:,1]
mu = np.mean(ambient)
print('Mean = ',mu)
s = np.std(ambient)
print('Standard Dev = ',s)
x = np.linspace(-3*s+mu,3*s+mu,100)
pdf = 1.0/(s*np.sqrt(2*np.pi))*np.exp((-(x-mu)**2)/(2.0*s**2))  * (s*np.sqrt(2*np.pi)) * 72
plt.plot(time,ambient)
plt.figure()
plt.hist(ambient)
plt.plot(x,pdf)
plt.show()