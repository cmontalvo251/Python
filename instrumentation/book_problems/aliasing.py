import matplotlib.pyplot as plt
import numpy as np

time = np.linspace(0,10,10000)
f = 10.0
w = 2*np.pi*f
amplitude = np.sin(w*time)

for fs in range(1,10):
    plt.clf()
    Ts = 1/fs
    print(fs)
    sampling_times = np.arange(0,10,Ts)
    samples = np.sin(w*sampling_times)
    plt.plot(time,amplitude)
    plt.plot(sampling_times,samples,'r-*')
    plt.grid()
    plt.pause(1.0)
    
plt.show()