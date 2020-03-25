import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('accelerometer.txt')
print(np.shape(data))

time = np.linspace(0,len(data)*0.1,len(data))

data20 = data[time<20]
time20 = time[time<20]

data_end = data[time > 52]
time_end = time[time > 52]

data_end2 = data_end[time_end < 63]
time_end2 = time_end[time_end < 63]

plt.plot(time,data,label='Full Data Set')
plt.plot(time20,data20,label='Time < 20 data set')
plt.plot(time_end2,data_end2,label='Time end data set')
plt.legend()
plt.grid()

plt.figure()
plt.plot(time20,data20,'m-')
plt.plot(time_end2-time_end2[0],data_end2,'g-')
plt.grid()

mean20 = np.mean(data20)
std20 = np.std(data20)
print(mean20,std20)
mean_end = np.mean(data_end2)
std_end = np.std(data_end2)
print(mean_end,std_end)

plt.figure()
plt.hist(data20)

plt.figure()
plt.hist(data_end2)

plt.show()