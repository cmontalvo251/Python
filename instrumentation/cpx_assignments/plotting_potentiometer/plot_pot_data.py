import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Test_Data.txt')

time = data[:,0]
time = time - time[0]
pot = data[:,1]

voltage = 3.3*pot/2**16

plt.plot(time,voltage)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Voltage (V)')
plt.show()
