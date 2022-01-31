import matplotlib.pyplot as plt
import numpy as np

time = np.linspace(0,1,10000)
f0 = 10.0
w0 = 2*np.pi*f0
amplitude = np.sin(w0*time)

for fs in range(1,40):
    plt.clf()
    Ts = 1/fs
    print(fs)
    sampling_times = np.arange(0,1,Ts)
    samples = np.sin(w0*sampling_times)
    plt.plot(time,amplitude)
    plt.plot(sampling_times,samples,'r-*')
    plt.grid()
    plt.pause(2.0)
    
plt.show()