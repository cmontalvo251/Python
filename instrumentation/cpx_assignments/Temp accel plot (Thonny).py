import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt('Test_Data.txt')

time = data[:,0]

time -= time[0]

Temp = data[:,4]
Ax = data[:,1]
Ay = data[:,2]
Az = data[:,3]

#Temp plot
plt.figure(1)
plt.plot(time,Temp)
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Temperature Plot')

#Acceleration plot
plt.figure(2)
plt.plot(time,Ax,label='X')
plt.plot(time,Ay,label='Y')
plt.plot(time,Az,label='Z')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Acceleration')
plt.title('Acceleration plot')

plt.show()
