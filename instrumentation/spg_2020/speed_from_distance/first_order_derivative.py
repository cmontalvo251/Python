import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Trial_1_July_20_20.txt')

time = data[:,0]
distance = data[:,1]

distance_filtered = 0*distance
distance_filtered[0] = distance[0]
s = 0.05
# s = 0 --- totally filter out the signal
# s = 1 --- turn off the filter
for ctr in range(1,len(distance)):
    distance_filtered[ctr] = (1-s)*distance_filtered[ctr-1] + s*distance[ctr]

plt.figure()
plt.plot(time,distance,label='Raw')
plt.plot(time,distance_filtered,label='Filtered')
plt.xlabel('Time (sec)')
plt.ylabel('Distance (mm)')
plt.grid()
plt.legend()

###Let's take a derivative
dx = distance[1:]-distance[0:-1]
dt = time[1:]-time[0:-1]
speed = dx/dt
dx_filtered = distance_filtered[1:]-distance_filtered[0:-1]
speed_filtered = dx_filtered/dt

plt.figure()
plt.plot(dt,'b*')

plt.figure()
#plt.plot(time[0:-1],speed,label='No Filter')
plt.plot(time[0:-1],speed_filtered,label='Filtered')
plt.xlabel('Time (sec)')
plt.ylabel('Speed (mm/s)')
plt.grid()
plt.legend()

plt.show()

