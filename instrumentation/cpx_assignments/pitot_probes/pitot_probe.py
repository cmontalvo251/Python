import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('2_15_2017.csv',delimiter=',')
time = data[:,0]
pitot = data[:,6]

plt.plot(time,pitot)

voltage = pitot*5.0/1023.0

plt.figure()
plt.plot(time,voltage)

offset = 2.542

scaled_voltage = voltage - offset

plt.figure()
plt.plot(time,scaled_voltage)

pressure = scaled_voltage/101.325

ainf = 331.0

k = 5*((pressure+1)**(2.0/7.0)-1)

U = ainf*np.sqrt(k)

plt.figure()
plt.plot(time,U)

plt.show()

